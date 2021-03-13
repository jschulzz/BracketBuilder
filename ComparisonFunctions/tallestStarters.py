from statistics import mean

from ComparisonFunctions.CompareFunction import CompareFunction
from ComparisonFunctions.utils import getStarters


def compareTeams(team, data):
    starters = getStarters(data[team]["players"])
    heights = list(map(lambda x: x["height"], starters))
    score = max(heights)
    return score


comparison = CompareFunction(wantHighest=True, comparison=compareTeams)
