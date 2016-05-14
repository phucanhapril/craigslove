import sys
import collections
import Queue
import csv

AGE_PARAMETER = 2
GENDER_PARAMETER = -1 # modify

PARAMATER_OFFSET = 0 # modify according to structure of data
NUM_PARAMETERS = 9

AGE_RANGE = range(100)
GENDER_RANGE = range(3) # 0 = M, 1 = F, 2 = T

NONE_TOLERANCE = 0

CSV_PATH = 'results.csv'

def conditionalProbability(A, B, pathToData):
    with open(pathToData, 'rb') as data:
        reader = csv.reader(data)

        countAandB = 0
        countB = 0

        for row in reader:
            # print row
            potentiallyB = True
            potentiallyAandB = True
            
            for i in range(NUM_PARAMETERS):
                # print str(A[i]) + ', ' + str(B[i]) + ', ' + row[i + PARAMATER_OFFSET]
                
                if A[i] is not None and row[i + PARAMATER_OFFSET] != A[i]:
                    # print "potentiallyAandB is false"
                    potentiallyAandB = False
                    
                if B[i] is not None and row[i + PARAMATER_OFFSET] != B[i]:
                    # print "potentiallyAandB is false"
                    # print "potentiallyB is false"
                    potentiallyAandB = False
                    potentiallyB = False
            
            if potentiallyB:
                countB += 1
                
            if potentiallyAandB:
                countAandB += 1
        
        # print countAandB
        # print countB
        
        if countB > 0:
            return float(countAandB) / countB
        else:
            return -1
            
def howManyNonesInTuple(tuple):
    noneCount = 0
    
    for element in tuple:
        if element is None:
            noneCount += 1
    
    return noneCount

def whoIsLookingForLove():
    loveDemographics = {}
    
    for age in AGE_RANGE:
        for gender in GENDER_RANGE:
            if (age, gender) in loveDemographics:
                loveDemographics[(age, gender)] = loveDemographics[(age, gender)] + len(lookingForLove(age, gender))
            else:
                loveDemographics[(age, gender)] = len(lookingForLove(age, gender))
    
    priorityQueue = Queue.PriorityQueue()
    
    for key, value in loveDemographics:
        priorityQueue.put(-value, key)
    
    while (not priorityQueue.Empty):
        priority, tuple = priorityQueue.get()
        
        if howManyNonesInTuple(tuple) <= NONE_TOLERANCE:
            return tuple

def doYouGrowOutOfFootFetishism():
    footFetishesIn20s = 0
    footFetishesIn30s = 0
    
    for posting in data:
        if posting.hasFootFetish():
            age = posting.getAge();
            
            if 20 <= age and age < 30:
                footFetishesIn20s += 1
            elif 30 <= age and age < 40:
                footFetishesIn30s += 1
    
    print footFetishesIn20s
    print footFetishesIn30s
    
    return footFetishesIn20s > footFetishesIn30s

def getAge():
    print "not implemented"
    # figure out later how to fill these in
    
def hasFootFetish():
    print "not implemented"

def lookingForLove(age, gender):
    print "not implemented"

def priorityQueueTest():
    q = Queue.PriorityQueue()
    q.put((10,'red'))
    q.put((1,'green'))
    q.put((2,'green'))
    q.put((5,'blue'))
    
    print q.get()

def argmax(func):
    for age in AGE_RANGE:
        for gender in GENDER_RANGE:
            print func(age - 1, gender)
            print func(age, gender)
            print func(age + 1, gender)
            # get the derivative of func evaluated at (age, gender)
            
print(conditionalProbability([None, None, None, 'single', None, None, None, None, None], [None, None, None, None, 'average', None, None, None, None], CSV_PATH))
print(conditionalProbability([None, None, None, 'single', None, None, None, None, None], [None, None, None, None, 'curvy', None, None, None, None], CSV_PATH))

print(conditionalProbability([None, None, None, 'single', None, None, None, None, None], [None, None, None, None, None, None, None, None, ''], CSV_PATH))
print(conditionalProbability([None, None, None, 'single', None, None, None, None, None], [None, None, None, None, None, None, None, None, 'Tattoo\'s'], CSV_PATH))