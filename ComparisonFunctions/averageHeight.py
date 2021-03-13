from statistics import mean

from ComparisonFunctions.CompareFunction import CompareFunction
from ComparisonFunctions.utils import getStarters


def compareTeams(team, data):
    players = data[team]["players"].values()
    heights = list(map(lambda x: x["height"], players))
    score = mean(heights)
    return score


comparison = CompareFunction(wantHighest=True, comparison=compareTeams)
