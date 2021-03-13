from statistics import mean

from ComparisonFunctions.CompareFunction import CompareFunction
from ComparisonFunctions.utils import getStarters


def compareTeams(t1, t2, data):
    ft1 = data[t1]["ft_pct"]
    fouls2 = data[t2]["pf"]
    games2 = data[t2]["g"]
    score = fouls2 / games2 * ft1
    return score


comparison = CompareFunction(wantHighest=True, comparison=compareTeams, isolated=False)
