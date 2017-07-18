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
2. Backend collects trending topics for provided criteria
    - If criteria is invalid, returns HTTP status code 400 (Bad Request)
    - If criteria is valid, backend consumes Twitter API to gather trending topics for the specified criteria.
        - The backend will take the location parameter provided, and will pass it to the Yahoo geoplanet API in order to retrieve the WOEID (where on earth id) that will be passed to the Twitter API 
3. Backend finds appropriate news story for each trending topic
    - Coming soon
4. Backend compiles information for each news story
    - URL
    - Title
    - Short description
    - Trending topic
5. Backend returns collection of news story information
    - Format: JSON
    - Status code: 200 (OK)

### Usage
Coming soon

### Public Access
TNS is not currently hosted for public use. When the project is finished, this section will be updated with the appropriate info.
