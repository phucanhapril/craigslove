#!/usr/bin/env python
import sys
import csv
import os

def main():

    typedict = {}
    typeindex = 0
    bodydict = {}
    bodyindex = 0
    statusdict = {}
    statusindex = 0


    for location in os.listdir('../results'):
        for filename in os.listdir('../results/'+location):
            if filename[-4:]=='.csv':
                with open('../results/'+location+'/'+filename) as r:
                    reader = csv.reader(r)

                    next(reader)
                    for row in reader:
                        t = row[6].lower()
                        with open (t+'age.csv', 'a') as w:
                            with open (t+'height.csv', 'a') as w1:
                                agewriter = csv.writer(w)
                                heightwriter = csv.writer(w1)

                                if (row[9] != '') and ((len(row[9]) < 3) or (len(row[9]) == 3 and row[9][0]==1)):
                                    agewriter.writerow([row[9]])
                                if (row[22] != ''):
                                    feetinches = row[22].split('"')[0].strip().split('\'')
                                    feet = int(feetinches[0])
                                    inches = int(feetinches[1])
                                    heightwriter.writerow([feet*12+inches])
                                            

if __name__ == '__main__':
    main()