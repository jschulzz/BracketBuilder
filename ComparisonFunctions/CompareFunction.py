import json
from ComparisonFunctions.utils import fixNames


def defaultOddsFunction(score1, score2):
    return max(score1 / (score1 + score2), score2 / (score1 + score2))


class CompareFunction:
    data = {}
    with open("stats_2020.json") as f:
        data = json.load(f)["team_stats"]

    ###
    # Isolated
    # if a CompareFunction is isolated, it means that we're comparing data completely belonging to the teams individually
    # e.g. Comparing the tallest player is data isolated to the individual teams
    # A non-isolated CompareFunction means that both teams' data needs to be used to calculate the comparison's score
    #
    ###

    def __init__(
        self,
        wantHighest,
        comparison,
        isolated=True,
        symmetric=True,
        oddsFunction=defaultOddsFunction,
    ):
        self.wantHighest = wantHighest
        self.comparison = comparison
        self.isolated = isolated
        self.symmetric = symmetric
        self.oddsFunction = oddsFunction

    def compare(self, t1, t2):
        t1, t2 = fixNames(t1, t2, self.data)
        t1_score = 0
        t2_score = 0
        if self.isolated:
            t1_score = self.comparison(t1, self.data)
            t2_score = self.comparison(t2, self.data)
            odds = self.oddsFunction(t1_score, t2_score)
        else:
            if self.symmetric:
                t1_score = self.comparison(t1, t2, self.data)
                t2_score = self.comparison(t2, t1, self.data)
                odds = self.oddsFunction(t1_score, t2_score)
            else:
                t1_score, t2_score, odds = self.comparison(t1, t2, self.data)

        return t1_score, t2_score, odds
