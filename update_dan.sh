#!/bin/bash
git pull
python craigslove.py dallas.craigslist.org
python craigslove.py denver.craigslist.org
python craigslove.py miami.craigslist.org
python craigslove.py providence.craigslist.org
git add .
git commit . -m "Dallas, Denver, Miami, Providence"
git pull
git push