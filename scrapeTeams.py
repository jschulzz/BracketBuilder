from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

import requests
import time
import json
import re
import sys

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
browser = webdriver.Chrome("chromedriver", chrome_options=options)

# browser = webdriver.PhantomJS()
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
    # r = requests.get(url)
    # html = r.text
    html = browser.page_source
    return html

start_year = 2020
if len(sys.argv) > 1:
    start_year = int(sys.argv[1])

gamefile = "/statfiles/games_" + str(start_year) + ".json"
htmlfile = "/statfiles/html_" + str(start_year) + ".json"



teamdata = {}
data = {}
with open(gamefile, "r+") as readfile:
    game_data = json.load(readfile)
    data["html"] = {}
    results = game_data["game_results"]
    teams_with_wins = dict()
    for (key, value) in results.items():
        if bool(value["wins"]) == True and value["link"] != None:
            teams_with_wins[key] = value
    total_known_teams = len(list(teams_with_wins.keys()))
    
    with open(htmlfile, "w") as writefile:
        for idx, team in enumerate(teams_with_wins):
            print(str(idx) + "/" + str(total_known_teams), team)
            if teams_with_wins[team]["link"] is not None:
                url = baseUrl + teams_with_wins[team]["link"]
                html = getHTML(url)
                data["html"][team] = html
                writefile.seek(0)
                json.dump(data, writefile, indent=4)
                writefile.truncate()
