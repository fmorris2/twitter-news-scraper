from flask import jsonify
from backend import TwitterApi
from backend.types import CachedTopicInfo
from backend.YahooGeoPlanetApi import getWoeidForLoc
from backend.NewsCollector import getNewsForTopics

class RequestParser:
    """Used to handle HTTP requests for
        certain routes

        Attributes:
            twitterApi - object used for accessing
                the Twitter API

            cache - dictionary mapping a location
                to it's news entries
                Key: woeid (WOEID)
                Val: CachedTopicInfo object
        """

    def __init__(self):
        self.twitterApi = TwitterApi.TwitterApi()
        self.cache = {} #initialize empty dictionary for cache

    """
        Grabs a json representation of the trending news for a location
    """
    def getNewsForLoc(self, location):
        #first, get WOEID for location
        woeid = getWoeidForLoc(location)

        #second, check cache
        if location in self.cache and self.cache[woeid].isValid():
            return jsonify(newsEntries = self.cache[woeid].newsEntries)

        #cache didn't have entry, or it wasn't valid. So parse a new one
        return self.parseAndCache(woeid)

    """
        From a provided woeid, we generate a
        list of NewsEntry objects, which will then
        be cached
    """
    def parseAndCache(self, woeid):
        #query Twitter API for top 50 trending topics for the WOEID
        topics = self.twitterApi.getTrendingTopics(woeid)

        #parse news stories from the web for each of the topics
        news = getNewsForTopics(topics)

        #create a cache entry with the generated news stories
        self.cache[woeid] = CachedTopicInfo.CachedTopicInfo(news)

        ##return JSON representation of news stories
        return jsonify(newsEntries = news)