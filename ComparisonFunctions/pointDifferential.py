from statistics import mean

from ComparisonFunctions.CompareFunction import CompareFunction
from ComparisonFunctions.utils import getStarters


def compareTeams(t1, t2, data):
    PS1 = data[t1]["points_scored"]
    PA2 = data[t2]["points_against"]
    score = (PS1 + PA2) / 2
    return score


comparison = CompareFunction(wantHighest=True, comparison=compareTeams, isolated=False)
