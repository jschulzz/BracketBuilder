# Python program to print all paths from a source to destination.

from collections import defaultdict
from statistics import mean
import json
import sys
# import urllib
import train
import re
import random
import numpy as np
from functools import reduce


def printpath(data_point):
    path = data_point[0]
    score = data_point[1]
    print(round(score/max(len(path)-1, 1), 3), "pts per level", end="\t- ")
    for i in path:
        print(list(data.keys())[i], end=" > ")
    print()


def findpaths(g, src, dst, writeGames=False, depth=5, others=[]):
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
        if len(path) > suck_degree:
            suck_degree += 1
            if writeGames:
                print()
                print("Entering Degree", suck_degree,
                      "of suck. Score at", score)
        if suck_degree > depth:
            return score
        others_contained = True
        for i in others:
            if i not in path:
                others_contained = False
        if last == dst and others_contained:
            if writeGames:
                printpath(data_point)
            score += scoreFn(suck_degree, data_point[1], len(path)-1)

        # print(g, last)
        for team in g[last]:
            # print(team, path)
            if team[0] not in path or team[0] == src:  # circle suck
                # if team[0] not in path:  # non circle such
                newpath = list(path)
                newpath.append(team[0])
                queue.append((newpath, trans_score + team[1]))


data = {}
bracket_data = {}
with open('games.json') as f:
    data = json.load(f)


def scoreFn(suck_degree, game_score, num_games):
    score_multiplier = 1.0
    diff_per_level = game_score / max(num_games, 1)
    if(diff_per_level <= 3):
        score_multiplier = 0.75
    elif(diff_per_level <= 6):
        score_multiplier = 0.8
    elif(diff_per_level <= 8):
        score_multiplier = 0.9
    else:
        score_multiplier = 1.0
    return (100) * score_multiplier * (1/2) ** (suck_degree)


# print(len(data))
g = []
for winner in data:
    # print(winner)
    for loser in data[winner]["opponent_scores"]:
        winner_idx = list(data.keys()).index(winner)
        # loser_id
        try:
            loser_idx = list(data.keys()).index(loser)
            # print(loser_idx)
            if winner_idx >= len(g):
                g.append([(loser_idx, data[winner]["opponent_scores"][loser])])
            else:
                g[winner_idx].append(
                    (loser_idx, data[winner]["opponent_scores"][loser]))
            # print(winner_idx, loser_idx)/
        except:
            # print(loser, "never won")
            pass

score = 0

searchreplacements = {
    'TCU$': "Texas Christian",
    'Saint Francis': "Saint Francis",
    'UCF': "Central Florida",
    'UC Irvine': "California Irvine",
}


def searchfor(t):
    for w in searchreplacements:
        if re.search(w, t):
            t = searchreplacements[w]
    return t + " University"


replacements = {
    'St$': "State",
    'St\.': "Saint",
    "Prairie View A&M": "Prairie View",
    "\(pa\)": "(PA)",
    "North Carolina$": "UNC",
    "Ucf$": "UCF",
    "Saint John's$": "St. John's (NY)",
    "UC Irvine$": "UC-Irvine",
}


def replace(t):
    for w in replacements:
        t = re.sub(w, replacements[w], t)
    return t


def thiccestPlayer(t1, t2, field):
    if t1 not in list(data.keys()):
        t1 = replace(t1)
    if t2 not in list(data.keys()):
        t2 = replace(t2)
    weights1 = data[t1]["weights"]
    weights2 = data[t2]["weights"]
    big1 = max(weights1)
    big2 = max(weights2)
    # std2 = np.std(jerseyNums2)
    return big1, big2, max(big1/(big1+big2), big2/(big1+big2))


def thiccestStarters(t1, t2, field):
    if t1 not in list(data.keys()):
        t1 = replace(t1)
    if t2 not in list(data.keys()):
        t2 = replace(t2)
    weights1 = data[t1]["weights"][:5]
    weights2 = data[t2]["weights"][:5]
    big1 = mean(weights1)
    big2 = mean(weights2)
    # std2 = np.std(jerseyNums2)
    return big1, big2, max(big1/(big1+big2), big2/(big1+big2))


def machineLearning(team1name, team2name, field):
    if team1name not in list(data.keys()):
        team1name = replace(team1name)
    if team2name not in list(data.keys()):
        team2name = replace(team2name)
    t1 = data[team1name]
    t2 = data[team2name]
    # print(t1, t2)
    input_list = train.createInputList(t1, t2)
    model = train.createModel(len(input_list))

    model.load_weights("weights-improvement-85-0.4550-0.5646.hdf5")
    prediction = model.predict(np.expand_dims(input_list, axis=0))[0][0]
    if prediction > 0.5:
        # print( 100 - round(100 * prediction), round(100 * prediction), max(prediction, 1-prediction))
        return 0, 1, round(max(prediction, 1-prediction) * 1000)/1000
    return 1, 0, round(max(prediction, 1-prediction) * 1000)/1000


def shortestStarters(t1, t2, field):
    if t1 not in list(data.keys()):
        t1 = replace(t1)
    if t2 not in list(data.keys()):
        t2 = replace(t2)
    weights1 = data[t1]["heights"][:5]
    weights2 = data[t2]["heights"][:5]
    small1 = min(weights1)
    small2 = min(weights2)
    # std2 = np.std(jerseyNums2)
    return small1, small2, max(small1/(small1+small2), small2/(small1+small2))


def closestAvgHometown(t1, t2, field):
    if t1 not in list(data.keys()):
        t1 = replace(t1)
    if t2 not in list(data.keys()):
        t2 = replace(t2)
    homes1 = data[t1]["hometowns"][:5]
    homes2 = data[t2]["hometowns"][:5]
    from geopy import Nominatim
    from geopy import distance
    geolocator = Nominatim(user_agent="CBBScraping")
    school1 = geolocator.geocode(
        searchfor(t1), addressdetails=True, timeout=10)
    school2 = geolocator.geocode(
        searchfor(t2), addressdetails=True, timeout=10)
    # print(searchfor(t1), searchfor(t2))
    # print(school1, school2)
    if school1.raw["address"]["country_code"] != "us":
        print(school1)
    if school2.raw["address"]["country_code"] != "us":
        print(school2)
    locs1 = list(map(lambda x: geolocator.geocode(x, timeout=10), homes1))
    locs2 = list(map(lambda x: geolocator.geocode(x, timeout=10), homes2))
    # print(t1, t2, locs1, locs2)
    avgLat1 = reduce(lambda x, y: x + y,
                     list(map(lambda x: x.latitude if x != None else 39.86, locs1))) / 5
    avgLon1 = reduce(lambda x, y: x + y,
                     list(map(lambda x: x.longitude if x != None else -98.6, locs1))) / 5
    avgLat2 = reduce(lambda x, y: x + y,
                     list(map(lambda x: x.latitude if x != None else 39.86, locs2))) / 5
    avgLon2 = reduce(lambda x, y: x + y,
                     list(map(lambda x: x.longitude if x != None else -98.6, locs2))) / 5
    avg1 = (avgLat1, avgLon1)
    avg2 = (avgLat2, avgLon2)
    s1 = (school1.latitude, school1.longitude)
    s2 = (school2.latitude, school2.longitude)

    # small1 = min(weights1)
    # print(avg1, avg2, s1, s2)
    # small2 = min(weights2)
    # std2 = np.std(jerseyNums2)
    res1 = distance.distance(avg1, s1).miles
    res2 = distance.distance(avg2, s2).miles
    return res1, res2, max(res1/(res1+res2), res2/(res1+res2))


def closestToGame(t1, t2, field, site):
    if t1 not in list(data.keys()):
        t1 = replace(t1)
    if t2 not in list(data.keys()):
        t2 = replace(t2)
    from geopy import Nominatim
    from geopy import distance
    geolocator = Nominatim(user_agent="CBBScraping")
    school1 = geolocator.geocode(
        searchfor(t1), addressdetails=True, timeout=10)
    school2 = geolocator.geocode(
        searchfor(t2), addressdetails=True, timeout=10)
    # print(field)
    if school1.raw["address"]["country_code"] != "us":
        print(school1)
    if school2.raw["address"]["country_code"] != "us":
        print(school2)
    site_loc = geolocator.geocode(
        site, addressdetails=True, timeout=10)
    s1 = (school1.latitude, school1.longitude)
    s2 = (school2.latitude, school2.longitude)
    site_coords = (site_loc.latitude, site_loc.longitude)

    # small1 = min(weights1)
    # print(avg1, avg2, s1, s2)
    # small2 = min(weights2)
    # std2 = np.std(jerseyNums2)
    res1 = distance.distance(site_coords, s1).miles
    res2 = distance.distance(site_coords, s2).miles
    return res1, res2, max(res1/(res1+res2), res2/(res1+res2))


def tallestStarters(t1, t2, field):
    if t1 not in list(data.keys()):
        t1 = replace(t1)
    if t2 not in list(data.keys()):
        t2 = replace(t2)
    weights1 = data[t1]["heights"][:5]
    weights2 = data[t2]["heights"][:5]
    small1 = max(weights1)
    small2 = max(weights2)
    # std2 = np.std(jerseyNums2)
    return small1, small2, max(small1/(small1+small2), small2/(small1+small2))


def avgHeight(t1, t2, field):
    if t1 not in list(data.keys()):
        t1 = replace(t1)
    if t2 not in list(data.keys()):
        t2 = replace(t2)
    heights1 = data[t1]["heights"]
    heights2 = data[t2]["heights"]
    small1 = mean(heights1)
    small2 = mean(heights2)
    # std2 = np.std(jerseyNums2)
    return small1, small2, max(small1/(small1+small2), small2/(small1+small2))


def mostAvgTeam(t1, t2, field):
    if t1 not in list(data.keys()):
        t1 = replace(t1)
    if t2 not in list(data.keys()):
        t2 = replace(t2)

    t1score = 0
    t2score = 0
    stats = ["offensive", "defensive", "sos", "points_scored", "points_against", "g", "mp", "fg", "fga", "fg_pct", "fg2", "fg2a",
             "fg2_pct", "fg3", "fg3a", "fg3_pct", "ft", "fta", "ft_pct", "orb", "drb", "trb", "ast", "stl", "blk", "tov", "pf", "pts", "pts_per_g"]

    for stat in stats:
        list_of_stat = list(map(lambda x: data[replace(
            x["team"])][stat], list(filter(lambda x: "/" not in x["team"], field))))
        list_of_stat.sort()
        t1score += abs((len(field) - 1)/2 - list_of_stat.index(data[t1][stat]))
        t2score += abs((len(field) - 1)/2 - list_of_stat.index(data[t2][stat]))
    # print(sost1)

    # meanSOS = mean(list(map(lambda x: data[replace(
    #     x["team"])]["sos"] if "/" not in x["team"] else 0, field)))
    # meanOff = mean(list(map(lambda x: data[replace(
    #     x["team"])]["offensive"]if "/" not in x["team"] else 100, field)))
    # meanDef = mean(list(map(lambda x: data[replace(
    #     x["team"])]["defensive"]if "/" not in x["team"] else 100, field)))
    # meanPS = mean(list(map(lambda x: data[replace(
    #     x["team"])]["points_scored"] if "/" not in x["team"] else 70, field)))
    # meanPA = mean(list(map(lambda x: data[replace(
    #     x["team"])]["points_against"] if "/" not in x["team"] else 70, field)))
    # t1score = abs(data[t1]["sos"] - meanSOS)/meanSOS + \
    #     abs(data[t1]["offensive"] - meanOff)/meanOff + \
    #     abs(data[t1]["defensive"] - meanDef)/meanDef + \
    #     abs(data[t1]["points_scored"] - meanPS)/meanPS + \
    #     abs(data[t1]["points_against"] - meanPA)/meanPA
    # t2score = abs(data[t2]["sos"] - meanSOS)/meanSOS + \
    #     abs(data[t2]["offensive"] - meanOff)/meanOff + \
    #     abs(data[t2]["defensive"] - meanDef)/meanDef + \
    #     abs(data[t2]["points_scored"] - meanPS)/meanPS + \
    #     abs(data[t2]["points_against"] - meanPA)/meanPA
    return t1score, t2score, max(t1score/(t1score+t2score), t2score/(t1score+t2score))


def compareJerseys(t1, t2, field):
    if t1 not in list(data.keys()):
        t1 = replace(t1)
    if t2 not in list(data.keys()):
        t2 = replace(t2)
    jerseyNums1 = data[t1]["jersey_nums"]
    jerseyNums2 = data[t2]["jersey_nums"]
    std1 = np.std(jerseyNums1)
    std2 = np.std(jerseyNums2)
    return std1, std2, max(std1/(std1+std2), std2/(std1+std2))


def pointDifferential(t1, t2, field):
    if t1 not in list(data.keys()):
        t1 = replace(t1)
    if t2 not in list(data.keys()):
        t2 = replace(t2)
    PS1 = data[t1]["points_scored"]
    PS2 = data[t2]["points_scored"]
    PA1 = data[t1]["points_against"]
    PA2 = data[t2]["points_against"]
    res1 = PS1 - PA2
    res2 = PS2 - PA1
    return res1, res2, max(res1/(res1+res2), res2/(res1+res2))


def pointsOffFouls(t1, t2, field):
    if t1 not in list(data.keys()):
        t1 = replace(t1)
    if t2 not in list(data.keys()):
        t2 = replace(t2)
    fouls1 = data[t1]["pf"]
    fouls2 = data[t2]["pf"]
    ft1 = data[t1]["ft_pct"]
    ft2 = data[t2]["ft_pct"]
    games1 = data[t1]["g"]
    games2 = data[t2]["g"]
    res1 = fouls2 / games2 * ft1
    res2 = fouls1 / games1 * ft2
    return res1, res2, max(res1/(res1+res2), res2/(res1+res2))


def efficiencyMargin(t1, t2, field):
    if t1 not in list(data.keys()):
        t1 = replace(t1)
    if t2 not in list(data.keys()):
        t2 = replace(t2)
    off1 = data[t1]["offensive"]
    off2 = data[t2]["offensive"]
    def1 = data[t1]["defensive"]
    def2 = data[t2]["defensive"]
    res1 = (off1 + def2)/2
    res2 = (off2 + def1)/2
    return res1,  res2, max(res1/(res1+res2), res2/(res1+res2))


def efficiencyMarginWithSOS(t1, t2, field):
    if t1 not in list(data.keys()):
        t1 = replace(t1)
    if t2 not in list(data.keys()):
        t2 = replace(t2)
    off1 = data[t1]["offensive"]
    off2 = data[t2]["offensive"]
    def1 = data[t1]["defensive"]
    def2 = data[t2]["defensive"]
    sos1 = data[t1]["sos"]
    sos2 = data[t2]["sos"]
    # print(sos1, sos2)
    # random.seed()
    # if random.randint(1, 101) < 25:
    #     off1 += 15
    # if random.randint(1, 101) < 25:
    #     off2 += 15
    # if random.randint(1, 101) < 12.5:
    #     off1 -= 15
    # if random.randint(1, 101) < 12.5:
    #     off2 -= 15
    # if random.randint(1, 101) < 8.64:
    #     def1 += 15
    # if random.randint(1, 1) < 8.64:
    #     def2 += 15
    # if random.randint(1, 101) < 4.371:
    #     def1 -= 15
    # if random.randint(1, 101) < 4.371:
    #     def2 -= 15
    res1 = ((off1 * sos1) + (sos2 * def2))/2
    res2 = ((off2 * sos2) + (sos1 * def1))/2
    return res1, res2, max(res1/(res1+res2), res2/(res1+res2))


def getScores(t1, t2, writePaths, depth):
    score = 0
    if t1 not in list(data.keys()):
        # print("replacing", t1)
        t1 = replace(t1)
    if t2 not in list(data.keys()):
        # print("replacing", t2)
        t2 = replace(t2)
    s_idx = list(data.keys()).index(t1)
    d_idx = list(data.keys()).index(t2)
    s_score = findpaths(g, s_idx, d_idx, writePaths, depth)
    d_score = s_score
    if(t1 != t2):
        d_score = findpaths(g, d_idx, s_idx, writePaths, depth)
    chance = 0.5
    if (s_score+d_score) != 0:
        chance = max(s_score/(s_score+d_score), d_score/(s_score+d_score))
    return s_score, d_score, chance


if __name__ == "__main__":
    s = sys.argv[1]
    d = s
    if(len(sys.argv) > 2):
        d = sys.argv[2]
    others = []
    score = 0
    # s_score, d_score = getScores(s, d, True, 5)
    s_score, d_score, c = machineLearning(s, d, 1)
    losing_score = round((1 - c) * 1000)/10
    # losing_score = 100 - c
    if s_score > d_score:
        print(s, "over", d, "by", 100 * c, "-", losing_score)
    else:
        print(d, "over", s, "by", 100 * c, "-", losing_score)
    # print(d, "over", s, "by", d_score)
