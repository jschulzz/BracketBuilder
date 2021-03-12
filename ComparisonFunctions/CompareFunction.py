import json
from ComparisonFunctions.utils import fixNames

class CompareFunction:
    data = {}
    with open("stats_2020.json") as f:
        data = json.load(f)["team_stats"]
        
    def __init__(self, wantHighest, comparison):
        self.wantHighest = wantHighest
        self.comparison = comparison
    def compare(self, t1, t2):
        t1, t2 = fixNames(t1, t2, self.data)
        result = self.comparison(t1, t2, self.data)
        return result