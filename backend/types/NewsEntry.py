class NewsEntry:
    """An news entry which relates a news article to a trending topic on Twitter

    Attributes:
        url
        title
        desc
        topic
    """

    def __init__(self, url, title, desc, topic):
        self.url = url
        self.title = title
        self.desc = desc
        self.topic = topic
