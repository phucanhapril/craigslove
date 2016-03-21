from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import datetime
import csv
import sys
import os
import re
import logging
import json
import time

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

"""
to run:

python craigslove.py <url from below>

newyork.craigslist.org
sfbay.craigslist.org
providence.craigslist.org
miami.craigslist.org
denver.craigslist.org
dallas.craigslist.org

"""

# Flag for scraping only first page of search results for each query (to not overwhelm craigslist when testing)
FIRST_PAGE_ONLY = False

DELAY = True

DATE_FORMAT = '%Y-%m-%d %H:%M'
COLUMNS = [
    # required
    'url',
    'city', # need?
    'subcity',
    'datetime_created',
    'datetime_updated',
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

PERSONALS_SECTIONS = [ 'm4m', 'm4w', 'stp', 'w4w', 'w4m', 'msr' ]

# global vars
city_base_url = '' # passed in as arg
city_name = ''
query = '' # the current personal section being scraped

# get a list of URLs from a personals search result
def parse_search_result_page(page):
    search_url = 'http://{}/search/{}/?s={}'.format(city_base_url, query, page)
    try:
        soup = BeautifulSoup(urlopen(search_url).read(), 'lxml')
    except Exception as e:
        logging.error('%s (%s)', e, search_url)
        return []

    rows = soup.find('div', 'content').find_all('p', 'row')

    postings_list = []
    for row in rows:
        
        """
        skip url if href starts with "//" to avoid double counting
        because it means they're linking to a "nearby city"
        """
        postinghref = row.a['href'] 
        if not postinghref.startswith('//') and not postinghref.startswith('http') :
            url = 'http://{}{}'.format(city_base_url, postinghref)
            dtime = row.find('time')['datetime']
            posting_link = {}
            posting_link['url'] = url
            posting_link['datetime_updated'] = dtime # %Y-%m-%d %H:%M
            postings_list.append(posting_link)
    return postings_list


# parse text and relevant attributes from a personal ad
def parse_page_result(page_url):
    try:
       soup = BeautifulSoup(urlopen(page_url).read(), 'lxml')
    except Exception as e:
        logging.error('%s (%s)', e, page_url)
        return

    # the post object represents the single personal ad on this page
    post = {}

    # wrap the whole thing in a try-except because at any point the post may be marked for removal
    try:
        # get title
        post['title'] = soup.title.get_text()

        # get text body
        post['text'] = soup.find(id='postingbody').get_text()

        # get time (time it was *posted* -- not the last updated time)
        posted_time = soup.find('time', class_='timeago')['datetime']
        # convert from '2016-02-01T10:54:36-0500' to '2016-02-01 10:54'
        post['datetime_created'] = posted_time[:-8].replace('T', ' ')

        # find all attributes (age, status, zodiac, etc)

        attr_array = soup.find_all('p', 'attrgroup')
        for p in attr_array:
            for span in p.find_all('span'):
                if span.b is not None:  
                    value = span.b.extract().get_text()
                    key_label = span.get_text()
                    key = key_label[:-2].strip().lower()
                    if key in COLUMNS: #ignore custom attributes
                        post[key] = value
    except Exception as e:
        logging.warning(e)
        return None # skip this post altogether

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
    # if in m4m/m4w/w4w/w4m, rename as 'msr' (misc romance), and use the section as the search type
    if '4' in section:
        return ('msr', section)
    
    # otherwise, find the search type from the title string
    m = re.search(' - ..?4..?$', title)
    s_type = None
    if (m):
        s_type = m.group(0)[3:]
    return (section, s_type)



# get the datetime of the last post we've saved for this query
def get_last_post_datetime():
    logging.info('   getting last time for %s %s', city_name, query)
    readpath = 'results/{}/datetime_last_saved_posts.json'.format(city_name)
    directory_path = 'results/{}'.format(city_name)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    mode = 'r' if os.path.exists(readpath) else 'w+'
    with open(readpath, mode) as f:
        try: 
            data = json.load(f)
        except ValueError as e:
            logging.info(e) 
            data = {}
    return data.get(query) # returns None if the key doesn't exist

def save_time(dtime):
    logging.info('   updating last time for %s %s to %s', city_name, query, dtime)
    path = 'results/{}/datetime_last_saved_posts.json'.format(city_name)
    with open(path, 'r+') as f:
        try: 
             data = json.load(f)
        except ValueError: 
             data = {}

    data[query] = dtime.strftime(DATE_FORMAT)

    with open(path, 'w') as f:
        json.dump(data, f)

# scrape this city's personal page for this query UNTIL you hit a post past
# the 'datetime_most_recent' (means we've already stored it)
def scrape(datetime_most_recent):
    logging.info('   scraping %s %s until hitting %s', city_name, query, datetime_most_recent)
    page = 0
    

    search_results = parse_search_result_page(page)
    if len(search_results) < 0:
        logging.info('   no search results for %s %s', city_name, query)
        return

    posts_to_write = []

    last_saved_d = None
    if (datetime_most_recent): # if we have a most recent time from the file
        last_saved_d = datetime.strptime(datetime_most_recent, DATE_FORMAT)

    smallest_post_date = None
    while len(search_results) > 0:
        logging.info('   scraping %s results from page %s', len(search_results), page/100 + 1)
        
        # iterate thru search results and scrape each page
        reached_datetime = False
        for posting_link in search_results:
            post_url = posting_link['url']
            post_d = datetime.strptime(posting_link['datetime_updated'], DATE_FORMAT)
            if datetime_most_recent and post_d <= last_saved_d:
                reached_datetime = True
                logging.info('   reached datetime %s at %s', datetime_most_recent, post_url)
                break

            parsedPost = parse_page_result(post_url)
            if DELAY:
                time.sleep(1)
            # post may be null if it has been flagged for removal
            if (parsedPost):
                # add aditional info to post
                parsedPost['url'] = post_url
                parsedPost['city'] = city_name
                parsedPost['datetime_updated'] = posting_link['datetime_updated']
                parsedPost['subcity'] = get_subcity(post_url)
                category,search_type = get_category_and_type(query, parsedPost['title'])
                # remove ' - m4m' from end of title
                parsedPost['title'] = re.sub(' - ..?4..?$', '', parsedPost['title'])
                parsedPost['category'] = category
                parsedPost['type'] = search_type
                
                posts_to_write.append(parsedPost)
                
                if smallest_post_date is None:
                    smallest_post_date = post_d

        # don't go on to the next page if reached most recently saved datetime
        if FIRST_PAGE_ONLY or reached_datetime:
            break

        page += 100
        search_results = parse_search_result_page(page)
        if DELAY:
            time.sleep(1)


    # save the most recent post date
    if smallest_post_date:
        save_time(smallest_post_date)

    return posts_to_write


# get the subcity, like 'brk' in 'http://newyork.craigslist.org/brk/stp/'
def get_subcity(url):
    remove_http = re.sub('https?:\/\/', '', url)
    split = remove_http.split('/')
    if len(split) > 3:
        return split[1]
    return None

def main():
    if len(sys.argv) < 2:
        print 'Usage: python craigslove.py providence.craigslist.org'
        return

    if len(sys.argv[1].split('.')) != 3:
        print 'error in city url'
        return

    global city_base_url
    global city_name
    global query
    
    city_base_url = sys.argv[1]
    city_name = city_base_url.split('.')[0] #global

    for q in PERSONALS_SECTIONS:
        logging.info('*** beginning scrape of %s in %s ***', q, city_name)

        query = q # set global var

        datetime_most_recent = get_last_post_datetime()
        if datetime_most_recent is not None:
            logging.info('   read most recent time to be %s', datetime_most_recent)

        # scrape all posts from this query in this city
        posts_to_write = scrape(datetime_most_recent)
        
        if len(posts_to_write) < 1:
            logging.info(' >>> No posts to save for %s in %s <<<', query, city_name)
        else:
            # write results
            
            directory_path = 'results/{}'.format(city_name)
            result_path = 'results/{}/{}.csv'.format(city_name, query)

            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

            # if not a file yet, add column labels
            add_labels = False
            if not os.path.isfile(result_path):
                add_labels = True

            # open file for appending
            with open(result_path, 'ab') as f:
                outputWriter = csv.writer(f)
                if add_labels:
                    logging.info('   created a new file for %s in %s', query, city_name)
                    outputWriter.writerow(COLUMNS)

                # write all rows
                for p in posts_to_write:
                    outputWriter.writerow(convert_to_row(p))
                logging.info(' >>> SAVED: %s posts for %s in %s <<<', len(posts_to_write), query, city_name)

if __name__ == '__main__':
    main()

