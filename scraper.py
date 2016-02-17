from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import datetime
import csv
import sys
import os
import smtplib
import config
import re

# Flag for scraping only first page of search results for each query (to not overwhelm craigslist when testing)
FIRST_PAGE_ONLY = True

COLUMNS = [
    # required
    'url',
    'city', # need?
    'datetime',
    'category', # ex CAS
    'type', # ex M4W
    'title',
    'text',
    # optional
    'age',
    'body',
    'body art',
    'diet',
    'dislikes',
    'drinks',
    'drugs',
    'education',
    'ethnicity',
    'eye color',
    'facial hair',
    'fears',
    'hair',
    'height',
    'hiv/hsv/hpv',
    'interests',
    'kids, have',
    'kids, want',
    'likes',
    'native language',
    'occupation',
    'personality',
    'pets',
    'politics',
    'religion',
    'resembles',
    'smokes',
    'status',
    'weight',
    'zodiac' ]

PERSONALS_SECTIONS = [ "stp", "w4w", "w4m", "m4w","m4m", "msr", "cas", "mis", "rnr" ]

# SEARCH_TYPES = [ 'w4m', 'm4m', 'm4w', 'w4w', 't4m', 'm4t', 't4w', 'w4t', 't4t', 'mw4mw', 'mw4w', 'mw4m',
# 'w4mw', 'm4mw', 'w4ww', 'm4mm', 'mm4m', 'ww4w', 'ww4m', 'mm4w', 'm4ww', 'w4mm', 't4mw', 'mw4t' ]

CITY_LINKS = [
    # 'providence.craigslist.org'
    # 'newyork.craigslist.org'
    # 'sfbay.craigslist.org',
    # 'washingtondc.craigslist.org',
     'dallas.craigslist.org'
    ]

# get a list of URLs from a personals search result
def parse_search_result_page(search_url, city_url_root):
    
    soup = BeautifulSoup(urlopen(search_url).read(), "html.parser")
    rows = soup.find('div', 'content').find_all('p', 'row')

    url_list = []
    for row in rows:
        
        """
        skip url if href starts with "//" to avoid double counting
        because it means they're linking to a "nearby city"
        """
        postinghref = row.a['href'] 
        if not postinghref.startswith("//") and not postinghref.startswith("http") :
            url = 'http://' + city_url_root + postinghref
            url_list.append(url)

    return url_list


# parse text and relevant attributes from a personal ad
def parse_page_result(page_url):
    try:
       soup = BeautifulSoup(urlopen(page_url).read(), "html.parser")
    except Exception as e:
        print e
        return

    # the post object represents the single personal ad on this page
    post = {}

    # wrap the whole thing in a try-except because at any point the post may be marked for removal
    try:
        # get title
        post["title"] = soup.title.get_text()

        # get text body
        post["text"] = soup.find(id="postingbody").get_text()

        # get time
        post["datetime"] = soup.find('time', class_='timeago')["datetime"]

        # find all attributes (age, status, zodiac, etc)

        attr_array = soup.find_all("p", "attrgroup")
        for p in attr_array:
            for span in p.find_all("span"):
                if span.b is not None:  
                    value = span.b.extract().get_text()
                    key_label = span.get_text()
                    key = key_label[:-2].strip().lower()
                    if key not in COLUMNS:
                        print "!! CUSTOM ATTRIBUTE: " + key_label + " at " + page_url
                    else:
                        post[key] = value
    except Exception as e:
        print 'error at ' + page_url
        print e

    return post


# convert post object to an ordered list, which can be written to a csv as one row
def convert_to_row(post):
    values = [None] * len(COLUMNS)
    for key in post:
        col = COLUMNS.index(key)
        if col > -1 and post[key]: #ignore custom attributes and keys with null values
            values[col] = post[key].encode('utf8')
    return values

"""
get a post's 'category' (i.e. casual encounter, strictly platonic)
along with its type (i.e. m4m, w4mw)
"""
def get_category_and_type(section, title):
    # if in m4m/m4w/w4w/w4m, rename as "msr" (misc romance), and use the section as the search type
    if '4' in section:
        return ('msr', section)
    
    # otherwise, find the search type from the title string
    m = re.search(' - .*4*$', title)
    s_type = None
    if (m):
        s_type = m.group(0)[3:]
    return (section, s_type)

def main():

    # load location file containing craigslist urls for each city
    #file = open('locations.txt', 'r')

    rows_to_write = []

    for city in CITY_LINKS:
        city_url = city.strip('\n')
        city_name = city_url.split(".")[0]
        print "In city " + city_url

        # do a search for every ad type
        for section in PERSONALS_SECTIONS:
            print "searching " + section
            count = 0
            searchUrl = "http://" + city_url + "/search/" + section + "/?s=" + str(count)

            searchResults = parse_search_result_page(searchUrl, city_url)
            
            while len(searchResults) > 0:
                print "searching count " + str(count)
                # iterate thru search results and scrape each page
                for adUrl in searchResults:
                    # print "scraping " + adUrl
                    parsedPost = parse_page_result(adUrl)
                    # post may be null if it has been flagged for removal
                    if (parsedPost):
                        # add aditional info to post
                        parsedPost["url"] = adUrl
                        parsedPost["city"] = city_name
                        category,search_type = get_category_and_type(section, parsedPost["title"])
                        parsedPost["category"] = category
                        parsedPost["type"] = search_type

                        rows_to_write.append(convert_to_row(parsedPost))

                if FIRST_PAGE_ONLY:
                    break

                count += 100
                searchUrl = "http://" + city_url + "/search/" + section + "/?s=" + str(count)
                searchResults = parse_search_result_page(searchUrl, city_url)
    

    outputFile = open('results.csv', 'w')
    outputWriter = csv.writer(outputFile)

    # write header
    outputWriter.writerow(COLUMNS);

    # write all rows
    for row in rows_to_write:
        outputWriter.writerow(row)

    outputFile.close()

if __name__ == '__main__':
    main()

