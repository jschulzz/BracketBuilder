from functools import reduce
from geopy import Nominatim
from geopy import distance
import re

#TODO: This requires refactor to include Site location in the data

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
    site = "Canada?"
    starters = getStarters(data[team]["players"])

    geolocator = Nominatim(user_agent="CBBScraping")
    school = geolocator.geocode(searchfor(team), addressdetails=True, timeout=10)
    if school.raw["address"]["country_code"] != "us":
        print(school)
    site_loc = geolocator.geocode(site, addressdetails=True, timeout=10)
    schoolLocation = (school.latitude, school.longitude)
    site_coords = (site_loc.latitude, site_loc.longitude)
    score = distance.distance(site_coords, schoolLocation).miles
    return score


comparison = CompareFunction(wantHighest=False, comparison=compareTeams)
