import json
import compareFns
import numpy as np
import copy
import math


def pickWinner(team1, team2, method, field, site):
    scoreOfT1, scoreofT2, chance = method(team1, team2, None)
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


def buildInitialBracket(method=compareFns.efficiencyMarginWithSOS, assigned=[]):

    sortorder = [0, 15, 7, 8, 4, 11, 3, 12, 5, 10, 2, 13, 6, 9, 1, 14]
    print(assigned)
    with open("bracketology.json") as f:
        team_names = json.load(f)
        east = [
            {
                "name": list(np.array(team_names["E"])[sortorder])[i],
                "seed": sortorder[i],
                "overall_chance": 1.0,
                "opponent": ""
            }
            for i in range(0, 16)
        ]
        midwest = [
            {
                "name": list(np.array(team_names["M"])[sortorder])[i],
                "seed": sortorder[i],
                "overall_chance": 1.0,
                "opponent": ""
            }
            for i in range(0, 16)
        ]
        west = [
            {
                "name": list(np.array(team_names["W"])[sortorder])[i],
                "seed": sortorder[i],
                "overall_chance": 1.0,
                "opponent": ""
            }
            for i in range(0, 16)
        ]
        south = [
            {
                "name": list(np.array(team_names["S"])[sortorder])[i],
                "seed": sortorder[i],
                "overall_chance": 1.0,
                "opponent": ""
            }
            for i in range(0, 16)
        ]

    bracket_list = east + west + south + midwest

    for idx, team in enumerate(bracket_list):
        opponent_idx = idx + 1 if idx % 2 == 0 else idx - 1
        bracket_list[idx]["opponent"] = bracket_list[opponent_idx]["name"]

    # quickly decide the winners of the play-ins
    for idx, team in enumerate(bracket_list):
        # print(team)

        name = team["name"]
        team = {}
        team["name"] = name
        team["overall_chance"] = 1.0
        team["matchup_chance"] = 1.0
        team["opponent"] = bracket_list[idx + 1 if idx % 2 == 0 else idx - 1]["name"]
        if "/" in team["name"]:
            t1, t2 = team["name"].split(" / ")
            winner, loser, odds = pickWinner(t1, t2, method, bracket_list, "Dayton, OH")
            bracket_list[idx]["name"] = winner
            bracket_list[idx]["overall_chance"] = float(odds)
            bracket_list[idx]["matchup_chance"] = float(odds)
            bracket_list[idx]["opponent"] = bracket_list[idx + 1 if idx % 2 == 0 else idx - 1]["name"]

    filename = "client/src/result_bracket.json"
    data = {}
    data["round_of_64"] = copy.deepcopy(bracket_list)

    with open(filename, "w+") as f:
        f.write("")

    this_round = bracket_list
    next_round = bracket_list

    while len(this_round) > 1:
        this_round_duplicate = copy.deepcopy(this_round)
        list_len = len(this_round)
        for i in range(0, int(list_len / 2)):
            t1 = this_round[i]
            t2 = this_round[i + 1]
            site = "Canada"
            # site = getSite(this_round_duplicate, locations)
                
            winner_name, loser_name, chance = pickWinner(
                t1["name"], t2["name"], method, this_round_duplicate, site
            )
            chance = max(min(chance, 1.0), 0)
            if (t1["name"], t2["name"], loser_name) in assigned or (t2["name"], t1["name"], loser_name) in assigned:
                print("Match Defined", (t1["name"], t2["name"], loser_name))
                swap = winner_name
                winner_name = loser_name
                loser_name = swap
                chance = 1 - chance


            losing_team = None
            if t1["name"] == loser_name:
                losing_team = t1
            else:
                losing_team = t2
            next_round.remove(losing_team)

            previous_chance = copy.deepcopy(
                list(filter(lambda x: x["name"] == winner_name, this_round))[0][
                    "overall_chance"
                ]
            )
            list(filter(lambda x: x["name"] == winner_name, next_round))[0][
                "overall_chance"
            ] = float(previous_chance * chance)
            list(filter(lambda x: x["name"] == winner_name, next_round))[0][
                "matchup_chance"
            ] = float(chance)
        for idx, team in enumerate(next_round):
            if len(next_round) > 1:
                opponent_idx = idx + 1 if idx % 2 == 0 else idx - 1
                next_round[idx]["opponent"] = next_round[opponent_idx]["name"]
            else:
                next_round[idx]["opponent"] = ""
        print("\n" + "Round Of " + str(len(this_round)) + "\n")
        this_round = next_round
        data["round_of_" + str(len(this_round))] = copy.deepcopy(this_round)

    return data


if __name__ == "__main__":
    filename = "client/src/result_bracket.json"

    data = buildInitialBracket()
    with open(filename, "a") as f:
        json.dump(data, f)
