from flask import jsonify
from backend import TwitterApi
from backend.types import CachedTopicInfo
from backend.YahooGeoPlanetApi import getCoordsForLoc
from backend.NewsCollector import getNewsForTopics

class RequestParser:
    """Used to handle HTTP requests for
        certain routes

        Attributes:
            twitterApi - object used for accessing
                the Twitter API

            cache - dictionary mapping a location
                to it's news entries
                Key: location
                Val: CachedTopicInfo object
        """

    def __init__(self):
        self.twitterApi = TwitterApi.TwitterApi()
        self.cache = {} #initialize empty dictionary for cache

    """
        Grabs a json representation of the trending news for a location
    """
    def getNewsForLoc(self, location):
        #check cache for location entry
        cachedEntry = self.cache[location] if location in self.cache else None
        coordinates = cachedEntry.coordinates if cachedEntry != None else getCoordsForLoc(location)

        #second, check cache
        if cachedEntry != None and cachedEntry.isValid():
            return jsonify(newsEntries = cachedEntry.newsEntries)

        #cache didn't have entry, or it wasn't valid. So parse a new one
        return self.parseAndCache(location, coordinates)

    """
        From a provided woeid, we generate a
        list of NewsEntry objects, which will then
        be cached
    """
    def parseAndCache(self, location, coords):
        #query Twitter API for top 50 trending topics for the coordinates
        topics = self.twitterApi.getTrendingTopics(coords)

        #parse news stories from the web for each of the topics
        news = getNewsForTopics(topics)

        #create a cache entry with the generated news stories
        self.cache[location] = CachedTopicInfo.CachedTopicInfo(coords, news)

        ##return JSON representation of news stories
        return jsonify(newsEntries = news)