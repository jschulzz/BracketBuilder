from ComparisonFunctions.CompareFunction import CompareFunction


def compareTeams(team, data):
    weights = list(map(lambda x: x[1]["weight"], data[team]["players"].items()))
    score = max(weights)
    return score


comparison = CompareFunction(wantHighest=True, comparison=compareTeams)
