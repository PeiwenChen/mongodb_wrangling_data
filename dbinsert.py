import json
import pprint

def insert_data(data, db):

    db.arachnid.insert(data)
    pass


if __name__ == "__main__":
    
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples

    with open('arachnid.json') as f:
        data = json.loads(f.read())
        insert_data(data, db)
        pprint.pprint(db.arachnid.find_one())
