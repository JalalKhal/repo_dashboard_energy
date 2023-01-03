#!/usr/bin/env python3
from pymongo import MongoClient
from bson.json_util import dumps
import importlib
import sys
import os
absolute_path = os.path.dirname(__file__)
relative_path="../../"
sys.path.append(os.path.join(absolute_path, relative_path))
"""
sys.argv[1]: relative path (root:./repo_dashboards_ecom) of class ProcessSQLEnergy (exemple:App.energies.gaz.ProcessSQLGaz
sys.argv[2]: ProcessSQLEnergy (exemple:Energy=Gaz)
sys.argv[3]: mongo database name
sys.argv[4]: mongo collection name
"""
module = importlib.import_module(sys.argv[1])
ProcessSQLEnergy= getattr(module,sys.argv[2])
client=MongoClient()
db=client[sys.argv[3]]
cursor=db[sys.argv[4]].find().sort("_id",-1).limit(1)
data_json_str = dumps(list(cursor)[0])
try:
    ProcessSQLEnergy(data_json_str).push_sqlserver()
except Exception as e:
    print(f"Exit program: Exception {e}")
    exit(1)
