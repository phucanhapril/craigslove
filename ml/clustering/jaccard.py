import json
import sys

def main():
    with open(sys.argv[1]) as data_file:  
        data = json.load(data_file)
        
        for cluster1 in data:
            for cluster2 in data:
                print cluster1['city'] + ', ' + cluster1['cluster_name']
                print cluster2['city'] + ', ' + cluster2['cluster_name']
                print jaccard_similarity_score(cluster1['terms'], cluster2['terms'])
                print

def jaccard_similarity_score(cluster1, cluster2):
    set1 = set(cluster1)
    set2 = set(cluster2)
    
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    
    return float(len(intersection)) / len(union)

if __name__ == '__main__':
	main()