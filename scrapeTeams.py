from selenium import webdriver
import time
import json
import re

browser = webdriver.Chrome("chromedriver")
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
    browser.get(url)
    html = browser.execute_script("return document.documentElement.outerHTML")
    return html


teamdata = {}
data = {}
with open("games.json", "r+") as f:
    data = json.load(f)
    data["html"] = {}
    results = data["game_results"]
    total_known_teams = len(list(results.keys()))
    for idx, team in enumerate(results):
        print(str(idx) + "/" + str(total_known_teams), team)
        # if data[team].get("player_pts", []) != [] or data[team]["link"] == None:
        #     continue
        if results[team]["link"] is not None:
            url = baseUrl + results[team]["link"]
            html = getHTML(url)
            data["html"][team] = html
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
