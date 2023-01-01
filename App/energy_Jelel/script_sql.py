#! /home/khaldi/anaconda3/envs/repo_dashboards_ecom/bin/python
from pymongo import MongoClient
from bson.json_util import dumps
import importlib
import sys
"""
sys.argv[1]: relative path (root:./repo_dashboards_ecom) of class ProcessSQLEnergy (exemple:App.energy_Jelel.gaz.ProcessSQLGaz
sys.argv[2]: ProcessSQLEnergy (exemple:Energy=Gaz)
"""
sys.path.insert(0, "../../../") #insert repo_dashboards_ecom to PYTHONPATH
module = importlib.import_module(sys.argv[1])
ProcessSQLEnergy= getattr(module,sys.argv[2])
client=MongoClient()
db=client.energy_db
cursor=db.gaz_energy_tb.find().sort("_id",-1).limit(1)
data_json_str=dumps(list(cursor)[0])
ProcessSQLEnergy(data_json_str).push_sqlserver()


