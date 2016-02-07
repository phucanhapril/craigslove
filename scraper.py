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

AD_TYPE = [ "stp", "w4w", "w4m", "m4w", "m4m", "msr", "cas", "mis", "rnr"]

def parse_search_result_page(search_url, city_url):
    results = []
    # search_term = search_term.strip().replace(' ', '+')
    # search_url = URL_LINKER.format(search_term)
    soup = BeautifulSoup(urlopen(search_url).read())
    rows = soup.find('div', 'content').find_all('p', 'row')
    for row in rows:
        ##print row.a['href']
        if row.a['href'].startswith("//"):
            url = "http:" + row.a['href']
        else:     
            url = 'http://' + city_url + row.a['href']
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
    cities_less_url = city_url.split(".")
    post["city"] = cities_less_url[0]
    post["url"] = search_url
    post["title"] = soup.title.get_text()
    
    try:
        post["text"] = soup.find(id="postingbody").get_text()
    except AttributeError:
        pass

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
    ##print page
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
    file = open('locations.txt', 'r')

    
    for city in file:
        city_url =  city
        city_url = city_url.strip('\n')
        print "In city " + city_url

    # do a search for every ad type
        for adType in AD_TYPE:
            ##print "searching " + adType
            searchUrl = "http://" + city_url + "/search/" + adType
            ##print "URL is:" + searchUrl

            searchResults = parse_search_result_page(searchUrl, city_url)
            # iterate thru search results and scrap each page
            for ad in searchResults:
                ##print "scraping " + ad['url']
                parsedPost = parse_page_result(ad['url'] )
                # write parsed post to csv
                write_results_page(parsedPost)
        
    outputFile.close()

