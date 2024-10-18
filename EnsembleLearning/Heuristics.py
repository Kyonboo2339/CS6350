import math

def informationGain(labelProportions):
    p_sum = 0
    weightsum = 0
    #Must support weighting
    
    for label in labelProportions:
        p = labelProportions[label]
        weightsum += p
        if p > 0:
            #print("p_result: " + str(-1*p*math.log(p, 2)))
            p_sum += p*math.log(p, 2)

    #print("P_sum:  " + str(-1*p_sum))

    
    return -1*p_sum


def giniIndex(labelProportions):
    p_sum = 0
    for label in labelProportions:   
        p_sum += labelProportions[label]**2

    return 1 - p_sum

def majorityError(labelProportions):
    majorityPercent = float("-inf")
    for label in labelProportions:
        majorityPercent = max(majorityPercent, labelProportions[label])
    if majorityPercent < 0:
        return 0
    return 1 - majorityPercent

