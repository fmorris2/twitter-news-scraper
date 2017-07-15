# Overview of Twitter News Scraper (TNS)
A RESTful web service which scrapes trending topics from Twitter, compiles a collection of relevant news stories, and provides information about them in JSON format.

### Architecture
- Language: [Python](https://www.python.org/)
- Frameworks:
    - [Flask](http://flask.pocoo.org/)

### Basic Logic Flow
1. User accesses API endpoint wth GET request
    - User has ability to provide a country or city to narrow the search
        - Location has to be supported by [trends24](https://trends24.in)
        - If no location is provided, service will default to worldwide
    - User has ability to provide a time frame to narrow the search
        - < 1 hour ago
        - 1-23 hours ago
2. Backend collects trending topics for provided criteria
    - If criteria is invalid, returns HTTP status code 400 (Bad Request)
    - If criteria is valid, backend parses [trends24](https://trends24.in) for the specific criteria
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
