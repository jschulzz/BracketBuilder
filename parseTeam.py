from bs4 import BeautifulSoup
import json
import re
import io
from colorthief import ColorThief
from urllib.request import urlopen


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
                players = []
                player_table = soup.find_all("table", {"id": "per_game"})[0].find_all("tbody")[0]
                for player_html in player_table.find_all("tr"):
                    player = {}
                    player["name"] = str(player_html.find_all("td", {"data-stat": "player"})[0].get("csk", ""))
                    player["started"] = int(player_html.find_all("td", {"data-stat": "gs"})[0].string)
                    player["minutes"] = float(player_html.find_all("td", {"data-stat": "mp_per_g"})[0].string)
                    player["fga"] = float(player_html.find_all("td", {"data-stat": "fga_per_g"})[0].string)
                    player["fg"] = float(player_html.find_all("td", {"data-stat": "fg_per_g"})[0].string)
                    player["fg2a"] = float(player_html.find_all("td", {"data-stat": "fg2a_per_g"})[0].string)
                    player["fg2"] = float(player_html.find_all("td", {"data-stat": "fg2_per_g"})[0].string)
                    player["fg3a"] = float(player_html.find_all("td", {"data-stat": "fg3a_per_g"})[0].string)
                    player["fg3"] = float(player_html.find_all("td", {"data-stat": "fg3_per_g"})[0].string)
                    player["fta"] = float(player_html.find_all("td", {"data-stat": "fta_per_g"})[0].string)
                    player["ft"] = float(player_html.find_all("td", {"data-stat": "ft_per_g"})[0].string)
                    player["orb"] = float(player_html.find_all("td", {"data-stat": "orb_per_g"})[0].string)
                    player["drb"] = float(player_html.find_all("td", {"data-stat": "drb_per_g"})[0].string)
                    player["ast"] = float(player_html.find_all("td", {"data-stat": "ast_per_g"})[0].string)
                    player["stl"] = float(player_html.find_all("td", {"data-stat": "stl_per_g"})[0].string)
                    player["blk"] = float(player_html.find_all("td", {"data-stat": "blk_per_g"})[0].string)
                    player["tov"] = float(player_html.find_all("td", {"data-stat": "tov_per_g"})[0].string)
                    player["pf"] = float(player_html.find_all("td", {"data-stat": "pf_per_g"})[0].string)
                    player["pts"] = float(player_html.find_all("td", {"data-stat": "pts_per_g"})[0].string)
                    # print(player)
                    players.append(player)
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
                main_color = "000000"
                try:
                    fd = urlopen(logo_url)
                    f = io.BytesIO(fd.read())
                    color_thief = ColorThief(f)
                    c = color_thief.get_palette(color_count=2)[0]
                    main_color = '#%02x%02x%02x' % c
                except:
                    pass
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

                scraped_stats["team_stats"][team]["players"] = players
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
                scraped_stats["team_stats"][team]["main_color"] = main_color
                scraped_stats["team_stats"][team]["wins"] = game_results[team]["wins"]
                statfile.seek(0)
                json.dump(scraped_stats, statfile, indent=4)
                statfile.truncate()
