import sys
import collections
import Queue

AGE_PARAMETER = 0
GENDER_PARAMETER = 1

PARAMATER_OFFSET = -1 # correct once we know structure of data
NUM_PARAMETERS = 2

AGE_RANGE = range(100)
GENDER_RANGE = range(3) # 0 = M, 1 = F, 2 = T

NONE_TOLERANCE = 0

def conditionalProbability(A, B, data):
    countAandB = 0
    countB = 0
    
    potentiallyB = true
    potentiallyAandB = true
    
    for row in data:
        for i in range(NUM_PARAMETERS):
            if B[i] is not None and row[i + PARAMATER_OFFSET] != B[i]:
                potentiallyB = false
                    
                if A[i] is not None and row[i + PARAMATER_OFFSET] != A[i]:
                    potentiallyAandB = false
        
        if potentiallyB:
            countB += 1
            
        if potentiallyAandB:
            countAandB += 1
            
    return float(countAandB) / countB
            
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