import urllib2
import xml.etree.ElementTree as ET

from YahooGeoPlanetApi import SAFE_URL_PARAMS

class NewsCollector:
    BASE_GOOGLE_NEWS_URL = 'https://news.google.com/news/rss/search/section/q/'

    """
       Takes a list of topics (Strings), and creates a
       list of 4-tuples associated with them.
    
       returns a list of 4-tuples
    """
    def get_news_for_topics(self, topics):
        print 'getting news for topics: ' + str(topics)
        newsEntries = []
        for topic in topics:
            entry = self.get_news_entry_for_topic(topic[0], topic[1])
            if entry is not None:
                newsEntries.append(entry)

        return newsEntries

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

    def parse_news_story(self, url):
        print 'Starting to parse news link for [' + url + ']'
        newsLink = None
        # send a GET request to the news.google URL and save the page as a file
        resp = urllib2.urlopen(url)
        html = resp.read()
        xml = ET.fromstring(html)
        return self.parse_news_from_xml(xml[0])

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