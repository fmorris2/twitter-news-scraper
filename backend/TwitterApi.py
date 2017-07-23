from urllib import quote
from base64 import b64encode
from requests import post, get

class TwitterApi:
    """
        Keys to access Twitter API using oAuth2
        These need to be provided in the data/twitter_api_keys
        file. Consumer key goes on the first line, secret key
        goes on the second line
    """
    CONSUMER_KEY = ''
    SECRET_KEY = ''

    #API endpoint to obtain a bearer token from
    OBTAIN_TOKEN_URL = 'https://api.twitter.com/oauth2/token'

    #API endpoint to obtain trending topics for a place
    OBTAIN_TOPICS_URL = 'https://api.twitter.com/1.1/trends/place.json'

    #API endpoint to obtain the closest woeid supported by the twitter API for a given lat/long
    OBTAIN_CLOSEST_WOEID_URL = 'https://api.twitter.com/1.1/trends/closest.json'

    KEY_FILE_PATH = '/data/twitter_api_keys'
    ROOT_PATH = ''
    BASE64_BEARER_TOKEN_CREDENTIALS = ''

    def __init__(self):
        self.readKeys()
        self.setBearerTokenCredentials()

    """
        Grab trending topics for a specific location,
        specified by a coordinate pair(latitude & longitude).
        First we must obtain the WOEID for the Twitter-supported
        location closest to the given coords. Secondly, we access
        a different endpoint on the Twitter API to obtain the trending
        topics related to the WOEID.
    """
    def getTrendingTopics(self, coords):
        #obtain WOEID for coords
        woeid = self.obtainWoeid(coords)
        if woeid == -1:
            return []

        #obtain trending topics for the WOEID
        topics = self.obtainTopics(woeid)
        print 'Topics: ' + str(topics)
        return topics

    """
        Obtains a Twitter-supported WOEID
        closest to the supplied coordinate
        pair
    """
    def obtainWoeid(self, coords):
        token = self.obtainBearerToken()
        if token is None:
            return -1

        headers = {
            'Authorization': 'Bearer ' + token,
        }
        payload = {'lat':coords[0], 'long':coords[1]}
        response = get(self.OBTAIN_CLOSEST_WOEID_URL, headers=headers, params=payload)
        json = response.json()
        if 'errors' not in json:
            return json[0]['woeid']

        return -1

    """
        Obtains a bearer token to access the Twitter-API
        with
    """
    def obtainBearerToken(self):
        headers = {
            'Authorization':'Basic ' + self.BASE64_BEARER_TOKEN_CREDENTIALS,
            'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8.'
        }
        data = 'grant_type=client_credentials'
        response = post(self.OBTAIN_TOKEN_URL,headers=headers, data=data)
        json = response.json()
        if json['token_type'] == 'bearer':
            return json['access_token']

        return None

    """
        Obtain the top trending topics for the
        provided Twitter-supported WOEID. Sort
        them by tweet-volume (high to low), and
        return them in a list
    """
    def obtainTopics(self, woeid):
        token = self.obtainBearerToken()
        if token is None:
            return []

        topics = []

        headers = {
            'Authorization': 'Bearer ' + token,
        }
        payload = {'id':woeid}
        response = get(self.OBTAIN_TOPICS_URL,headers=headers, params=payload)
        json = response.json()
        if 'errors' not in json:
            trends = json[0]['trends']
            for trend in trends:
                topics.append((trend['name'], trend['tweet_volume']))

        #sort topics by tweet volume
        topics.sort(key=lambda tup: tup[1], reverse=True)
        return topics

    """
        Per Twitter's directions on encoding
        the consumer & secret keys, we perform the
        following steps:
        1.) URL encode the consumer & secret keys according to RFC1738
        2.) Concatenate the two RFC1738 encoded keys with a colon ":"
        3.) Base64 encode the concatenated string
    """
    def setBearerTokenCredentials(self):
        consumer = self.rfc1738encode(self.CONSUMER_KEY)
        secret = self.rfc1738encode(self.SECRET_KEY)
        concatenated = consumer + ":" + secret
        self.BASE64_BEARER_TOKEN_CREDENTIALS = b64encode(concatenated)

    """
        URL encodes the specified key (string)
        according to RFC 1738
    """
    def rfc1738encode(self, key):
        return quote(key)

    """
        Reads the Twitter API keys from the
        file twitter_api_keys in the data directory
    """
    def readKeys(self):
        lines = open(self.ROOT_PATH + self.KEY_FILE_PATH).read().splitlines()
        self.CONSUMER_KEY = lines[0]
        self.SECRET_KEY = lines[1]
        print self.CONSUMER_KEY + ':' + self.SECRET_KEY

