import json
import compareFns
import numpy as np
import copy
import math

bracket_data = {}
with open("bracketology.json") as f:
    bracket_data = json.load(f)

sortorder = [0, 15, 7, 8, 4, 11, 3, 12, 5, 10, 2, 13, 6, 9, 1, 14]


east = list(np.array(bracket_data["E"])[sortorder])
midwest = list(np.array(bracket_data["M"])[sortorder])
west = list(np.array(bracket_data["W"])[sortorder])
south = list(np.array(bracket_data["S"])[sortorder])
# east_locations = bracket_data["east_locations"]
# west_locations = bracket_data["west_locations"]
# south_locations = bracket_data["south_locations"]
# midwest_locations = bracket_data["midwest_locations"]
# locations = [east_locations, west_locations, south_locations, midwest_locations]

bracket_list = east + west + south + midwest

d = 4


def pickWinner(team1, team2, field, site):
    scoreOfT1, scoreofT2, chance = compareFns.efficiencyMarginWithSOS(team1, team2, field)
    want_highest = True
    # want_highest depends on the compareFn used
    winning_score = round((chance) * 1000) / 1000
    losing_score = round((1 - chance) * 1000) / 1000
    if (want_highest and scoreOfT1 > scoreofT2) or (
        not want_highest and scoreOfT1 < scoreofT2
    ):
        print(team1, "beats", team2, ":", winning_score * 100, "-", losing_score * 100)
        return team1, team2, winning_score
    else:
        print(team2, "beats", team1, ":", winning_score * 100, "-", losing_score * 100)
        return team2, team1, winning_score


def splitPlayIns(team):
    seed = team["seed"]
    t1, t2 = team["name"].split(" / ")
    newT1 = {"seed": seed, "name": t1}
    newT2 = {"seed": seed, "name": t2}
    return newT1, newT2


def getSite(remaining_bracket, locations):
    site = ""
    if len(remaining_bracket) > 16:
        region_num = math.floor((i) / (len(remaining_bracket) / 8))
        site_num = math.floor(i / (len(remaining_bracket) / 32)) % 4
        site = locations[region_num][site_num]
        print(site)
    elif len(remaining_bracket) > 4:
        region_num = math.floor(i / (len(remaining_bracket) / 8))
        site = locations[region_num][4]
        print(locations[region_num], locations[region_num][4])
        print(site)
    else:
        site = "Minneapolis, MN"  # Final Site at time of update
    return site


c = copy.deepcopy(bracket_list)
for team in bracket_list:
    print(team)
    if "/" in team["name"]:
        c.remove(team)
        t1, t2 = splitPlayIns(team)
        c.append(t1)
        c.append(t2)


# quickly decide the winners of the play-ins
for idx, team in enumerate(bracket_list):
    team["overall_chance"] = 1.0
    team["matchup_chance"] = 1.0
    if "/" in team["name"]:
        t1, t2 = team["name"].split(" / ")
        winner, loser, odds = pickWinner(t1, t2, c, "Dayton, OH")
        team["name"] = winner
        team["overall_chance"] = float(odds)
        team["matchup_chance"] = float(odds)

filename = "client/src/result_bracket.json"
data = {}
data["round_of_64"] = copy.deepcopy(bracket_list)

with open(filename, "w+") as f:
    f.write("")

old_list = bracket_list
new_list = bracket_list

while len(old_list) > 1:
    list_copy = copy.deepcopy(old_list)
    list_len = len(old_list)
    for i in range(0, int(list_len / 2)):
        t1 = old_list[i]
        t2 = old_list[i + 1]
        site = "Canada"
        # site = getSite(list_copy, locations)
        winner_name, loser_name, chance = pickWinner(
            t1["name"], t2["name"], list_copy, site
        )

        losing_team = None
        if t1["name"] == loser_name:
            losing_team = t1
        else:
            losing_team = t2
        new_list.remove(losing_team)

        previous_chance = copy.deepcopy(
            list(filter(lambda x: x["name"] == winner_name, old_list))[0][
                "overall_chance"
            ]
        )
        list(filter(lambda x: x["name"] == winner_name, new_list))[0][
            "overall_chance"
        ] = float(previous_chance * chance)
        list(filter(lambda x: x["name"] == winner_name, new_list))[0][
            "matchup_chance"
        ] = float(chance)
    print("\n" + "Round Of " + str(len(old_list)) + "\n")
    old_list = new_list
    data["round_of_" + str(len(old_list))] = copy.deepcopy(old_list)

with open(filename, "a") as f:
    json.dump(data, f)
