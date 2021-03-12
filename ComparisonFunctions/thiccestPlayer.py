from ComparisonFunctions.CompareFunction import CompareFunction


def compareTeams(t1, t2, data):
    weights1 = list(map(lambda x: x[1]["weight"], data[t1]["players"].items()))
    weights2 = list(map(lambda x: x[1]["weight"], data[t2]["players"].items()))
    t1_score = max(weights1)
    t2_score = max(weights2)
    odds = max(t1_score / (t1_score + t2_score), t2_score / (t1_score + t2_score))
    return t1_score, t2_score, odds


comparison = CompareFunction(wantHighest=True, comparison=compareTeams)
