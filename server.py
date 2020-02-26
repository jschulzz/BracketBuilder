from flask import Flask, request
from flask_cors import CORS
import compareFns
import bracket

app = Flask(__name__)
CORS(app)

@app.route('/challenge', methods=["POST"])
def challengeTeams():
    if request.method == "POST":
        data = request.get_json()
        print(data)
    return 0

@app.route('/')
def getStarterBracket():
    bracket_result = bracket.buildInitialBracket(method=compareFns.efficiencyMargin)
    return bracket_result


if __name__ == "__main__":
    app.run()