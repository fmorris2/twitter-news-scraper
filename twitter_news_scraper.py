#!/usr/bin/env python

from flask import Flask, jsonify
from backend.RequestParser import getNewsForLoc

app = Flask('twitter_news_scraper')


@app.route('/')
def test():
    return 'Online'

@app.route('/news/<location>')
def scrape(location):
    return getNewsForLoc(location)


if __name__ == '__main__':
    app.run()
