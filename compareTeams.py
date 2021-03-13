import sys
from ComparisonFunctions import CompareFunction
from ComparisonFunctions.efficiencyWithSOS import comparison
from bracket import pickWinner

if __name__ == "__main__":
    team1 = sys.argv[1]
    team2 = team1
    if len(sys.argv) > 2:
        team2 = sys.argv[2]
    pickWinner(team1, team2, comparison)
