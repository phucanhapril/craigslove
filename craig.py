from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import datetime
import csv
import sys
import os
import smtplib
import config

# Craigslist search URL
BASE_URL = ('http://chicago.craigslist.org/search/'
            '?sort=rel&areaID=11&subAreaID=&query={0}&catAbb=sss')

def parse_results(search_term):
    results = []
    search_term = search_term.strip().replace(' ', '+')
    search_url = BASE_URL.format(search_term)
    soup = BeautifulSoup(urlopen(search_url).read())
    rows = soup.find('div', 'content').find_all('p', 'row')
    for row in rows:
        url = 'http://chicago.craigslist.org' + row.a['href']
        # price = row.find('span', class_='price').get_text()
        create_date = row.find('time').get('datetime')
        title = row.find_all('a')[1].get_text()
        results.append({'url': url, 'create_date': create_date, 'title': title})
    return results


def write_results(results):
    """Writes list of dictionaries to file."""
    fields = results[0].keys()
    with open('results.csv', 'w') as f:
        dw = csv.DictWriter(f, fieldnames=fields, delimiter='|')
        dw.writer.writerow(dw.fieldnames)
        dw.writerows(results)



def get_current_time():
    return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')



    
    results = parse_results(TERM)
    ## This will save the 
    ##write_results(results) 
    
    ##print results
    ##print results

    ##print first results's url
    print results[1]['url']




## Now we access each link in the result and

