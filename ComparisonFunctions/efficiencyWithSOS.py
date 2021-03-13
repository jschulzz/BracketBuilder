from statistics import mean

from ComparisonFunctions.CompareFunction import CompareFunction
from ComparisonFunctions.utils import getStarters


def compareTeams(t1, t2, data):
    off1 = data[t1]["offensive"]
    def2 = data[t2]["defensive"]
    sos1 = data[t1]["sos"]
    sos2 = data[t2]["sos"]
    score = ((off1 * sos1) + (sos2 * def2)) / 2
    return score

def oddsFunction(score1, score2):
    return min(1, ((0.0035 * abs(score1 - score2)) + 0.5))

comparison = CompareFunction(wantHighest=True, comparison=compareTeams, isolated=False, oddsFunction=oddsFunction)
