#!/usr/bin/env python
import sys
import csv
import string
import operator
from string import punctuation

def main():

    mostFrequentWords = {}

    with open('posts/newyork/m4w.csv', 'r') as m4wListings:
        m4wreader = csv.reader(m4wListings)
        for row in m4wreader:
            for column in row:
                words = column.split()
                for word in words:
                    word.strip()
                    word.lower()

                    if (word in mostFrequentWords.keys()):
                        mostFrequentWords[word] = mostFrequentWords[word] + 1
                    else:
                        mostFrequentWords[word] = 1
                    # print mostFrequentWords[word], word

    sorted_mostFrequent = sorted(mostFrequentWords.items(), key=operator.itemgetter(1), reverse=True)
    printnum = 0;

    with open('posts/newyork/mostFrequentWordsm4w.txt', 'w') as writer:
        while printnum < 100:
            writer.write(sorted_mostFrequent[printnum][0]+", "+str(sorted_mostFrequent[printnum][1])+ '\n')
            printnum = printnum + 1
        pass
        writer.close()

if __name__ == '__main__':
    main()