import os
import json
from random import  SystemRandom
from flask import Flask, abort
app = Flask(__name__)

jsons = {
    "1": [],
    "2": [],
    "3": [],
    "4": [],
    "5": [],
    "6": [],
}

randomizer = SystemRandom()


@app.route("/tesla/<num>")
def measurement(num):
    if int(num) > 6 or int(num) < 1:
        return abort(404)

    return randomizer.choice(jsons[str(num)])


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == "__main__":
    for filename in os.listdir("example_data"):
        with open(f"example_data/{filename}", "r") as f:
            d = json.loads(f.read())
            jsons[filename.split("_")[1]].append(d)

    app.run(host="0.0.0.0", port=3000, debug=True)
