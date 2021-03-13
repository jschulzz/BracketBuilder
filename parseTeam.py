from bs4 import BeautifulSoup
import json
import re
import io
import sys
from colorthief import ColorThief
from urllib.request import urlopen


# used for getting stats like SOS, Record, Conference
def getHeaderStat(name):
    try:
        origin = soup.find(text=re.compile(name))
        parent = origin.parent.parent
        if name is "SOS":
            parent = parent.parent
        if name == "Record:":
            return parent.find_all("a")[0].string
        value = float(parent.getText().split(" ")[1])
        return value
    except:
        print("No", name)
        return 1


# used for logistic stats: height, weight, jersey, age
def getPlayerAttr(name, isInt=False, useFullValue=False):
    allValues = soup.find_all("td", attrs={"data-stat": name})
    if name == "player":
        # print(soup.find_all("table", attrs={"id": "roster"})[0])
        allValues = soup.find_all("table", attrs={"id": "roster"})[0].find_all(
            "th", attrs={"data-stat": name}
        )
    wrapper = lambda x: str(x)
    defaultValue = "_"
    if isInt:
        wrapper = lambda x: int(float(x))
        defaultValue = -1
    dataLocation = lambda x: x.get("csk", defaultValue)
    if useFullValue:
        dataLocation = lambda x: x.string
    data = lambda x: dataLocation(x) if dataLocation(x) is not None else defaultValue
    transformer = lambda x: wrapper(data(x))
    stats = list(map(transformer, allValues))
    return stats


# used for game stats
def getPlayerStat(data, stat_name):
    value = data.find_all("td", {"data-stat": stat_name})[0].string
    return float(value) if value is not None else 0.0


start_year = 2020
if len(sys.argv) > 1:
    start_year = int(sys.argv[1])

gameFilename = "statfiles/games_" + str(start_year) + ".json"
htmlFilename = "statfiles/html_" + str(start_year) + ".json"
statsFilename = "statfiles/stats_" + str(start_year) + ".json"

with open(htmlFilename, "r+") as htmlfile:
    with open(gameFilename, "r+") as gamefile:
        with open(statsFilename, "w") as statfile:
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
                player_table = soup.find_all("table", {"id": "per_game"})[0].find_all(
                    "tbody"
                )[0]
                advanced_table = soup.find_all("table", {"id": "advanced"})[0].find_all(
                    "tbody"
                )[0]
                players = {}
                playerNames = getPlayerAttr("player")
                playerNames.pop(0)
                heights = getPlayerAttr("height", isInt=True)
                weights = getPlayerAttr("weight", isInt=True)
                jerseys = getPlayerAttr("number", isInt=True, useFullValue=True)
                hometowns = getPlayerAttr("hometown", useFullValue=True)
                classes = getPlayerAttr("class", useFullValue=True)
                for player_idx, player_name in enumerate(playerNames):
                    players[player_name] = {}
                    players[player_name]["height"] = heights[player_idx]
                    players[player_name]["weight"] = weights[player_idx]
                    players[player_name]["jersey"] = jerseys[player_idx]
                    players[player_name]["hometown"] = hometowns[player_idx]
                    players[player_name]["class"] = classes[player_idx]
                player_stat_names = [
                    "gs",
                    "mp_per_g",
                    "fga_per_g",
                    "fg_per_g",
                    "fg2a_per_g",
                    "fg2_per_g",
                    "fg3a_per_g",
                    "fg3_per_g",
                    "fta_per_g",
                    "ft_per_g",
                    "orb_per_g",
                    "drb_per_g",
                    "ast_per_g",
                    "stl_per_g",
                    "blk_per_g",
                    "tov_per_g",
                    "pf_per_g",
                    "pts_per_g",
                ]
                advanced_stat_names = [
                    "per",
                    "ts_pct",
                    "efg_pct",
                    "fg3a_per_fga_pct",
                    "fta_per_fga_pct",
                    "pprod",
                    "orb_pct",
                    "drb_pct",
                    "trb_pct",
                    "ast_pct",
                    "stl_pct",
                    "blk_pct",
                    "tov_pct",
                    "usg_pct",
                    "obpm",
                    "dbpm",
                    "bpm",
                ]
                for player_html in player_table.find_all("tr"):
                    player = {}
                    player_name = str(
                        player_html.find_all("td", {"data-stat": "player"})[0].get(
                            "csk", ""
                        )
                    )
                    for stat_type in player_stat_names:
                        stat_value = getPlayerStat(player_html, stat_type)
                        readable_stat_name = "unknown"
                        if stat_type == "gs":
                            readable_stat_name = "started"
                        if stat_type == "mp_per_g":
                            readable_stat_name = "minutes"
                        else:
                            readable_stat_name = stat_type.split("_")[0]
                        players[player_name][readable_stat_name] = stat_value
                for advanced_html in advanced_table.find_all("tr"):
                    for stat_type in advanced_stat_names:
                        stat_value = getPlayerStat(advanced_html, stat_type)
                        players[player_name][stat_type] = stat_value


                # general team stats/data
                logo_url = soup.find_all("img", attrs={"class": "teamlogo"})[0]["src"]
                main_color = "000000"
                try:
                    fd = urlopen(logo_url)
                    f = io.BytesIO(fd.read())
                    color_thief = ColorThief(f)
                    c = color_thief.get_palette(color_count=2)[0]
                    main_color = "#%02x%02x%02x" % c
                except:
                    pass

                O_rtg = getHeaderStat("ORtg:")
                D_rtg = getHeaderStat("DRtg:")
                SOS = getHeaderStat("SOS")
                PS = getHeaderStat("PS/G:")
                PA = getHeaderStat("PA/G:")
                conference = getHeaderStat("Record:")

                avg_block = soup.find_all("div", attrs={"class": "footer"})[0]
                experience = float(avg_block.text.split("Exp:")[1].split("Averages")[0])

                scraped_stats["team_stats"][team] = {}
                try:
                    stats_table = soup.find("table", attrs={"id": "schools_per_game"})
                    team_stats_row = stats_table.find_all("tr")[1]
                    for data_tag in team_stats_row.find_all("td"):
                        stat = data_tag["data-stat"]
                        scraped_stats["team_stats"][team][stat] = float(data_tag.string)
                except:
                    print("Could not read generic stats")
                    continue
                if jerseys == []:
                    print(team)

                scraped_stats["team_stats"][team]["players"] = players
                scraped_stats["team_stats"][team]["offensive"] = O_rtg
                scraped_stats["team_stats"][team]["defensive"] = D_rtg
                scraped_stats["team_stats"][team]["sos"] = SOS
                scraped_stats["team_stats"][team]["points_scored"] = PS
                scraped_stats["team_stats"][team]["points_against"] = PA
                scraped_stats["team_stats"][team]["logo_url"] = logo_url
                scraped_stats["team_stats"][team]["main_color"] = main_color
                scraped_stats["team_stats"][team]["wins"] = game_results[team]["wins"]
                scraped_stats["team_stats"][team]["experience"] = experience
                scraped_stats["team_stats"][team]["conference"] = conference
                statfile.seek(0)
                json.dump(scraped_stats, statfile, indent=4)
                statfile.truncate()
