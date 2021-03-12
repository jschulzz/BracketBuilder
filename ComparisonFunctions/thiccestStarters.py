from statistics import mean

from ComparisonFunctions.CompareFunction import CompareFunction
from ComparisonFunctions.utils import getStarters


def compareTeams(t1, t2, data):
    starters1 = getStarters(data[t1]["players"])
    starters2 = getStarters(data[t2]["players"])
    weights1 = list(map(lambda x: x["weight"], starters1))
    weights2 = list(map(lambda x: x["weight"], starters2))
    t1_score = mean(weights1)
    t2_score = mean(weights2)
    odds = max(t1_score / (t1_score + t2_score), t2_score / (t1_score + t2_score))
    return t1_score, t2_score, odds


comparison = CompareFunction(wantHighest=True, comparison=compareTeams)
