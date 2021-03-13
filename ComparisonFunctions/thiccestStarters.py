from statistics import mean

from ComparisonFunctions.CompareFunction import CompareFunction
from ComparisonFunctions.utils import getStarters


def compareTeams(team, data):
    starters = getStarters(data[team]["players"])
    weights = list(map(lambda x: x["weight"], starters))
    score = mean(weights)
    return score


comparison = CompareFunction(wantHighest=True, comparison=compareTeams)
