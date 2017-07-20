#!/usr/bin/env python

from flask import Flask, jsonify
from backend import RequestParser

app = Flask('twitter_news_scraper')
requestParser = RequestParser()

@app.route('/')
def test():
    return 'Online'

@app.route('/news/<location>')
def scrape(location):
    return requestParser.getNewsForLoc(location)


if __name__ == '__main__':
    app.run()
