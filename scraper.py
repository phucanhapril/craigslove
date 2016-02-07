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
    "status": 4,
    "body": 5,
    "zodiac": 6,
    "diet": 7,
    "facial hair": 8,
    "drinks": 9,
    "eye color": 10,
    "religion": 11 }

AD_TYPE = [ "stp", "w4w", "w4m", "m4w", "m4m", "msr", "cas", "mis", "rnr"]

def parse_search_result_page(search_url):
    results = []
    # search_term = search_term.strip().replace(' ', '+')
    # search_url = URL_LINKER.format(search_term)
    soup = BeautifulSoup(urlopen(search_url).read())
    rows = soup.find('div', 'content').find_all('p', 'row')
    for row in rows:
        if row.a['href'].startswith("//"):
            url = "http:" + row.a['href']
        else:     
            url = 'http://providence.craigslist.org' + row.a['href']
        create_date = row.find('time').get('datetime')
        title = row.find_all('a')[1].get_text()
        results.append({'url': url, 'create_date': create_date, 'title': title})
    return results



##Method to save all the neccesary data into csv
def parse_page_result(URL_LINK):
    #print URL_LINK
    result_array = []
    search_url = URL_LINK.format(URL_LINK)
    #print search_url
    soup = BeautifulSoup(urlopen(search_url).read())

    result_array = soup.find_all("p", "attrgroup")
    post = {}
    post["url"] = search_url
    post["title"] = soup.title.get_text()
    post["text"] = soup.find(id="postingbody").get_text()

    for p in result_array:
        for span in p.find_all("span"):
           #  print span 
            if span.b is None:  
                continue           
            value = span.b.extract().get_text()
            key = span.get_text()[:-2].strip() # strip colons and trailing whitespace
            post[key] = value
    return post



def write_results_page(page):
    print page
    valueList = [None] * len(COLUMN_MAP)
    for key in page:
        if key in COLUMN_MAP:
            index = COLUMN_MAP[key]
            valueList[index] = page[key]    
    try:
        outputWriter.writerow(valueList)
    except UnicodeEncodeError:
        pass
    

if __name__ == '__main__':
    outputFile = open('results.csv', 'w')
    outputWriter = csv.writer(outputFile)
    orderedColumns = sorted(COLUMN_MAP, key=lambda k: COLUMN_MAP[k])
    outputWriter.writerow(orderedColumns);
        

    # TODO search all pages for each query
    # TODO search different cities

    # do a search for every ad type
    for adType in AD_TYPE:
        print "searching " + adType
        searchUrl = "http://providence.craigslist.org/search/" + adType
        searchResults = parse_search_result_page(searchUrl)
        # iterate thru search results and scrap each page
        for ad in searchResults:
            print "scraping " + ad['url']
            parsedPost = parse_page_result(ad['url'])
            # write parsed post to csv
            write_results_page(parsedPost)
        
    outputFile.close()

