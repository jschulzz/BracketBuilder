# Python program to print all paths from a source to destination.

from collections import defaultdict
from statistics import mean
import json
import sys
import re
import math
import random
import os
import numpy as np
from functools import reduce

# TODO: What if these were all seperate objects, containing the function, and the reasoning?


def printpath(data_point):
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


searchreplacements = {
    "TCU$": "Texas Christian",
    "Saint Francis": "Saint Francis",
    "UCF": "Central Florida",
    "UC Irvine": "California Irvine",
}


def searchfor(t):
    for w in searchreplacements:
        if re.search(w, t):
            t = searchreplacements[w]
    return t + " University"


replacements = {
    "St$": "State",
    "St\.": "Saint",
    "Prairie View A&M": "Prairie View",
    "\(pa\)": "(PA)",
    "North Carolina$": "UNC",
    "Ucf$": "UCF",
    "Saint John's$": "St. John's (NY)",
    "Saint Peter's$": "St. Peter's",
    "UC Irvine$": "UC-Irvine",
    "Liu Brooklyn$": "LIU-Brooklyn",
    "East Tennessee State$": "ETSU",
    "Charleston": "College of Charleston",
    "UT Arlington": "Texas-Arlington",
    "Bowling Green": "Bowling Green State",
    "N.C. A&T": "North Carolina A&T;",
    "UNCG": "UNC Greensboro",
    "Loyola Chicago": "Loyola (IL)",
    "W\. Kentucky": "Western Kentucky",
}


def replace(t):
    for w in replacements:
        t = re.sub(w, replacements[w], t)
    return t


def fixNames(t1, t2):
    return (fixName(t1), fixName(t2))


def fixName(t):
    if t not in list(data.keys()):
        t = replace(t)
    return t


def thiccestPlayer(input_args):
    t1 = input_args["team1"]
    t2 = input_args["team2"]
    t1, t2 = fixNames(t1, t2)
    weights1 = data[t1]["weights"]
    weights2 = data[t2]["weights"]
    big1 = max(weights1)
    big2 = max(weights2)
    return big1, big2, max(big1 / (big1 + big2), big2 / (big1 + big2))


def thiccestStarters(input_args):
    t1 = input_args["team1"]
    t2 = input_args["team2"]
    if t1 not in list(data.keys()):
        t1 = replace(t1)
    if t2 not in list(data.keys()):
        t2 = replace(t2)
    weights1 = data[t1]["weights"][:5]
    weights2 = data[t2]["weights"][:5]
    big1 = mean(weights1)
    big2 = mean(weights2)
    return big1, big2, max(big1 / (big1 + big2), big2 / (big1 + big2))


def machineLearning(input_args):
    team1name = input_args["team1"]
    team2name = input_args["team2"]
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    import train
    import keras

    if team1name not in list(data.keys()):
        team1name = replace(team1name)
    if team2name not in list(data.keys()):
        team2name = replace(team2name)
    t1 = data[team1name]
    t2 = data[team2name]
    input_list = train.createInputList(t1) + train.createInputList(t2)
    keras.backend.clear_session()
    model = train.createModel(len(input_list))

    model.load_weights("best.hdf5")
    prediction = model.predict(np.expand_dims(input_list, axis=0))[0][0]
    keras.backend.clear_session()
    if prediction > 0.5:
        return 0, 1, round(max(prediction, 1 - prediction) * 1000) / 1000
    return 1, 0, round(max(prediction, 1 - prediction) * 1000) / 1000


def shortestStarters(input_args):
    t1 = input_args["team1"]
    t2 = input_args["team2"]
    t1, t2 = fixNames(t1, t2)
    weights1 = data[t1]["heights"][:5]
    weights2 = data[t2]["heights"][:5]
    small1 = min(weights1)
    small2 = min(weights2)
    return small1, small2, max(small1 / (small1 + small2), small2 / (small1 + small2))


def closestAvgHometown(input_args):
    t1 = input_args["team1"]
    t2 = input_args["team2"]
    t1, t2 = fixNames(t1, t2)
    homes1 = data[t1]["hometowns"][:5]
    homes2 = data[t2]["hometowns"][:5]
    from geopy import Nominatim
    from geopy import distance

    geolocator = Nominatim(user_agent="CBBScraping")
    school1 = geolocator.geocode(searchfor(t1), addressdetails=True, timeout=10)
    school2 = geolocator.geocode(searchfor(t2), addressdetails=True, timeout=10)
    if school1.raw["address"]["country_code"] != "us":
        print(school1)
    if school2.raw["address"]["country_code"] != "us":
        print(school2)
    locs1 = list(map(lambda x: geolocator.geocode(x, timeout=10), homes1))
    locs2 = list(map(lambda x: geolocator.geocode(x, timeout=10), homes2))
    avgLat1 = (
        reduce(
            lambda x, y: x + y,
            list(map(lambda x: x.latitude if x != None else 39.86, locs1)),
        )
        / 5
    )
    avgLon1 = (
        reduce(
            lambda x, y: x + y,
            list(map(lambda x: x.longitude if x != None else -98.6, locs1)),
        )
        / 5
    )
    avgLat2 = (
        reduce(
            lambda x, y: x + y,
            list(map(lambda x: x.latitude if x != None else 39.86, locs2)),
        )
        / 5
    )
    avgLon2 = (
        reduce(
            lambda x, y: x + y,
            list(map(lambda x: x.longitude if x != None else -98.6, locs2)),
        )
        / 5
    )
    avg1 = (avgLat1, avgLon1)
    avg2 = (avgLat2, avgLon2)
    s1 = (school1.latitude, school1.longitude)
    s2 = (school2.latitude, school2.longitude)

    res1 = distance.distance(avg1, s1).miles
    res2 = distance.distance(avg2, s2).miles
    return res1, res2, max(res1 / (res1 + res2), res2 / (res1 + res2))


def closestToGame(input_args):
    t1 = input_args["team1"]
    t2 = input_args["team2"]
    site = input_args["site"]
    t1, t2 = fixNames(t1, t2)
    from geopy import Nominatim
    from geopy import distance

    geolocator = Nominatim(user_agent="CBBScraping")
    school1 = geolocator.geocode(searchfor(t1), addressdetails=True, timeout=10)
    school2 = geolocator.geocode(searchfor(t2), addressdetails=True, timeout=10)
    # print(field)
    if school1.raw["address"]["country_code"] != "us":
        print(school1)
    if school2.raw["address"]["country_code"] != "us":
        print(school2)
    site_loc = geolocator.geocode(site, addressdetails=True, timeout=10)
    s1 = (school1.latitude, school1.longitude)
    s2 = (school2.latitude, school2.longitude)
    site_coords = (site_loc.latitude, site_loc.longitude)
    res1 = distance.distance(site_coords, s1).miles
    res2 = distance.distance(site_coords, s2).miles
    return res1, res2, max(res1 / (res1 + res2), res2 / (res1 + res2))


def tallestStarters(input_args):
    t1 = input_args["team1"]
    t2 = input_args["team2"]
    t1, t2 = fixNames(t1, t2)
    weights1 = data[t1]["heights"][:5]
    weights2 = data[t2]["heights"][:5]
    small1 = max(weights1)
    small2 = max(weights2)
    return small1, small2, max(small1 / (small1 + small2), small2 / (small1 + small2))


def avgHeight(input_args):
    t1 = input_args["team1"]
    t2 = input_args["team2"]
    t1, t2 = fixNames(t1, t2)
    heights1 = data[t1]["heights"]
    heights2 = data[t2]["heights"]
    small1 = mean(heights1)
    small2 = mean(heights2)
    return small1, small2, max(small1 / (small1 + small2), small2 / (small1 + small2))


def mostAvgTeam(input_args):
    t1 = input_args["team1"]
    t2 = input_args["team2"]
    field = input_args["field"]
    t1, t2 = fixNames(t1, t2)

    t1score = 0
    t2score = 0
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

    for stat in stats:
        list_of_stat = list(
            map(
                lambda x: data[replace(x["team"])][stat],
                list(filter(lambda x: "/" not in x["team"], field)),
            )
        )
        list_of_stat.sort()
        t1score += abs((len(field) - 1) / 2 - list_of_stat.index(data[t1][stat]))
        t2score += abs((len(field) - 1) / 2 - list_of_stat.index(data[t2][stat]))
    # print(sost1)
    return (
        t1score,
        t2score,
        max(t1score / (t1score + t2score), t2score / (t1score + t2score)),
    )


def compareJerseys(input_args):
    t1 = input_args["team1"]
    t2 = input_args["team2"]
    t1, t2 = fixNames(t1, t2)
    jerseyNums1 = data[t1]["jersey_nums"]
    jerseyNums2 = data[t2]["jersey_nums"]
    std1 = np.std(jerseyNums1)
    std2 = np.std(jerseyNums2)
    return std1, std2, max(std1 / (std1 + std2), std2 / (std1 + std2))


def pointDifferential(input_args):
    t1 = input_args["team1"]
    t2 = input_args["team2"]
    t1, t2 = fixNames(t1, t2)
    PS1 = data[t1]["points_scored"]
    PS2 = data[t2]["points_scored"]
    PA1 = data[t1]["points_against"]
    PA2 = data[t2]["points_against"]
    res1 = (PS1 + PA2) / 2
    res2 = (PS2 + PA1) / 2
    return res1, res2, max(res1 / (res1 + res2), res2 / (res1 + res2))


def pointsOffFouls(input_args):
    t1 = input_args["team1"]
    t2 = input_args["team2"]
    t1, t2 = fixNames(t1, t2)
    fouls1 = data[t1]["pf"]
    fouls2 = data[t2]["pf"]
    ft1 = data[t1]["ft_pct"]
    ft2 = data[t2]["ft_pct"]
    games1 = data[t1]["g"]
    games2 = data[t2]["g"]
    res1 = fouls2 / games2 * ft1
    res2 = fouls1 / games1 * ft2
    return res1, res2, max(res1 / (res1 + res2), res2 / (res1 + res2))


def efficiencyMargin(input_args):
    t1 = input_args["team1"]
    t2 = input_args["team2"]
    t1, t2 = fixNames(t1, t2)
    off1 = data[t1]["offensive"]
    off2 = data[t2]["offensive"]
    def1 = data[t1]["defensive"]
    def2 = data[t2]["defensive"]
    res1 = (off1 + def2) / 2
    res2 = (off2 + def1) / 2
    chance = (0.5 * abs(res1 - res2) / 10) + 0.5
    return res1, res2, chance


def efficiencyMarginWithSOS(input_args):
    t1 = input_args["team1"]
    t2 = input_args["team2"]
    t1, t2 = fixNames(t1, t2)
    print(t1, t2)
    # if t1 not in list(data.keys()):
    #     t1 = replace(t1)
    #     if t1 not in list(data.keys()):
    #         return 0, 100, 100
    # if t2 not in list(data.keys()):
    #     t2 = replace(t2)
    #     if t2 not in list(data.keys()):
    #         return 100, 0, 100
    off1 = data[t1]["offensive"]
    off2 = data[t2]["offensive"]
    def1 = data[t1]["defensive"]
    def2 = data[t2]["defensive"]
    sos1 = data[t1]["sos"]
    sos2 = data[t2]["sos"]
    res1 = ((off1 * sos1) + (sos2 * def2)) / 2
    res2 = ((off2 * sos2) + (sos1 * def1)) / 2
    # print(t1)
    # print("\tOff:", off1, "Def:", def1, "SOS:", sos1, "Scr:", res1)
    # print(t2)
    # print("\tOff:", off2, "Def:", def2, "SOS:", sos2, "Scr:", res2)
    chance = min(1, ((0.0035 * abs(res1 - res2)) + 0.5))
    return res1, res2, chance


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
def findpaths(g, src, dst, writeGames=True, depth=5, others=[]):
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
                printpath(data_point)
            score += scoreFn(suck_degree, data_point[1], len(path) - 1)

        # print(g, last)
        for team in g[last]:
            # print(team, path)
            # if team[0] not in path or team[0] == src:  # circle suck
            if team[0] not in path:  # non circle such
                newpath = list(path)
                newpath.append(team[0])
                queue.append((newpath, trans_score + team[1]))


def transitiveWinScores(input_args):
    t1 = input_args["team1"]
    t2 = input_args["team2"]
    writePaths = input_args.get("writePaths", False)
    depth = input_args.get("depth", 4)
    t1, t2 = fixNames(t1, t2)
    print("Looking for", t1, "and", t2)
    source_idx = list(data.keys()).index(t1)
    dest_idx = list(data.keys()).index(t2)
    source_score = findpaths(
        g, source_idx, dest_idx, writeGames=writePaths, depth=depth
    )
    dest_score = source_score
    if t1 != t2:
        dest_score = findpaths(
            g, dest_idx, source_idx, writeGames=writePaths, depth=depth
        )
    chance = 0.5
    if (source_score + dest_score) != 0:
        chance = max(
            source_score / (source_score + dest_score),
            dest_score / (source_score + dest_score),
        )
    return source_score, dest_score, chance


data = {}
bracket_data = {}
with open("stats_2020.json") as f:
    data = json.load(f)["team_stats"]
g = buildGraph(data)


def testMatch(method, team1, team2, site=""):
    print("\nUsing:", method.__name__)
    combined_data = {
        "team1": team1,
        "team2": team2,
        "site": site,
        "field": None,
        "writePaths": True,
    }
    team1_score, team2_score, chance = method(combined_data)
    losing_odds = round((1 - chance) * 1000) / 10
    print(team1, ":", team1_score, "\t", team2, ":", team2_score)
    if team1_score > team2_score:
        print(team1, "over", team2, "by", 100 * chance, "-", losing_odds)
    else:
        print(team2, "over", team1, "by", 100 * chance, "-", losing_odds)


if __name__ == "__main__":
    team1 = sys.argv[1]
    team2 = team1
    if len(sys.argv) > 2:
        team2 = sys.argv[2]
    others = []
    score = 0
    # testMatch(machineLearning, team1, team2)
    # testMatch(machineLearning, team1, team2)
    # testMatch(pointDifferential, team1, team2)
    testMatch(efficiencyMarginWithSOS, team1, team2)
