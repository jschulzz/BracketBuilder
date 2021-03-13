import numpy as np

from ComparisonFunctions.CompareFunction import CompareFunction
from ComparisonFunctions.utils import getStarters


def compareTeams(team, data):
    jerseyNums = list(map(lambda x: x.get("jersey", 0), data[team]["players"].values()))
    jerseyDeviation = np.std(jerseyNums)
    return jerseyDeviation



comparison = CompareFunction(wantHighest=False, comparison=compareTeams)
