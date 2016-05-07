import json
import sys
from collections import defaultdict

def main():
    jaccard_similarities = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(float))))
    
    with open(sys.argv[1]) as data_file:  
        data = json.load(data_file)
        
        for cluster1 in data:
            for cluster2 in data:
                jaccard_similarity = jaccard_similarity_score(cluster1['terms'], cluster2['terms'])
                jaccard_similarities[cluster1['city']][cluster1['cluster_name']][cluster2['city']][cluster2['cluster_name']] = jaccard_similarity
                
                # print cluster1['city'] + ', ' + cluster1['cluster_name']
                # print cluster2['city'] + ', ' + cluster2['cluster_name']
                # print jaccard_similarity
                # print
        
    num_cities = len(jaccard_similarities)
    
    love_to_sex_similarity_by_city = defaultdict(float)
    sex_to_love_similarity_by_city = defaultdict(float)
    love_to_love_similarity_by_city = defaultdict(float)
    sex_to_sex_similarity_by_city = defaultdict(float)
    
    for city1 in jaccard_similarities:
        cumulative_love_to_sex_similarity = 0.0
        cumulative_sex_to_love_similarity = 0.0
        cumulative_love_to_love_similarity = 0.0
        cumulative_sex_to_sex_similarity = 0.0
        
        for city2 in jaccard_similarities[city1]['love']:
            love_to_sex_similarity = jaccard_similarities[city1]['love'][city2]['sex']
            love_to_love_similarity = jaccard_similarities[city1]['love'][city2]['love']
            
            cumulative_love_to_sex_similarity += love_to_sex_similarity
            cumulative_love_to_love_similarity += love_to_love_similarity
        
        love_to_sex_similarity_by_city[city1] = cumulative_love_to_sex_similarity / num_cities
        sex_to_love_similarity_by_city[city1] = cumulative_sex_to_love_similarity / num_cities
        
        for city2 in jaccard_similarities[city1]['sex']:
            sex_to_sex_similarity = jaccard_similarities[city1]['sex'][city2]['sex']
            sex_to_love_similarity = jaccard_similarities[city1]['sex'][city2]['love']
            
            cumulative_sex_to_sex_similarity += sex_to_sex_similarity
            cumulative_sex_to_love_similarity += sex_to_love_similarity
        
        love_to_sex_similarity_by_city[city1] = cumulative_love_to_sex_similarity / num_cities
        sex_to_love_similarity_by_city[city1] = cumulative_sex_to_love_similarity / num_cities
        love_to_love_similarity_by_city[city1] = cumulative_love_to_love_similarity / num_cities
        sex_to_sex_similarity_by_city[city1] = cumulative_sex_to_sex_similarity / num_cities
    
    rescale(love_to_sex_similarity_by_city, False)
    rescale(sex_to_love_similarity_by_city, False)
    rescale(love_to_love_similarity_by_city, True)
    rescale(sex_to_sex_similarity_by_city, True)
    
    print 'how similar each city\'s love posts are to other cities\' sex posts'
    for city in sorted(love_to_sex_similarity_by_city, key=love_to_sex_similarity_by_city.get, reverse=True):
        print city, love_to_sex_similarity_by_city[city]

    print
    
    print 'how similar each city\'s sex posts are to other cities\' love posts'
    for city in sorted(sex_to_love_similarity_by_city, key=sex_to_love_similarity_by_city.get, reverse=True):
        print city, sex_to_love_similarity_by_city[city]
    
    print
    
    print 'uniqueness of each city\'s sex posts'
    for city in sorted(sex_to_sex_similarity_by_city, key=sex_to_sex_similarity_by_city.get, reverse=True):
        print city, sex_to_sex_similarity_by_city[city]
    
    print
    
    print 'uniqueness of each city\'s love posts'
    for city in sorted(love_to_love_similarity_by_city, key=love_to_love_similarity_by_city.get, reverse=True):
        print city, love_to_love_similarity_by_city[city]

def rescale(dictionary_by_city, invert):
    min = 1.0
    max = 0.0
    
    scale_min = float(sys.argv[2])
    scale_max = float(sys.argv[3])
    
    for city in dictionary_by_city:
        if dictionary_by_city[city] > max:
            max = dictionary_by_city[city]
        
        if dictionary_by_city[city] < min:
            min = dictionary_by_city[city]
    
    scaling_factor = (scale_max - scale_min) / (max - min)
    
    for city in dictionary_by_city:
        dictionary_by_city[city] = scale_min + (dictionary_by_city[city] - min) * scaling_factor
        
        if invert:
            dictionary_by_city[city] = scale_max - dictionary_by_city[city] + scale_min
        
def jaccard_similarity_score(cluster1, cluster2):
    set1 = set(cluster1)
    set2 = set(cluster2)
    
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    
    return float(len(intersection)) / len(union)

if __name__ == '__main__':
	main()