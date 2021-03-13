from functools import reduce
from geopy import Nominatim
from geopy import distance
import re

from ComparisonFunctions.CompareFunction import CompareFunction
from ComparisonFunctions.utils import getStarters

searchreplacements = {
    "TCU$": "Texas Christian",
    "Saint Francis": "Saint Francis",
    "UCF": "Central Florida",
    "UC Irvine": "California Irvine",
}


def searchfor(t):
    for w in searchreplacements:
        if re.search(w, t):
            t = searchreplacements[w]
    return t + " University"


def compareTeams(team, data):
    starters = getStarters(data[team]["players"])
    hometowns = list(map(lambda x: x["hometown"], starters))

    geolocator = Nominatim(user_agent="CBBScraping")
    school = geolocator.geocode(searchfor(team), addressdetails=True, timeout=10)
    if school.raw["address"]["country_code"] != "us":
        print(school)
    locs = list(map(lambda x: geolocator.geocode(x, timeout=10), hometowns))
    avgLat = (
        reduce(
            lambda x, y: x + y,
            list(map(lambda x: x.latitude if x != None else 39.86, locs)),
        )
        / 5
    )
    avgLon = (
        reduce(
            lambda x, y: x + y,
            list(map(lambda x: x.longitude if x != None else -98.6, locs)),
        )
        / 5
    )
    avgLocation = (avgLat, avgLon)
    schoolLocation = (school.latitude, school.longitude)

    score = distance.distance(avgLocation, schoolLocation).miles
    return score


comparison = CompareFunction(wantHighest=False, comparison=compareTeams)
