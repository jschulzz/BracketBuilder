from statistics import mean

from ComparisonFunctions.CompareFunction import CompareFunction
from ComparisonFunctions.utils import getStarters


def compareTeams(t1, t2, data):
    off1 = data[t1]["offensive"]
    def2 = data[t2]["defensive"]
    res1 = (off1 + def2) / 2
    return res1

def oddsFunction(score1, score2):
    return (0.5 * abs(score1 - score2) / 10) + 0.5

comparison = CompareFunction(wantHighest=True, comparison=compareTeams, isolated=False, oddsFunction=oddsFunction)
