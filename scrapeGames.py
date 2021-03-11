from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import json
import sys

# browser = webdriver.Chrome("chromedriver")
baseUrl = "https://www.sports-reference.com/cbb/boxscores/index.cgi?"
result_dict = {}
result_dict["game_results"] = {}

start_year = 2020
if len(sys.argv) > 1:
    start_year = int(sys.argv[1])

filename = "games_" + str(start_year) + ".json"


for year in [start_year, start_year + 1]:
    start_month = 1
    end_month = 4
    if year == start_year:
        start_month = 11
        end_month = 12
    for month in range(start_month, end_month + 1):
        start_day = 1
        end_day = 31
        if month == 11:
            start_day = 5
        for day in range(start_day, end_day + 1):
            url = baseUrl
            url = (
                url + "month=" + str(month) + "&day=" + str(day) + "&year=" + str(year)
            )
            # browser.get(url)
            r = requests.get(url)
            html = r.text

            # time.sleep(2)
            # html = browser.execute_script("return document.documentElement.outerHTML")
            soup = BeautifulSoup(html, "html.parser")
            soup.prettify()
            for game in soup.findAll("div", {"class": "section_content"})[0].findAll(
                "table", {"class": "teams"}
            ):
                loser = game.findAll("tr", {"class": "loser"})[0]
                losing_score_string = loser.findAll("td", {"class": "right"})[0].string
                if losing_score_string is not None:
                    losing_team = loser.findAll("td")[0].find("a").string
                    losing_link = loser.findAll("td")[0].find("a").get("href")
                    losing_score = int(losing_score_string)

                    winner = game.findAll("tr", {"class": "winner"})[0]
                    winning_team = winner.findAll("td")[0].find("a").string
                    winning_link = winner.findAll("td")[0].find("a").get("href")
                    winning_score = int(
                        winner.findAll("td", {"class": "right"})[0].string
                    )
                    if winning_team not in result_dict["game_results"]:
                        result_dict["game_results"][winning_team] = {}
                        result_dict["game_results"][winning_team]["wins"] = {}
                    result_dict["game_results"][winning_team]["link"] = winning_link
                    result_dict["game_results"][winning_team]["wins"][losing_team] = (
                        winning_score - losing_score
                    )

                    if losing_team not in result_dict["game_results"]:
                        result_dict["game_results"][losing_team] = {}
                        result_dict["game_results"][losing_team]["wins"] = {}
                    result_dict["game_results"][losing_team]["link"] = losing_link
                else:
                    continue
            print("Completed ", month, "/", day, "/", year)
            with open(filename, "w") as outfile:
                json.dump(result_dict, outfile)
