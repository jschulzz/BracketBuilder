import json
import compareFns
import numpy as np
import copy
import math


def mapOdds(chance):
    return max(min(round((chance) * 1000) / 1000, 1.0), 0)


def findWinner(name, search_list):
    return list(filter(lambda x: x["name"] == name, search_list))[0]


def pickWinner(team1, team2, method, field, site):
    scoreOfT1, scoreofT2, chance = method(
        {"team1": team1, "team2": team2, "site": None, "field": None}
    )
    want_highest = True
    # want_highest depends on the compareFn used
    winning_score = mapOdds(chance)
    losing_score = mapOdds(1 - chance)
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
    site = "Indianapolis, IN"
    # if len(remaining_bracket) > 16:
    #     region_num = math.floor((i) / (len(remaining_bracket) / 8))
    #     site_num = math.floor(i / (len(remaining_bracket) / 32)) % 4
    #     site = locations[region_num][site_num]
    #     print(site)
    # elif len(remaining_bracket) > 4:
    #     region_num = math.floor(i / (len(remaining_bracket) / 8))
    #     site = locations[region_num][4]
    #     print(locations[region_num], locations[region_num][4])
    #     print(site)
    # else:
    #     site = "Minneapolis, MN"  # Final Site at time of update
    return site


def buildInitialBracket(method=compareFns.machineLearning, assigned=[]):
    

    sortorder = [0, 15, 7, 8, 4, 11, 3, 12, 5, 10, 2, 13, 6, 9, 1, 14]
    # sortorder = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    print(assigned)
    with open("bracketology.json") as f:
        team_names = json.load(f)
        east = [
            {
                "name": list(np.array(team_names["REGION 1"]))[i],
                "seed": sortorder[i],
                "overall_chance": 1.0,
                "opponent": "",
                "winner": "",
            }
            for i in range(0, 16)
        ]
        midwest = [
            {
                "name": list(np.array(team_names["REGION 2"]))[i],
                "seed": sortorder[i],
                "overall_chance": 1.0,
                "opponent": "",
                "winner": "",
            }
            for i in range(0, 16)
        ]
        west = [
            {
                "name": list(np.array(team_names["REGION 3"]))[i],
                "seed": sortorder[i],
                "overall_chance": 1.0,
                "opponent": "",
                "winner": "",
            }
            for i in range(0, 16)
        ]
        south = [
            {
                "name": list(np.array(team_names["REGION 4"]))[i],
                "seed": sortorder[i],
                "overall_chance": 1.0,
                "opponent": "",
                "winner": "",
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
            t1, t2 = team["name"].split("/")
            winner, loser, odds = pickWinner(t1, t2, method, bracket_list, "Dayton, OH")
            bracket_list[idx]["name"] = winner
            bracket_list[idx]["overall_chance"] = float(odds)
            bracket_list[idx]["matchup_chance"] = float(odds)
            bracket_list[idx]["opponent"] = bracket_list[
                idx + 1 if idx % 2 == 0 else idx - 1
            ]["name"]

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

            if isAssigned(assigned, t1, t2, loser_name):
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
            winner_entry = findWinner(winner_name, next_round)

            previous_chance = copy.deepcopy(
                findWinner(winner_name, this_round)["overall_chance"]
            )
            winner_entry["overall_chance"] = float(previous_chance * chance)
            winner_entry["matchup_chance"] = float(chance)
        for idx, team in enumerate(next_round):
            if len(next_round) > 1:
                opponent_idx = idx + 1 if idx % 2 == 0 else idx - 1
                next_round[idx]["opponent"] = next_round[opponent_idx]["name"]
            else:
                next_round[idx]["opponent"] = ""
        print("\n" + "Round Of " + str(len(this_round)) + "\n")
        data["round_of_" + str(len(this_round))] = copy.deepcopy(this_round)
        past_round = data["round_of_" + str(len(this_round) * 2)]
        for idx, team in enumerate(this_round):
            past_round_idx = idx * 2
            past_round[past_round_idx]["winner"] = team["name"]
            past_round[past_round_idx + 1]["winner"] = team["name"]
        data["round_of_" + str(len(past_round))] = copy.deepcopy(past_round)
        this_round = next_round

        # data["round_of_" + str(len(this_round))] = copy.deepcopy(this_round)

    return data


def isAssigned(assigned, t1, t2, loser_name):
    return (t1["name"], t2["name"], loser_name) in assigned or (
        t2["name"],
        t1["name"],
        loser_name,
    ) in assigned


if __name__ == "__main__":
    filename = "client/src/result_bracket.json"

    data = buildInitialBracket()
    with open(filename, "a") as f:
        json.dump(data, f)
