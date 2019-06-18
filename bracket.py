import json
import search
import numpy as np
import copy
import math

data = {}
bracket_data = {}
with open('games.json') as f:
    data = json.load(f)
with open('node_modules/bracket-data/data/ncaam/2019.json') as f:
    bracket_data = json.load(f)

sortorder = [0, 15, 7, 8, 4, 11, 3, 12, 5, 10, 2, 13, 6, 9, 1, 14]


east = list(np.array(bracket_data["teams"]["E"])[sortorder])
midwest = list(np.array(bracket_data["teams"]["M"])[sortorder])
west = list(np.array(bracket_data["teams"]["W"])[sortorder])
south = list(np.array(bracket_data["teams"]["S"])[sortorder])
east_locations = bracket_data["east_locations"]
west_locations = bracket_data["west_locations"]
south_locations = bracket_data["south_locations"]
midwest_locations = bracket_data["midwest_locations"]
locations = [east_locations, west_locations, south_locations, midwest_locations]
# print(east)

bracket_list = east + west + south + midwest
# print (bracket_list)

d = 4


def pickWinner(t1, t2, field, site):
    # s1, s2 = search.getScores(t1, t2, Fal
    # se, depth=d)
    s1, s2, chance = search.machineLearning(t1, t2, field, site)
    winner = t1
    loser = t2

    losing_score = round((1-chance) * 1000)/1000
    winning_score = round((chance) * 1000)/1000
    # if s1 < s2:
    if s1 > s2:
        winner = t2
        loser = t1
        print(winner, "beats", loser, ":",
              winning_score * 100, "-", losing_score * 100)
    else:
        print(winner, "beats", loser, ":",
              winning_score * 100, "-", losing_score * 100)
    return winner, loser, winning_score


c = copy.deepcopy(bracket_list)
for team in bracket_list:
    if "/" in team["team"]:
        seed = team["seed"]
        c.remove(team)
        t1, t2 = team["team"].split(" / ")
        newT1 = {"seed": seed, "team": t1}
        newT2 = {"seed": seed, "team": t2}
        c.append(newT1)
        c.append(newT2)

for idx, team in enumerate(bracket_list):
    team["overall_chance"] = 1.0
    team["matchup_chance"] = 1.0
    if "/" in team["team"]:

        t1, t2 = team["team"].split(" / ")

        # s2 = search.getScores(t2, t1)
        winner, loser, odds = pickWinner(t1, t2, c)
        team["team"] = winner
        team["overall_chance"] = float(odds)
        team["matchup_chance"] = float(odds)
        # print(t1, s1, t2, s2)
# print(bracket_list)
data = {}
data["method"] = "Closest to Toruney Site"
data["round_of_64"] = copy.deepcopy(bracket_list)

# with open("result_bracket.json", "r") as f:
#     data = json.load(f)
with open("result_bracket.json", "w+") as f:
    f.write("")
# '''
old_list = bracket_list
new_list = bracket_list
while len(old_list) > 1:
    list_copy = copy.deepcopy(old_list)
    list_len = len(old_list)
    for i in range(0, int(list_len/2)):
        t1 = old_list[i]
        t2 = old_list[i+1]
        site = ""
        if len(list_copy) > 16:
            region_num = math.floor((i) / (len(list_copy)/8))
            site_num = math.floor(i / (len(list_copy)/32)) % 4
            # print(locations[region_num], locations[region_num][site_num])
            site = locations[region_num][site_num]
            print(site)
        elif len(list_copy) > 4:
            region_num = math.floor(i / (len(list_copy)/8))
            print(locations[region_num], locations[region_num][4])
            site = locations[region_num][4]
            print(site)
        else:
            site = "Minneapolis, MN"

        winner, loser, chance = pickWinner(t1["team"], t2["team"], list_copy, site)

        if(t1["team"] == loser):
            loser = t1
            # winner = t1
        else:
            loser = t2
            # winner = t1
        # print(loser)
        new_list.remove(loser)
        # print(new_list[winner])
        c = copy.deepcopy(list(filter(lambda x: x["team"] == winner, old_list))[
                          0]["overall_chance"])
        list(filter(lambda x: x["team"] == winner, new_list))[
            0]["overall_chance"] = float(c * chance)
        list(filter(lambda x: x["team"] == winner, new_list))[
            0]["matchup_chance"] = float(chance)
        # new_list = [t for t in new_list if t["team"] != loser]
    # print(new_list)
    print("\n" + "Round Of "+str(len(old_list)) + "\n")
    old_list = new_list
    data["round_of_"+str(len(old_list))] = copy.deepcopy(old_list)
'''
for team in data["round_of_64"]:
    overall_chance = 1
    rounds = ["round_of_64", "round_of_32", "round_of_16", "round_of_8", "round_of_4", "round_of_2"]
    index = 64
    arrNum = 0
    arr = data[rounds[arrNum]]
    team_name = team["team"]
    index = list(map(lambda x: x['team'], arr)).index(team_name)
    data[team_name] = {}
    while arrNum < 6:
        arr = data[rounds[arrNum]]
        opponent_idx = index - (index % 2)
        if opponent_idx == index:
            opponent_idx += 1
        # print(opponent_idx)
        opponent_name = arr[opponent_idx]["team"]
        # print(team_name, "vs", opponent_name)
        winner, loser, chance = pickWinner(team_name, opponent_name, arr)
        res = (1-chance)
        if winner == team_name:
            res = chance
        overall_chance *= res
        index = math.floor(index / 2)
        data[team_name][rounds[arrNum]] = res
        arrNum += 1
    print(overall_chance)
'''
with open("result_bracket.json", "a") as f:
    json.dump(data, f)
# '''