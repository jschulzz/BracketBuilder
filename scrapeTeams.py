from bs4 import BeautifulSoup
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


teamdata = {}
with open("games.json", "r+") as f:
    data = json.load(f)
    for team in data:
        print(
            str(list(data.keys()).index(team)) + "/" + str(len(list(data.keys()))), team
        )
        if data[team].get("player_pts", []) != [] or data[team]["link"] == None:
            # if data[team]["link"] == None:
            continue
        url = baseUrl + data[team]["link"]
        browser.get(url)
        html = browser.execute_script("return document.documentElement.outerHTML")
        soup = BeautifulSoup(html, "html.parser")
        soup.prettify()
        logo_url = soup.find_all("img", attrs={"class":"teamlogo"})[0]["src"]
        heights = list(
            map(
                lambda x: int(float(x.get("csk", -1))),
                soup.find_all("td", attrs={"data-stat": "height"}),
            )
        )
        # print(heights)
        heights = list(filter(lambda x: x > 0, heights))
        weights = list(
            map(
                lambda x: int(x.get("csk", -1)),
                soup.find_all("td", attrs={"data-stat": "weight"}),
            )
        )
        weights = list(filter(lambda x: x > 0, weights))
        player_pts = list(
            map(
                lambda x: str(x.get("csk", "_")),
                soup.find_all("td", attrs={"data-stat": "summary"}),
            )
        )
        player_pts = list(filter(lambda x: x != "_" and x[:2] != "0-", player_pts))
        # print(player_pts)
        player_pts = list(
            map(lambda x: int(x.split("-")[1]) / int(x.split("-")[0]), player_pts)
        )
        nums = list(
            map(
                lambda x: int(x.string) if x.string != None else -1,
                soup.find_all("td", attrs={"data-stat": "number"}),
            )
        )
        nums = list(filter(lambda x: x != -1, nums))
        hometowns = list(
            map(
                lambda x: (x.string) if x.string != None else -1,
                soup.find_all("td", attrs={"data-stat": "hometown"}),
            )
        )
        hometowns = list(filter(lambda x: x != -1, hometowns))
        # print(hometowns)
        # O_rtg = soup.find(text=re.compile("ORtg:"))
        O_rtg = float(
            soup.find(text=re.compile("ORtg:")).parent.parent.getText().split(" ")[1]
        )
        D_rtg = float(
            soup.find(text=re.compile("DRtg:")).parent.parent.getText().split(" ")[1]
        )
        SOS = float(
            soup.find("a", text=re.compile("SOS")).parent.parent.getText().split(" ")[1]
        )
        PS = float(
            soup.find(text=re.compile("PS/G:")).parent.parent.getText().split(" ")[1]
        )
        PA = float(
            soup.find(text=re.compile("PA/G:")).parent.parent.getText().split(" ")[1]
        )
        team_stats_row = soup.find("table", attrs={"id": "team_stats"}).find_all("tr")[
            1
        ]

        for data_tag in team_stats_row.find_all("td"):
            stat = data_tag["data-stat"]
            data[team][stat] = float(data_tag.string)
        if nums == []:
            print(team)
        data[team]["weights"] = weights
        data[team]["heights"] = heights
        data[team]["jersey_nums"] = nums
        data[team]["hometowns"] = hometowns
        data[team]["player_pts"] = player_pts
        data[team]["offensive"] = O_rtg
        data[team]["defensive"] = D_rtg
        data[team]["sos"] = SOS
        data[team]["points_scored"] = PS
        data[team]["points_against"] = PA
        data[team]["logo_url"] = logo_url
        # print(data[team])
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
        # data[]
        # print(nums)
