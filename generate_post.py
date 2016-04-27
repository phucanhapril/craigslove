import string
import sys
import argparse
import csv
import scipy
import scipy.stats
from scipy.stats import rv_discrete
from collections import defaultdict

locations = ['chicago', 'dallas', 'denver', 'jacksonville', 'lasvegas', 'losangeles', 'miami', 'minneapolis', 'newyork', 'oklahomacity', 'providence', 'seattle', 'sfbay', 'washingtondc']
posttype = ['m4m', 'm4w', 'msr', 'stp', 'w4m', 'w4w']

def main():
    for location in locations:
        with open('results/' + location + '/m4m.csv') as f:
            reader = csv.reader(f)
            entries = []
            
            for row in reader:
                entry = row[8]
                entries.append(entry)
            
            transition_matrix = calculate_transition_matrix(entries)
            sampling_mechanism = defaultdict(lambda: None)
            
            for w in transition_matrix:
                xk = []
                pk = []
                
                for w_prime in transition_matrix:
                    xk.append(w_prime)
                    pk.append(transition_matrix[w][w_prime])
            
                sampling_mechanism[w] = rv_discrete(values=(xk, pk))
            
            prev_word = None
            next_word = '*START*'
            generated_post = ''
            
            while next_word is not '*END*':
                prev_word = next_word
                next_word = sampling_mechanism[prev_word].rvs()
                
                generated_post += next_word
            
            print generated_post
            
def tokenize(words):
    i = 0
    
    while i < len(words):
        if len(words[i]) > 1 and words[i][-1] in string.punctuation:
            words[i] = words[i][:-1]
            words.insert(i + 1, words[i][-1])
            
        index += 1
    
    return words


def calculate_transition_matrix(training_data): # training_data is a list of strings
    transition_matrix = defaultdict(lambda: defaultdict(float))
    
    for post in training_data.split('\n'):
        words = tokenize(post.lower().split())
        
        transition_matrix['*START*'][words[0]] += 1.0
        
        for i in len(words) - 1:
            transition_matrix[words[i]][words[i + 1]] += 1.0
        
        transition_matrix[words[len(words)]]['*END*'] += 1.0
    
    for w in transition_matrix:
        unigram_count = 0
        
        for w_prime in transition_matrix[w]:
            unigram_count += transition_matrix[w][w_prime]
        
        for w_prime in transition_matrix[w]:
            transition_matrix[w][w_prime] = transition_matrix[w][w_prime] / unigram_count
    
    return transition_matrix

if __name__ == "__main__":
    main()