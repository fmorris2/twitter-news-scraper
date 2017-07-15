#!/usr/bin/env python

from flask import Flask, jsonify

app = Flask('twitter_news_scraper')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
