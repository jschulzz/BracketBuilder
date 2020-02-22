from bs4 import BeautifulSoup
import json
import re


def getHeaderStat(name):
    try:
        origin = soup.find(text=re.compile(name))
        parent = origin.parent.parent
        if name is "SOS":
            parent = parent.parent
        value = float(parent.getText().split(" ")[1])
        return value
    except:
        print("No",name)
        return 1


def getPlayerStat(name, comparator, isInt):
    if isInt:
        stats = list(
            map(
                lambda x: int(float(x.get("csk", -1))),
                soup.find_all("td", attrs={"data-stat": name}),
            )
        )
    else:
        stats = list(
            map(
                lambda x: str(x.get("csk", "_")),
                soup.find_all("td", attrs={"data-stat": name}),
            )
        )

    filtered_stats = list(filter(comparator, stats))
    return filtered_stats


def getPlayerInfo(name, comparator):
    stats = list(
        map(
            lambda x: int(x.string) if x.string != None else -1,
            soup.find_all("td", attrs={"data-stat": name}),
        )
    )
    filtered_stats = list(filter(comparator, stats))
    return filtered_stats


with open("html.json", "r+") as htmlfile:
    with open("games.json", "r+") as gamefile:
        with open("stats.json", "w") as statfile:
            html = json.load(htmlfile)
            games = json.load(gamefile)
            scraped_stats = {}
            scraped_stats["team_stats"] = {}
            game_results = games.get("game_results")
            html_list = html.get("html")
            for idx, team in enumerate(html_list):
                print("Parsing", team, "-", idx)
                soup = BeautifulSoup(html_list.get(team), "html.parser")
                soup.prettify()

                # specific player stats
                heights = getPlayerStat("height", lambda x: x > 0, True)
                weights = getPlayerStat("weight", lambda x: x > 0, True)
                nums = getPlayerInfo("number", lambda x: x != -1)
                hometowns = getPlayerInfo("homewtown", lambda x: x != -1)
                player_pts = getPlayerStat("summary", lambda x: x != "_" and x[:2] != "0-", False)
                player_pts = list(
                    map(lambda x: int(x.split("-")[1]) / int(x.split("-")[0]), player_pts)
                )

                # general team stats/data
                logo_url = soup.find_all("img", attrs={"class": "teamlogo"})[0]["src"]
                O_rtg = getHeaderStat("ORtg:")
                D_rtg = getHeaderStat("DRtg:")
                SOS = getHeaderStat("SOS")
                PS = getHeaderStat("PS/G:")
                PA = getHeaderStat("PA/G:")

                scraped_stats["team_stats"][team] = {}
                try:
                    team_stats_row = soup.find("table", attrs={"id": "team_stats"}).find_all("tr")[
                        1
                    ]
                    for data_tag in team_stats_row.find_all("td"):
                        stat = data_tag["data-stat"]
                        scraped_stats["team_stats"][team][stat] = float(data_tag.string)
                except:
                    continue
                if nums == []:
                    print(team)

                scraped_stats["team_stats"][team]["weights"] = weights
                scraped_stats["team_stats"][team]["heights"] = heights
                scraped_stats["team_stats"][team]["jersey_nums"] = nums
                scraped_stats["team_stats"][team]["hometowns"] = hometowns
                scraped_stats["team_stats"][team]["player_pts"] = player_pts
                scraped_stats["team_stats"][team]["offensive"] = O_rtg
                scraped_stats["team_stats"][team]["defensive"] = D_rtg
                scraped_stats["team_stats"][team]["sos"] = SOS
                scraped_stats["team_stats"][team]["points_scored"] = PS
                scraped_stats["team_stats"][team]["points_against"] = PA
                scraped_stats["team_stats"][team]["logo_url"] = logo_url
                scraped_stats["team_stats"][team]["wins"] = game_results[team]["wins"]
                statfile.seek(0)
                json.dump(scraped_stats, statfile, indent=4)
                statfile.truncate()