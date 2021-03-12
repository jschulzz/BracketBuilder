from flask import Flask, request
from flask_cors import CORS
import compareFns
import bracket
import json

app = Flask(__name__)
CORS(app)

assigned = []

@app.route("/challenge", methods=["POST"])
def challengeTeams():
    global assigned
    if request.method == "POST":
        data = request.get_json(force=True)
        tuples = list(map(lambda arr: (arr["match"][0], arr["match"][1], arr["winner"]), data))
        assigned = tuples
    return "0"


@app.route("/", methods=["POST"])
def getStarterBracket():
    assigned = []
    if request.method == "POST":
        data = request.get_json(force=True)
        tuples = list(map(lambda arr: (arr["match"][0], arr["match"][1], arr["winner"]), data))
        assigned = tuples
    print(assigned)
    bracket_result = bracket.buildInitialBracket(method=compareFns.efficiencyMarginWithSOS, assigned=assigned)
    return bracket_result


@app.route("/team/<team_name>")
def getTeam(team_name):
    data = {}
    with open("stats.json") as stats:
        data = json.load(stats)["team_stats"]
        fixed_name = compareFns.fixName(team_name)
        stats.close()   
    return data[fixed_name]


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
