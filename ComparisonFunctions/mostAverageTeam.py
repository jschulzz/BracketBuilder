from statistics import mean

from ComparisonFunctions.CompareFunction import CompareFunction
from ComparisonFunctions.utils import getStarters

# TODO: This needs a lot of refactoring to fit the new structure

stats = [
    "offensive",
    "defensive",
    "sos",
    "points_scored",
    "points_against",
    "g",
    "mp",
    "fg",
    "fga",
    "fg_pct",
    "fg2",
    "fg2a",
    "fg2_pct",
    "fg3",
    "fg3a",
    "fg3_pct",
    "ft",
    "fta",
    "ft_pct",
    "orb",
    "drb",
    "trb",
    "ast",
    "stl",
    "blk",
    "tov",
    "pf",
    "pts",
    "pts_per_g",
]


def compareTeams(t1, t2, data):
    field = input_args["field"]
    t1score = 0
    for stat in stats:
        list_of_stat = list(
            map(
                lambda x: data[replace(x["team"])][stat],
                list(filter(lambda x: "/" not in x["team"], field)),
            )
        )
        list_of_stat.sort()
        t1score += abs((len(field) - 1) / 2 - list_of_stat.index(data[t1][stat]))
    return t1score


comparison = CompareFunction(wantHighest=False, comparison=compareTeams)
