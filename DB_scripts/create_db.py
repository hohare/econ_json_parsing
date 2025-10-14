# Script to create database from scratch

import pymongo
import json
from pymongo import MongoClient, InsertOne
import os, glob
import numpy as np
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--path", help="Path to JSON files", default = './data')
parser.add_argument("--dbname", help="DB name", default = 'econdDB')
parser.add_argument("--target", help="ECOND or ECONT", default = 'ECOND')
parser.add_argument("--dbaddress", help="DB name", default = 27017)
args = parser.parse_args()

# utility scripts

from json_uploader import jsonFileUploader



client = pymongo.MongoClient("localhost",args.dbaddress) # Connect to local database

#client.drop_database(args.dbname)

mydatabase = client[args.dbname] # create new database

fnames = list(np.sort(glob.glob(args.path + "/report*.json")))
print("Will add the files located in %s (total %d)"%(args.path,len(fnames)))

## Load all the JSON files in the database
for i, (fname) in enumerate(fnames):

    try:
        jsonFileUploader(fname,mydatabase)
    except Exception as e:
        print(e, fname, i)


#jsonObj = json.load(open("%s/data/report_ECOND_2024-04-17_21-49-01.json"%path,'r'))
   
#x = mycol.insert_one(jsonObj) # Write in DB

# Print written object

#for obj in mydatabase['hex46'].find():
#    print(obj)
