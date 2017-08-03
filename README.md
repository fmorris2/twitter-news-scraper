# Overview of Twitter News Scraper (TNS)
A RESTful web service which scrapes trending topics from Twitter, compiles a collection of relevant news stories, and provides information about them in JSON format.

### Architecture
- Language: [Python](https://www.python.org/)
- Frameworks:
    - [Flask](http://flask.pocoo.org/)

### Basic Logic Flow
1. User accesses API endpoint wth GET request
    - User has ability to provide a location (zip, city, country, etc) to narrow the search
        - If no location is provided, service will default to worldwide
2. Backend checks cache to see if we have the supported Twitter WOEID for the provided location stored.
    - If the location does not have a cache entry, backend will query the Yahoo GEOPlanet API to find the coordinates (latitude & longitude) for the provided location.
    - It will then query the Twitter API to find the closest supported WOEID for trending topics relative to the actual provided location, and cache it.
3. Backend checks news cache to see if we have already parsed news stories for the location in a certain time frame.
    - If the cache entry is valid, return it.
    - Otherwise, continue on to parse the news stories for the location.
3. Backend collects trending topics for provided criteria
    - Consumes Twitter API to gather trending topics for the supported WOEID.
4. Backend finds appropriate news story for each trending topic
    - Will request the Google News RSS feed for each specific topic, and parse info from the top news story.
4. Backend compiles information for each news story
    - Trending topic
    - Tweet volume
    - News story title
    - News story URL
5. Backend returns collection of news story information
    - Format: JSON
    - Status code: 200 (OK)

### Usage
Put on a server, make sure you're port forwarded and have the required python libraries (flask, requests), and run.

### Public Access
TNS can be accessed publicly at
```
tns.vikingsoftware.org:5000/news/[Location]
```
Example usage:
```
tns.vikingsoftware.org:5000/news/Europe
```
This would return news stories relating to the trending twitter topics closes to Europe.
