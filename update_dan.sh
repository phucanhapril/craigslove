#!/bin/bash
git pull
python craigslove.py dallas.craigslist.org
python remove_duplicates.py results/dallas
python craigslove.py denver.craigslist.org
python remove_duplicates.py results/denver
python craigslove.py miami.craigslist.org
python remove_duplicates.py results/miami
python craigslove.py providence.craigslist.org
python remove_duplicates.py results/providence
git add .
git commit . -m "Dallas, Denver, Miami, Providence"
git pull
git push