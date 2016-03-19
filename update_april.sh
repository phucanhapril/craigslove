#!/bin/bash
git pull
python craigslove.py oklahomacity.craigslist.org
python craigslove.py chicago.craigslist.org
python craigslove.py lasvegas.craigslist.org
python craigslove.py losangeles.craigslist.org
git commit -am 'Update OKCity, Chitown, Vegas, LA'
git push
