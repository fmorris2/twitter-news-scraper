#!/usr/bin/env python
import os
from flask import Flask
from backend import RequestParser, TwitterApi

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
TwitterApi.TwitterApi.ROOT_PATH = ROOT_PATH

app = Flask('twitter_news_scraper')
requestParser = RequestParser.RequestParser()

@app.route('/')
def test():
    return 'Online'

@app.route('/news/<location>')
def scrape(location):
    return requestParser.getNewsForLoc(location)

if __name__ == '__main__':
    app.run()
