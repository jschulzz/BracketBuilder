from flask import Flask, request
from flask_cors import CORS
import compareFns
import bracket
import json

app = Flask(__name__)
CORS(app)


@app.route("/challenge", methods=["POST"])
def challengeTeams():
    if request.method == "POST":
        data = request.get_json()
        print(data)
    return 0


@app.route("/")
def getStarterBracket():
    bracket_result = bracket.buildInitialBracket(method=compareFns.efficiencyMargin)
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
    app.run()
