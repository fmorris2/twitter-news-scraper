import urllib2
import xml.etree.ElementTree as ET

APPLICATION_ID = 's4Iywt34'
# TODO DON'T HARDCODE IN SPACE CHARACTERS.... PASS TO URL_ENCODE METHOD INSTEAD WITH NORMAL SPACES
QUERY_BASE = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20geo.places%20where%20text%20=%27'

"""
    Handles the logic flow for grabbing
    a WOEID for a specific location
    
    This method simply goes through the
    necessary steps, calls helper methods
    for all of the hard work, and provides
    some safety with null checks along the way
    
    returns the WOEID for the location, or None
    if the parsing process failed
"""
def getWoeidForLoc(location):
    #first, build the url we'll query for the given location
    url = buildUrl(location)

    #second, query the url and parse the XML doc from it
    xml = parseXmlFromUrl(url)
    #little null check to make sure we connected & parsed successfully
    if xml is None:
        print 'Error parsing XML for ' + location
        return None

    #third, parse the WOEID from the XML
    woeid = parseWoeidFromXml(xml)
    #null check to make sure we parsed the woeid successfully
    if woeid is None:
        print 'Error parsing WOEID from XML'
        return None

    #SUCCESS, return the woeid for the given location
    return woeid

"""
    Parses XML from the Yahoo API endpoint
    returns the root element from the ElementTree API for parsing XML
"""
def parseXmlFromUrl(url):
    #setup the url request
    response = urllib2.urlopen(url)
    #read the doc and store it in a file
    html = response.read()
    #use the ElementTree API to convert the file into an XML tree (root element)
    return ET.fromstring(html)

"""
    Given an XML element representing the root of
    the API response, we will parse it and find the
    WOEID from within it
    
    return the WOEID, as as string
"""
def parseWoeidFromXml(xml):
    return xml[0][0][0].text

"""
    Build a safe url from the query base & location
"""
# TODO BUILD SAFE URL WITH URL_ENCODE
def buildUrl(location):
    return QUERY_BASE + location+"*%27"