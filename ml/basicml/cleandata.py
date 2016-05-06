#!/usr/bin/env python
import sys
import csv
import os

def typeToNum(t):
    if (t=='m4m'):
        return 1
    elif (t=='m4w'):
        return 2
    elif (t=='msr'):
        return 3


def main():

    typedict = {}
    typeindex = 0
    bodydict = {}
    bodyindex = 0
    statusdict = {}
    statusindex = 0

    with open ('cleanresults.csv', 'wb') as w:
        for location in os.listdir('../../results'):
            for filename in os.listdir('../../results/'+location):
                if filename[-4:]=='.csv':
                    with open('../../results/'+location+'/'+filename) as r:
                        reader = csv.reader(r)
                        writer = csv.writer(w)
                        for row in reader:
                            #type, title, text, age, body, height, status
                            #[row[6], row[7], row[8], row[9], row[10], row[22], row[36]]
                            if (len(row[9]) < 4) and (row[36]!='') and (row[6]!='') and (row[7]!='') and (row[8]!='') and (row[9]!='') and (row[10]!='') and (row[22]!='') and (row[6]!='type'):
                                
                                t = row[6].lower()
                                if t not in typedict.keys():
                                    typedict[t] = typeindex
                                    typeindex = typeindex + 1
                                
                                body = row[10].lower()
                                if body not in bodydict.keys():
                                    bodydict[body] = bodyindex
                                    bodyindex = bodyindex + 1

                                status = row[36].lower()
                                if status not in statusdict.keys():
                                    statusdict[status] = statusindex
                                    statusindex = statusindex + 1

                                writer.writerow([t, len(row[7]), len(row[8]), row[9], body, row[22][-6:-3], status])
    print typedict
    print bodydict
    print statusdict

    with open ('cleanresults0.csv', 'wb') as w:
        writer = csv.writer(w)
        with open ('cleanresults.csv') as r:
            reader = csv.reader(r)
            for row in reader:
                writer.writerow([typedict[row[0]], row[1], row[2], row[3], bodydict[row[4]], row[5], statusdict[row[6]]])



if __name__ == '__main__':
    main()