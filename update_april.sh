#!/bin/bash
git pull
python craigslove.py oklahomacity.craigslist.org
python remove_duplicates.py results/oklahomacity
python craigslove.py chicago.craigslist.org
python remove_duplicates.py results/chicago
python craigslove.py lasvegas.craigslist.org
python remove_duplicates.py results/lasvegas
python craigslove.py losangeles.craigslist.org
python remove_duplicates.py results/losangeles
git commit -am 'Update OKCity, Chitown, Vegas, LA'
git push
