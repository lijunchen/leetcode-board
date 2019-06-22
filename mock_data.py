import datetime
import random
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient()
    Record = client["lcboard"]["Record"]
    User = client["lcboard"]["User"]

    Record.delete_many({})
    User.delete_many({})
    users = [(f"user{i}", "us") for i in range(10)]

    for i in range(10):
        User.insert({"id": i, "username": f"user{i}", "location": "us",
                     "avatar": "https://assets.leetcode.com/users/"})

    for user, location in users:
        for i in range(0, 90):
            crawler_time = datetime.datetime(2019, 6, 1, 23, 39, 59, 0) + datetime.timedelta(days=i)
            submissions = random.randint(0, 10)
            solved = 11
            while solved > submissions:
                solved = random.randint(0, 10)
            Record.insert({"username": user, "submission": submissions, "solved": solved, "date": crawler_time})
    for user, location in users:
        for i in range(0, 90):
            crawler_time = datetime.datetime(2019, 6, 1, 23, 59, 59, 0) + datetime.timedelta(days=i)
            submissions = random.randint(0, 10)
            solved = 11
            while solved > submissions:
                solved = random.randint(0, 10)
            Record.insert({"username": user, "submission": submissions, "solved": solved, "date": crawler_time})
    for user in User.find({}):
        print(user)
    for record in Record.find({}):
        print(record)
