from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import datetime
import csv
import sys
import os
import smtplib
import config

# Craigslist search URL
BASE_URL = ('http://providence.craigslist.org/search/'
            '?sort=rel&areaID=11&subAreaID=&query={0}&catAbb=sss')



TEST_URL = ('http://providence.craigslist.org/w4m/5434907516.html')

CSV = []
page = []
CONDITION = "condition:"
MEDIA_TYPE = "media:"



PROV_URL = ("http://providence.craigslist.org/search/stp")
PROV_URL1 = ("http://providence.craigslist.org/search/w4w")
PROV_URL2 = ("http://providence.craigslist.org/search/w4m")
PROV_URL3 = ("http://providence.craigslist.org/search/m4w")
PROV_URL4 = ("http://providence.craigslist.org/search/m4m")
PROV_URL5 = ("http://providence.craigslist.org/search/msr")
PROV_URL6 = ("http://providence.craigslist.org/search/cas")
PROV_URL7 = ("http://providence.craigslist.org/search/mis")
PROV_URL8 = ("http://providence.craigslist.org/search/rnr")



def parse_search_result_page(search_term, URL_LINKER):
    results = []
    search_term = search_term.strip().replace(' ', '+')
    search_url = URL_LINKER.format(search_term)
    soup = BeautifulSoup(urlopen(search_url).read())
    rows = soup.find('div', 'content').find_all('p', 'row')
    for row in rows:
        if row.a['href'].startswith("//"):
            url = "http:" + row.a['href']
        else:     
            url = 'http://providence.craigslist.org' + row.a['href']
        # price = row.find('span', class_='price').get_text()
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
    ##print "hello"
    ##rows = soup.find_all("p", class_="attrgroup")

    result_array = soup.find_all("p", "attrgroup")
    post = {}
    ##post["id"] = soup.find("p", class = "postinginfo").find
    post["title"] = soup.title.get_text()
    post["text"] = soup.find(id="postingbody").get_text()
    # post.title = 
    for p in result_array:
        for span in p.find_all("span"):
           #  print span 
            if span.b is None:  
                continue           
            value = span.b.extract().get_text()
            key = span.string

            post[key] = value
    print post
    write_results_Page(post)
    print page



def write_results_Page(page):

    mappings = { "title": 0,  "text": 1, "age: ": 2, "status : ": 3, "body : ": 4,"zodiac : ": 5, "diet : ": 6, "facial hair : ": 8, "drinks : ": 9, "eye color : ": 10, "religion : ": 11 }
    print page #{u'body : ': u'average', u'age: ': u'33'}
    valueList = [None] * 20
    for key in page:
        #print key
        if key in mappings:
            index = mappings[key]
            #print index
            valueList[index] = page[key]
    # csv.writeRow(valueList)


    
    try:
        outputWriter.writerow(valueList)
    except UnicodeEncodeError:
        pass



# def write_results(results):
#     """Writes list of dictionaries to file."""
#     fields = results[0].keys()
#     with open('results.csv', 'w') as f:
#         dw = csv.DictWriter(f, fieldnames=fields, delimiter=', ')
#         dw.writer.writerow(dw.fieldnames)
#         dw.writerows(results)






def get_current_time():
    return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

    

if __name__ == '__main__':
    outputFile = open('results.csv', 'w')
    outputWriter = csv.writer(outputFile)
    outputWriter.writerow(["title: ",  "text: ", "age: ", "status : ", "body : ","zodiac : ", "body art : ", "diet : ", "facial hair : ", "drinks : ","height : ", "eye color : ", "religion : "])
    
    try:
        TERM = sys.argv[1]
    except:
        print "You need to include a search term and a 10-digit phone number!\n"
        sys.exit(1)


    
    results = parse_search_result_page(TERM, PROV_URL)
    for i in results:
         # print type(i['url'])
        print i['url']
        ##print "hello"
        parse_page_result(i['url'])
        


    results = parse_search_result_page(TERM, PROV_URL1)
    for i in results:
         # print type(i['url'])
        print i['url']
        ##print "hello"
        parse_page_result(i['url'])


    results = parse_search_result_page(TERM, PROV_URL2)
    for i in results:
         # print type(i['url'])
        print i['url']
        ##print "hello"
        parse_page_result(i['url'])



    results = parse_search_result_page(TERM, PROV_URL3)
    for i in results:
         # print type(i['url'])
        print i['url']
        ##print "hello"
        parse_page_result(i['url'])


    results = parse_search_result_page(TERM, PROV_URL4)
    for i in results:
         # print type(i['url'])
        print i['url']
        ##print "hello"
        parse_page_result(i['url'])

    results = parse_search_result_page(TERM, PROV_URL5)
    for i in results:
         # print type(i['url'])
        print i['url']
        ##print "hello"
        parse_page_result(i['url'])



    results = parse_search_result_page(TERM, PROV_URL6)
    for i in results:
         # print type(i['url'])
        print i['url']
        ##print "hello"
        parse_page_result(i['url'])


    results = parse_search_result_page(TERM, PROV_URL7)
    for i in results:
         # print type(i['url'])
        print i['url']
        ##print "hello"
        parse_page_result(i['url'])

    results = parse_search_result_page(TERM, PROV_URL8)
    for i in results:
         # print type(i['url'])
        print i['url']
        ##print "hello"
        parse_page_result(i['url'])




    
    outputFile.close()




## Now we access each link in the result and

