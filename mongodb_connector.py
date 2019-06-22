from pymongo import MongoClient

client = MongoClient()

Record = client["lcboard"]["Record"]


def clear_db():
    Record.delete_many({})


if __name__ == "__main__":
    clear_db()
    import datetime
    Record.insert({"username": "lee215", "submission": 3, "solved": 2, "date": datetime.datetime.now()})
    Record.insert({"username": "lee215", "submission": 5, "solved": 4, "date": datetime.datetime.now()})
    Record.insert({"username": "lee215", "submission": 7, "solved": 6, "date": datetime.datetime.now()})
    Record.insert({"username": "lee215", "submission": 9, "solved": 8, "date": datetime.datetime.now()})
    records = Record.find({})
    for record in records:
        print(record)
