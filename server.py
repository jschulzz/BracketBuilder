from flask import Flask, request
import compareFns
import bracket

app = Flask(__name__)

@app.route('/challenge', methods=["POST"])
def challengeTeams():
    if request.method == "POST":
        data = request.get_json()
        print(data)
    return 0

@app.route('/')
def getStarterBracket():
    bracket_result = bracket.buildInitialBracket(method=compareFns.machineLearning)
    return bracket_result


if __name__ == "__main__":
    app.run()