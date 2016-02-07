from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import datetime
import csv
import sys
import os
import smtplib
import config

# Craigslist search ,
BASE_URL = ('http://providence.craigslist.org/search/'
            '?sort=rel&areaID=11&subAreaID=&query={0}&catAbb=sss')

COLUMN_MAP = {
    "url": 0,
    "title": 1, 
    "text": 2,
    "age": 3,
    "city": 4,
    "status": 5,
    "body": 6,
    "zodiac": 7,
    "diet": 8,
    "facial hair": 9,
    "drinks": 10,
    "eye color": 11,
    "religion": 12 }

AD_TYPE = [ "stp", "w4w", "w4m", "m4w","m4m", "msr", "cas", "mis", "rnr"]


CITY_LINKS = [
    'providence.craigslist.org',
    'newyork.craigslist.org',
    'sfbay.craigslist.org',
    'washingtondc.craigslist.org',
    'dallas.craigslist.org'
    ]

"""
return a list of URLs from a personals search result
"""
def parse_search_result_page(search_url, city_url_root):
    
    soup = BeautifulSoup(urlopen(search_url).read(), "html.parser")
    rows = soup.find('div', 'content').find_all('p', 'row')

    results = []
    for row in rows:
        
        """
        skip url if href starts with "//" to avoid double counting
        because it means they're linking to a "nearby city"
        """
        postinghref = row.a['href'] 
        if not postinghref.startswith("//") and not postinghref.startswith("http") :
            url = 'http://' + city_url_root + postinghref
            results.append(url)

    return results


# parse text and relevant attributes from a personal ad
def parse_page_result(page_url, city):
    #print URL_LINK
    result_array = []
    # search_url = URL_LINK.format(URL_LINK)
    # print URL_LINK + " VS " + search_url
    try:
       soup = BeautifulSoup(urlopen(page_url).read(), "html.parser")
    except Exception as e:
        print e
        return

    
    # post represents the single personal ad on this page
    post = {}

    post["city"] = city
    post["url"] = page_url

    if soup.title is not None:
        post["title"] = soup.title.get_text()
    
    postingbody = soup.find(id="postingbody")
    if postingbody is not None:
        post["text"] = postingbody.get_text()

    # find all attributes (age, status, body, etc)
    attr_array = soup.find_all("p", "attrgroup")
    for p in attr_array:
        for span in p.find_all("span"):
            if span.b is None:  
                continue           
            value = span.b.extract().get_text()
            key = span.get_text()[:-2].strip() # strip colons and trailing whitespace
            post[key] = value
    return post


# save a personal ad to a csv (as a single row)
def write_post(post):
    valueList = [None] * len(COLUMN_MAP)
    for key in post:
        if key in COLUMN_MAP:
            index = COLUMN_MAP[key]
            valueList[index] = post[key].encode('utf8')   
    try:
        outputWriter.writerow(valueList)
    except UnicodeEncodeError as e:
        print e
    

if __name__ == '__main__':
    outputFile = open('results.csv', 'w')
    outputWriter = csv.writer(outputFile)
    orderedColumns = sorted(COLUMN_MAP, key=lambda k: COLUMN_MAP[k])
    outputWriter.writerow(orderedColumns);

    # load location file containing craigslist urls for each city
    #file = open('locations.txt', 'r')

    for city in CITY_LINKS:
        city_url = city.strip('\n')
        city_name = city_url.split(".")[0]
        print "In city " + city_url

        # do a search for every ad type
        for adType in AD_TYPE:
            print "searching " + adType
            count = 0
            searchUrl = "http://" + city_url + "/search/" + adType + "/?s=" + str(count)

            searchResults = parse_search_result_page(searchUrl, city_url)
            
            while len(searchResults) > 0:
                print "searching count " + str(count)
                # iterate thru search results and scrap each page
                for adUrl in searchResults:
                    print "scraping " + adUrl
                    parsedPost = parse_page_result(adUrl, city_name)
                    # write parsed post to csv
                    write_post(parsedPost)

                count += 100
                searchUrl = "http://" + city_url + "/search/" + adType + "/?s=" + str(count)
                searchResults = parse_search_result_page(searchUrl, city_url)
        
    outputFile.close()

