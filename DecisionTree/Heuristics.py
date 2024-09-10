import math

def informationGain(labelProportions):
    p_sum = 0
    for label in labelProportions:
        p = labelProportions[label]
        if p > 0:
            p_sum += p*math.log(p, 2)

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

    return 1 - majorityPercent

