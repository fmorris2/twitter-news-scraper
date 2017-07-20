import time

class CachedTopicInfo:
    """A container containing information
        about an entry in the topic cache.

    Attributes:
        timeCached (the time that this cache entry was last updated)
        newsEntries (list of news entries associated with topics)
    """
    CACHE_TIME = 60 * 5 #5 minutes represented in seconds

    def __init__(self, newsEntries):
        self.timeCached = time.time()
        self.newsEntries = newsEntries

    """returns whether or not the cache entry is valid
        based on the Twitter API cache time (5 minutes)
        
        if the entry is within the cache time, it is
        considered valid
    """
    def isValid(self):
        return time.time() - self.timeCached < self.CACHE_TIME
