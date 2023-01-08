#!/bin/bash
#execution of all scripts of all energies which get data, insert to mongodb/SQL Server Databases
#After this, all of datas of all energies are stores in mongodb and SQL Server DataBases
cd ./energies
cd ./gaz
for i in {2011..2022}
  do
    source ./script_mongo_get_gaz.sh $i
    cd ../gaz_industriel
    source ./script_mongo_get_gaz_industriel.sh $i
    cd ../gaz_elec
    source ./script_mongo_get_gaz_elec.sh $i
    cd ../elec_day
    source ./script_mongo_get_elec_day.sh $i
    cd ../elec_met
    source ./script_mongo_get_elec_met.sh $i
    cd ../gaz
  done


