from statistics import mean

from ComparisonFunctions.CompareFunction import CompareFunction
from ComparisonFunctions.utils import getStarters


def printpath(data, data_point):
    path = data_point[0]
    score = data_point[1]
    print(round(score / max(len(path) - 1, 1), 3), "pts per level", end="\t- ")
    for i in path:
        print(list(data.keys())[i], end=" > ")
    print()


def scoreFn(suck_degree, game_score, num_games):
    score_multiplier = 1.0
    diff_per_level = game_score / max(num_games, 1)
    if diff_per_level <= 3:
        score_multiplier = 0.75
    elif diff_per_level <= 6:
        score_multiplier = 0.8
    elif diff_per_level <= 8:
        score_multiplier = 0.9
    else:
        score_multiplier = 1.0
    return (100) * score_multiplier * (1 / 2) ** (suck_degree)


def buildGraph(data):
    g = []
    for winner in data:
        for loser in data[winner]["wins"]:
            winner_idx = list(data.keys()).index(winner)
            try:
                loser_idx = list(data.keys()).index(loser)
                if winner_idx >= len(g):
                    g.append([(loser_idx, data[winner]["wins"][loser])])
                else:
                    g[winner_idx].append((loser_idx, data[winner]["wins"][loser]))
            except:
                pass
    return g


# TODO: refactor this to look like the other functions
def findpaths(g, src, dst, data, writeGames=True, depth=5, others=[]):
    score = 0
    queue = []

    path = []
    path.append(src)
    queue.append((path, 0))
    suck_degree = 0
    while queue:
        data_point = queue.pop(0)
        # print(data_point)
        path = data_point[0]
        trans_score = data_point[1]
        last = path[len(path) - 1]
        if suck_degree > depth:
            return score
        if len(path) > suck_degree:
            suck_degree += 1
            if writeGames:
                print("Entering Degree", suck_degree, "of suck. Score at", score)
        others_contained = True
        for i in others:
            if i not in path:
                others_contained = False
        if last == dst and others_contained:
            if writeGames:
                printpath(data, data_point)
            score += scoreFn(suck_degree, data_point[1], len(path) - 1)

        # print(g, last)
        for team in g[last]:
            # print(team, path)
            # if team[0] not in path or team[0] == src:  # circle suck
            if team[0] not in path:  # non circle such
                newpath = list(path)
                newpath.append(team[0])
                queue.append((newpath, trans_score + team[1]))


def compareTeams(t1, t2, data):

    g = buildGraph(data)
    writePaths = True
    depth = 4
    print("Looking for", t1, "and", t2)
    source_idx = list(data.keys()).index(t1)
    dest_idx = list(data.keys()).index(t2)
    source_score = findpaths(
        g, source_idx, dest_idx, data, writeGames=writePaths, depth=depth
    )
    dest_score = source_score
    if t1 != t2:
        dest_score = findpaths(
            g, dest_idx, source_idx, data, writeGames=writePaths, depth=depth
        )
    chance = 0.5
    if (source_score + dest_score) != 0:
        chance = max(
            source_score / (source_score + dest_score),
            dest_score / (source_score + dest_score),
        )
    return source_score, dest_score, chance


comparison = CompareFunction(
    wantHighest=True, comparison=compareTeams, isolated=False, symmetric=False
)
