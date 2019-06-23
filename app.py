from lxml import html
from flask import json
import flask
import gevent
import requests
import datetime as dt
import time
import datetime
from gevent.pywsgi import WSGIServer
from flask import Flask
from pymongo import MongoClient
import datetime
from collections import defaultdict
from pymongo import MongoClient
from utils import get_today_datetime
import pymongo
from typing import Tuple
from utils import get_today_datetime
from flask_cors import CORS
from flask import jsonify
from flask import render_template

app = Flask(__name__)
CORS(app)


def init():
    client = MongoClient()
    User = client["lcboard"]["User"]
    Config = client["lcboard"]["Config"]
    Record = client["lcboard"]["Record"]
    User.delete_many({})
    Config.delete_many({})
    Record.delete_many({})

    # Config.insert({"id": 0, "start": get_today_datetime(timezone=8)})
    Config.insert({"id": 0, "start": datetime.datetime(2019, 6, 1)})

    with open("userlist.txt") as fp:
        users = [tuple(line.strip().split(" ")) for line in fp]
    for username, location in users:
        User.insert({"username": username, "location": location,
                     "avatar": "https://assets.leetcode.com/users/"})


def get_sub_and_sol_of_day(Record: pymongo.collection, username: str, date: datetime) -> Tuple[int, int]:
    all_record = []
    records = Record.find({"username": username, "date": {"$gte": date, "$lt": date + datetime.timedelta(days=1)}})
    for record in records:
        all_record.append((record["submission"], record["solved"], record["date"]))
    all_record.sort(key=lambda r: r[2])
    if all_record:
        return all_record[-1][0], all_record[-1][1]
    return 0, 0


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/api/test")
def test():
    client = MongoClient()
    Record = client["lcboard"]["Record"]
    User = client["lcboard"]["User"]
    Config = client["lcboard"]["Config"]
    START = Config.find_one({"id": 0})["start"]
    # START = datetime.datetime(2019, 6, 1)
    users = {}
    data = []
    username_arr = []
    resp = {"users": users, "data": data, "username_arr": username_arr}
    for user in User.find({}):
        username_arr.append(user["username"])
        users[user["username"]] = {
            "avatar": user["avatar"],
        }

    date = datetime.datetime(START.year, START.month, START.day)
    today = get_today_datetime(timezone=8)
    while date <= today:
        day_info = {}
        day_info["date"] = date.strftime("%m/%d")
        user_solved = {}
        user_today_solved = {}
        user_submission = {}
        for user in users:
            user_submission[user], user_solved[user] = get_sub_and_sol_of_day(Record, user, date)
            user_today_solved[user] = user_solved[user] - get_sub_and_sol_of_day(Record, user, date + datetime.timedelta(days=-1))[1]
            user_today_solved[user] = abs(user_today_solved[user])
        today_solved_pairs = list(user_today_solved.items())
        today_solved_pairs.sort(key=lambda p: (p[1], p[0]))
        winner, winner_solved = today_solved_pairs[-1]
        # print(winner, winner_solved)
        if date == START:
            winner_solved = 0
        day_info["winner"] = {
            "username": winner,
            "sub": user_submission[winner],
            "solved": winner_solved
        }
        sub = []
        solved = []
        for user in User.find({}):
            username = user["username"]
            sub.append(user_submission[username])
            solved.append(user_today_solved[username])
        if date == START:
            solved = [0] * len(solved)
        day_info["all_users"] = {
            "sub": sub,
            "solved": solved
        }
        # print(day_info)
        resp["data"].append(day_info)
        date = date + datetime.timedelta(days=1)
    # print(resp)
    return jsonify(resp)


if __name__ == "__main__":
    http_server = WSGIServer(("0.0.0.0", 80), app)
    http_server.serve_forever()
    # app.run(host="0.0.0.0", port=80, debug=True)
