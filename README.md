# Love in the Time of Craigslist
## A Tale of Five Cities
In an ever-increasingly digital world, how has the human quest for love changed? In our project Craigslove, we try to answer this question, and more.
  
midterm report http://april1452.github.io/craigslove/  
preliminary findings visualized http://april1452.github.io/craigslove/viz/  

##How to run 
__`python craigslove.py <base url>`__  

the url should be a base url in this form:  
*   newyork.craigslist.org
*   sfbay.craigslist.org
*   providence.craigslist.org

This will scrape personals from Strictly Platonic (stp), Miscellaneous Romance (msr), w4w, w4m, m4w, and m4m.

Output is saved in 'results/city/query.csv' (for example: 'results/providence/w4w.csv')

##Setup (mac instructions)
install Python 2.7 and pip  
'sudo pip install BeautifulSoup4'  
'brew install libxml2'  
'pip install lxml' (if that doesn’t work try this first: 'xcode-select --install')  
