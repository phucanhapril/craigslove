## Craigslove: Love in the Time of Craigslist
http://phucanhapril.github.io/craigslove/  
  
## craigslist web scraper
__`python craigslove_scraper.py <base url>`__  

where the base url is newyork.craigslist.org, or sfbay.craigslist.org, etc.  

This will scrape personals from Strictly Platonic (stp), Miscellaneous Romance (msr), w4w, w4m, m4w, and m4m.  

Posts are saved to `posts/<city>/<query>.csv` (for example: `results/providence/w4w.csv`)  

##### setup (mac instructions)
install Python 2.7 and pip  
```
sudo pip install BeautifulSoup4  
brew install libxml2
pip install lxml (if that doesn’t work try this first: 'xcode-select --install')  
```

## k-means clustering
##### ml/clustering/cluster.py
*instructions for running within the ml/clustering directory:*  
  
__`python cluster.py -path data/city/sample -c 2 -plot True`__  
  
This will perform 2-means clustering on each csv file in __`data/city/sample`__.  
The resulting clusters in json format are saved to __`cluster_data/`__.  
It will also create 2-dimensional scatter plots representing the clusters, saved to __`cluster_plot/`__.  
  
note: __`ml/clustering/data/`__ is populated from the original raw __`posts/`__ by running __`ml/clustering/util/format_posts_for_clustering.py`__.  
  
##### CODE REFERENCED: http://brandonrose.org/clustering  
