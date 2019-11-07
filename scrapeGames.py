from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json

browser = webdriver.Chrome("chromedriver")
baseUrl = "https://www.sports-reference.com/cbb/boxscores/index.cgi?"
result_dict = {}
result_dict["game_results"] = {}


for year in range(2019, 2020):
    start_month = 1
    end_month = 4
    if year == 2019:
        start_month = 11
        end_month = 12
    for month in range(start_month, end_month + 1):
        for day in range(1, 32):
            url = baseUrl
            url = url + "month=" + str(month)
            url = url + "&day=" + str(day)
            url = url + "&year=" + str(year)
            browser.get(url)
            # time.sleep(2)
            html = browser.execute_script("return document.documentElement.outerHTML")
            soup = BeautifulSoup(html, "html.parser")
            soup.prettify()
            # print(soup)
            for game in soup.findAll("div", {"class": "section_content"})[0].findAll(
                "table", {"class": "teams"}
            ):
                loser = game.findAll("tr", {"class": "loser"})[0]
                losing_team = loser.findAll("td")[0].find("a").string
                losing_link = loser.findAll("td")[0].find("a").get("href")
                losing_score = int(loser.findAll("td", {"class": "right"})[0].string)
                if losing_team in result_dict:
                    result_dict["game_results"][losing_team]["link"] = losing_link
                else:
                    result_dict["game_results"][losing_team] = {}
                    result_dict["game_results"][losing_team]["link"] = losing_link



                winner = game.findAll("tr", {"class": "winner"})[0]
                winning_team = winner.findAll("td")[0].find("a").string
                winning_link = winner.findAll("td")[0].find("a").get("href")
                winning_score = int(winner.findAll("td", {"class": "right"})[0].string)
                if winning_team in result_dict:
                    result_dict["game_results"][winning_team]["link"] = winning_link
                    if losing_team in result_dict["game_results"][winning_team]["opponent_scores"]:
                        # if losing_team in result_dict["opponents"]:
                        #     if winning_team in result_dict["opponents"][losing_team]: # team lost after playing second time

                        result_dict["game_results"][winning_team]["opponent_scores"][losing_team] += (
                            winning_score - losing_score
                        )
                    else:
                        result_dict["game_results"][winning_team]["opponent_scores"][losing_team] = (
                            winning_score - losing_score
                        )
                else:
                    result_dict["game_results"][winning_team] = {}
                    result_dict["game_results"][winning_team]["opponent_scores"] = {}
                    result_dict["game_results"][winning_team]["link"] = winning_link
                    result_dict["game_results"][winning_team]["opponent_scores"][losing_team] = (
                        winning_score - losing_score
                    )
            # print(result_dict)
            print("Completed ", month, "/", day, "/", year)
            with open("games.json", "w") as outfile:
                json.dump(result_dict, outfile)
