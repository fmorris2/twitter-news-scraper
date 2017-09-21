from flask import jsonify
from backend import TwitterApi, NewsCollector
from backend.types import CachedTopicInfo
from backend.YahooGeoPlanetApi import get_coords_for_loc

class RequestParser:
    """Used to handle HTTP requests for
        certain routes

        Attributes:
            twitterApi - object used for accessing
                the Twitter API

            newsCollector - object used for scraping
                news.google.com for news stories

            cache - dictionary mapping a WOEID
                to it's news entries
                Key: woeid
                Val: CachedTopicInfo object

            woeidCache - dictionary mapping a location
                to it's Twitter-supported closest WOEID
        """

    def __init__(self):
        self.twitter_api = TwitterApi.TwitterApi()
        self.news_collector = NewsCollector.NewsCollector()
        self.cache = {} #initialize empty dictionary for cache
        self.woeidCache = {} #initialize empty dictionary for woeid cache

    """
        Grabs a json representation of the trending news for a location
    """
    def get_news_for_loc(self, location):
        #grab woeid for location from woeidCache
        woeid = self.woeidCache[location] if location in self.woeidCache else None
        coords = None
        if woeid is None: #if we don't have the WOEID cached for this loc
            coords = get_coords_for_loc(location)
            woeid = self.twitter_api.obtain_woeid(coords)
            if woeid == -1:
                print 'failed to get WOEID for ' + location + ' at coords ' + str(coords)
                self.woeidCache[location] = woeid

        #check cache for location entry
        cachedEntry = self.cache[woeid] if woeid in self.cache else None

        #check if cached location entry is valid
        if cachedEntry != None and cachedEntry.isValid():
            return jsonify(newsEntries = cachedEntry.newsEntries)

        #cache didn't have entry, or it wasn't valid. So parse a new one
        return self.parse_and_cache(location, woeid, coords)

    """
        From a provided woeid, we generate a
        list of 3-tuples containing news info, 
        which will then be cached
    """
    def parse_and_cache(self, location, woeid, coords):
        if woeid == -1 or coords is None:
            return jsonify(newsEntries = ())

        print 'parse_and_cache for ' + location + ', ' + str(woeid) + ', ' + str(coords)

        #query Twitter API for top 50 trending topics for the coordinates
        topics = self.twitter_api.get_trending_topics(coords)

        #parse news stories from the web for each of the topics
        news = self.news_collector.get_news_for_topics(topics)

        #create a cache entry with the generated news stories
        self.cache[woeid] = CachedTopicInfo.CachedTopicInfo(coords, news)

        ##return JSON representation of news stories
        return jsonify(news_entries = news)
