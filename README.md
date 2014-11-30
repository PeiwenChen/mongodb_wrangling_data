mongodb_wrangling_data
======================

arachnid.csv - raw data
processing.py - preparing dataset:
                                CSV reader read the content; clean data; store to arachnid.json.
arachnid.json - processed dataset for MongoDB

dbinsert.py - insert the arachnid.json documents to MongoDB database

update.py - retrieve a new dict from arachnid2.csv;
            insert the new field into the MongoDB database;


