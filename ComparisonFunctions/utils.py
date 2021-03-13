import re

replacements = {
    "Prairie View A&M": "Prairie View",
    "\(pa\)": "(PA)",
    "North Carolina$": "UNC",
    "Ucf$": "UCF",
    "Saint John's$": "St. John's (NY)",
    "Saint Peter's$": "St. Peter's",
    "UC Irvine$": "UC-Irvine",
    "Liu Brooklyn$": "LIU-Brooklyn",
    "East Tennessee State$": "ETSU",
    "Charleston": "College of Charleston",
    "UT Arlington": "Texas-Arlington",
    "Bowling Green": "Bowling Green State",
    "N.C. A&T": "North Carolina A&T;",
    "Brigham Young": "BYU",
    "UNCG": "UNC Greensboro",
    "Loyola Chicago": "Loyola (IL)",
    "W\. Kentucky": "Western Kentucky",
    "Norfolk St\.": "Norfolk State",
    "Colorado St\.": "Colorado State",
    "Oklahoma St\.": "Oklahoma State",
    "Michigan St\.": "Michigan State",
    "Florida St\.": "Florida State",
    "Cleveland St\.": "Cleveland State",
    "Wichita St\.": "Wichita State",
    "Morehead St\.": "Morehead State",
    "San Diego St\.": "San Diego State",
    "Nicholls St\.": "Nicholls State",
    "Appalachian St\.": "Appalachian State",
}


def replace(t):
    for w in replacements:
        t = re.sub(w, replacements[w], t)
    return t


def fixNames(t1, t2, all_names):
    return (fixName(t1, all_names), fixName(t2, all_names))


def fixName(t, all_names):
    if t not in list(all_names.keys()):
        t = replace(t)
    return t

def getStarters(players):
    player_stats = list(players.values())
    player_stats.sort(key=lambda x: x.get("minutes", 0), reverse=True)
    return player_stats[:5]
