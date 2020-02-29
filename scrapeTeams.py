from selenium import webdriver
import requests
import time
import json
import re

# browser = webdriver.Chrome("chromedriver")
baseUrl = "https://www.sports-reference.com/"
result_dict = {}

# This file goes through every team that appeared in a game and pulls the data seen below
# The issue is I always had to re-run it when I had a new datapoint idea
# TODO: Maybe store the entire html and then parse that as needed?
# would be a lot faster than having to pull each page each new idea


def transformTeamName(t):
    switches = {
        "UCF": "Central Florida",
        "Penn": "Pennsylvania",
        "Central Connecticutt": "Central Connecticutt State",
        "LIU-Brooklyn": "Long Island University",
        "UMass": "Massachusetts",
        "UNC Greensboro": "north carolina greensboro",
        "NC State": "north carolina state",
        "Pitt": "pittsburgh",
    }

    for s in switches:
        if t == s:
            t = switches[s]
    return (
        t.lower()
        .replace(" ", "-")
        .replace("(", "")
        .replace(")", "")
        .replace("'", "")
        .replace(".", "")
        .replace("&", "")
    )


def getHTML(url):
    # browser.get(url)
    r = requests.get(url)
    html = r.text
    # html = browser.execute_script("return document.documentElement.outerHTML")
    return html


teamdata = {}
data = {}
with open("games.json", "r+") as readfile:
    game_data = json.load(readfile)
    data["html"] = {}
    results = game_data["game_results"]
    teams_with_wins = dict()
    for (key, value) in results.items():
        if bool(value["wins"]) == True and value["link"] != None:
            teams_with_wins[key] = value
    total_known_teams = len(list(teams_with_wins.keys()))
    
    with open("html.json", "w") as writefile:
        for idx, team in enumerate(teams_with_wins):
            print(str(idx) + "/" + str(total_known_teams), team)
            if teams_with_wins[team]["link"] is not None:
                url = baseUrl + teams_with_wins[team]["link"]
                html = getHTML(url)
                data["html"][team] = html
                writefile.seek(0)
                json.dump(data, writefile, indent=4)
                writefile.truncate()
