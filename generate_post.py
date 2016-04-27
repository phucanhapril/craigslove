import string
import sys
import argparse
import csv
import random
# import scipy
# import scipy.stats
# from scipy.stats import rv_discrete
from collections import defaultdict

# locations = ['chicago', 'dallas', 'denver', 'jacksonville', 'lasvegas', 'losangeles', 'miami', 'minneapolis', 'newyork', 'oklahomacity', 'providence', 'seattle', 'sfbay', 'washingtondc']
locations = ['providence']
posttype = ['m4m', 'm4w', 'msr', 'stp', 'w4m', 'w4w']

def main():
    for location in locations:
        with open('results/' + location + '/w4w.csv') as f:
            reader = csv.reader(f)
            entries = []
            
            for row in reader:
                entry = row[8]
                entries.append(entry)
            
            transition_matrix = calculate_transition_matrix(entries)
            # sampling_mechanism = defaultdict(lambda: None)
            
            # for w in transition_matrix:
                # xk = []
                # pk = []
                
                # for w_prime in transition_matrix:
                    # xk.append(w_prime)
                    # pk.append(transition_matrix[w][w_prime])
            
                # sampling_mechanism[w] = rv_discrete(values=(xk, pk))
            
            prev_word = None
            next_word = '*START*'
            generated_post = ''
            
            while next_word != '*END*':
                prev_word = next_word
                random_probability = random.random() # between 0 and 1
                cumulative_probability = 0.0
                
                # next_word = sampling_mechanism[prev_word].rvs()
                
                for w_prime in transition_matrix[prev_word]:
                    cumulative_probability += transition_matrix[prev_word][w_prime]
                    
                    if cumulative_probability > random_probability:
                        next_word = w_prime
                        break
                
                if len(next_word) > 1 or next_word in (string.punctuation + 'i' + 'a'):
                    generated_post += next_word + ' '
            
            print generated_post[:-7]
            
def tokenize(words):
    index = 0
    
    while index < len(words):
        if len(words[index]) > 1 and words[index][-1] in string.punctuation:
            words[index] = words[index][:-1]
            words.insert(index + 1, words[index][-1])
            
        index += 1
    
    return words


def calculate_transition_matrix(training_data): # training_data is a list of strings
    transition_matrix = defaultdict(lambda: defaultdict(float))
    
    for post in training_data:
        words = tokenize(post.lower().split())
        
        transition_matrix['*START*'][words[0]] += 1.0
        
        for i in range(len(words) - 1):
            transition_matrix[words[i]][words[i + 1]] += 1.0
        
        transition_matrix[words[len(words) - 1]]['*END*'] += 1.0
    
    for w in transition_matrix:
        unigram_count = 0
        
        for w_prime in transition_matrix[w]:
            unigram_count += transition_matrix[w][w_prime]
        
        for w_prime in transition_matrix[w]:
            transition_matrix[w][w_prime] = transition_matrix[w][w_prime] / unigram_count
    
    return transition_matrix

if __name__ == "__main__":
    main()