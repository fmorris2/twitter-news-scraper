class TwitterApi:
    """
        Keys to access Twitter API using oAuth2
        These need to be provided in the data/twitter_api_keys
        file. Consumer key goes on the first line, secret key
        goes on the second line
    """
    CONSUMER_KEY = ''
    SECRET_KEY = ''

    KEY_FILE_PATH = '/data/twitter_api_keys'
    ROOT_PATH = ''

    def __init__(self):
        self.readKeys()

    def getTrendingTopics(self, woeid):
        return []

    def readKeys(self):
        file = open(self.ROOT_PATH + self.KEY_FILE_PATH) #read mode is assumed since mode param is omitted
        CONSUMER_KEY = file.readline()
        SECRET_KEY = file.readline()
        print CONSUMER_KEY + ':' + SECRET_KEY

