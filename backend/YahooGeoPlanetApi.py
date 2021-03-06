import urllib2
import xml.etree.ElementTree as ET

SAFE_URL_PARAMS = "%/:=&?~+!$,;'@()*[]"
QUERY_BASE = 'http://query.yahooapis.com/v1/public/yql?q=select * from geo.places where text =\''

"""
    Handles the logic flow for grabbing
    the latitude and longitude for a specific location
    
    This method simply goes through the
    necessary steps, calls helper methods
    for all of the hard work, and provides
    some safety with null checks along the way
    
    returns a tuple containing the latitude
    and longitude for the location, or None
    if the parsing process failed
"""
def get_coords_for_loc(location):
    #first, build the url we'll query for the given location
    url = build_url(location)

    #second, query the url and parse the XML doc from it
    xml = parse_xml_from_url(url)
    #little null check to make sure we connected & parsed successfully
    if xml is None:
        print 'Error parsing XML for ' + location
        return None

    #third, parse the lat & long from the XML
    coords = parse_coords_from_xml(xml)
    #null check to make sure we parsed the coords successfully
    if coords is None:
        print 'Error parsing coords from XML'
        return None

    #SUCCESS, return the coords for the given location
    return coords

"""
    Parses XML from the Yahoo API endpoint
    returns the root element from the ElementTree API for parsing XML
"""
def parse_xml_from_url(url):
    #setup the url request
    response = urllib2.urlopen(url)
    #read the doc and store it in a file
    html = response.read()
    #use the ElementTree API to convert the file into an XML tree (root element)
    return ET.fromstring(html)

"""
    Given an XML element representing the root of
    the API response, we will parse it and find the
    lat & longitude from within it
    
    return the coords, as a tuple
"""
def parse_coords_from_xml(xml):
    #TODO eventually improve this method of parsing.... Not very good
    loc = xml[0][0]
    for child in loc:
        if 'centroid' in child.tag:
            return (child[0].text, child[1].text)
    return (None, None)

"""
    Build a safe url from the query base & location
"""
def build_url(location):
    utf8 = (QUERY_BASE + location+"*'").encode('utf8')
    return urllib2.quote(utf8, SAFE_URL_PARAMS)