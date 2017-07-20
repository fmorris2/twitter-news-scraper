from flask import jsonify
from backend.types import CachedTopicInfo
from backend.YahooGeoPlanetApi import getWoeidForLoc
from backend.TwitterApi import getTrendingTopics
from backend.NewsCollector import getNewsForTopics

class RequestParser:
    """Used to handle HTTP requests for
        certain routes

        Attributes:
            cache - dictionary mapping a location
                to it's news entries
                Key: location (WOEID)
                Val: CachedTopicInfo object
        """

    def __init__(self):
        self.cache = {} #initialize empty dictionary for cache

    """
        Grabs a json representation of the trending news for a location
    """
    def getNewsForLoc(self, location):
        #first, check cache
        if location in self.cache and self.cache[location].isValid():
            return jsonify(newsEntries = self.cache[location].newsEntries)

        #cache didn't have entry, or it wasn't valid. So parse a new one
        return self.parseAndCache(location)

    """
        From a provided location, we generate a
        list of NewsEntry objects, which will then
        be cached
    """
    def parseAndCache(self, location):
        #first, convert location to a WOEID
        woeid = getWoeidForLoc(location);

        #second, query Twitter API for top 50 trending topics for the WOEID
        topics = getTrendingTopics(woeid)

        #third, parse news stories from the web for each of the topics
        news = getNewsForTopics(topics)

        #fourth, create a cache entry with the generated news stories
        self.cache[location] = CachedTopicInfo.CachedTopicInfo(news)

        ##return JSON representation of news stories
        return jsonify(newsEntries = news)