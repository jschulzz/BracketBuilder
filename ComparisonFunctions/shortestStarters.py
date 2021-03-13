from statistics import mean

from ComparisonFunctions.CompareFunction import CompareFunction
from ComparisonFunctions.utils import getStarters


def compareTeams(team, data):
    starters = getStarters(data[team]["players"])
    weights = list(map(lambda x: x["height"], starters))
    score = min(weights)
    return score


comparison = CompareFunction(wantHighest=False, comparison=compareTeams)
