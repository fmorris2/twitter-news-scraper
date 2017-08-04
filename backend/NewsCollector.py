import urllib2
import Queue
import threading
import xml.etree.ElementTree as ET

from YahooGeoPlanetApi import SAFE_URL_PARAMS

class NewsCollector:
    BASE_GOOGLE_NEWS_URL = 'https://news.google.com/news/rss/search/section/q/'

    """
       Takes a list of topics (Strings), and creates a
       list of 4-tuples associated with them.
       
       Creates a separate thread for each topic, and parses the
       news for each topic in parallel. This is much faster than
       doing it in serial fashion.
    
       returns a list of 4-tuples
    """
    def get_news_for_topics(self, topics):
        print 'getting news for topics: ' + str(topics)
        newsEntries = Queue.Queue()
        # wrapper to collect return value in a Queue
        def task_wrapper(*args):
            newsEntries.put(self.get_news_entry_for_topic(args[0], args[1]))
        threads = [threading.Thread(target=task_wrapper, args=topic) for topic in topics]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        #Iterate through queue, filter out None values, and put into a serializable list
        newsList = []
        for e in newsEntries.queue:
            if e is not None:
                newsList.append(e)
        return newsList

    """
        Create a news entry for a specific topic.
        Parses news.google.com for the topic, and
        scrapes the top news story.
        
        returns a 4-tuple representing news info
    """
    def get_news_entry_for_topic(self, topic, tweet_volume):
        #first, get news.google.com search URL for topic
        url = self.create_safe_url(topic)

        #second, parse the news entry from the URL
        return self.parse_news_entry(topic, tweet_volume, url)

    """
        Provided a news.google.com search
        url as a parameter, we will then open
        a connection to the web page, parse the HTML,
        and then parse the top news story from it
        and return it as a NewsEntry object
    """
    def parse_news_entry(self, topic, tweet_volume, url):
        newsStory = self.parse_news_story(url)
        if newsStory is None:
            return None

        return topic, tweet_volume, newsStory[0], newsStory[1]

    """
        Provided a url, we will open the page,
        convert the contents into an XML element
        tree, and pass it to the parse_news_from_xml
        method.
        
        If urllib2#urlopen raises a URLError,
        we will simple return None
    """
    def parse_news_story(self, url):
        print 'Starting to parse news link for [' + url + ']'
        newsLink = None
        # send a GET request to the news.google URL and save the page as a file
        try:
            resp = urllib2.urlopen(url)
            html = resp.read()
            xml = ET.fromstring(html)
            return self.parse_news_from_xml(xml[0])
        except urllib2.URLError:
            return None

    """
        Provided an element tree as the xml of
        the web page, we will parse the news
        story from it, and return it as a tuple
        (title, url)
        
        Definitely should not use indexes to find the
        first item (like I'm currently doing). Need
        to update to a better method
    """
    #TODO upgrade parsing method from indexes to something safer
    def parse_news_from_xml(self, xml):
        if xml is None:
            return None
        for child in xml:
            if child.tag == 'item':
                return child[0].text, child[1].text
        return None

    """
        Encodes the topic with the base google news url,
        and ensures it is URL safe
    """
    def create_safe_url(self, topic):
        utf8 = (self.BASE_GOOGLE_NEWS_URL + topic).encode('utf8')
        return urllib2.quote(utf8, SAFE_URL_PARAMS)