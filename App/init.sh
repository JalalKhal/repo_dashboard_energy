#!/bin/bash
#run script in sudo mode

source /home/khaldi/anaconda3/bin/activate energies_env
#docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=Stackover75" -p 1433:1433 --name sqlserver  -d --network host  mcr.microsoft.com/mssql/server:2022-latest #docker container for SQL Server
#docker run -d --name mongodb --network host mongo:latest #docker container for mongodb
docker cp ./init_mongo.js mongodb:/tmp/init_mongo.js
docker exec -it mongodb mongosh --file /tmp/init_mongo.js

cd ./energies

cd ./gaz

for i in {2011..2023}
  do
    source ./script_mongo_get_gaz.sh $i
    cd ../gaz_industriel
    source ./script_mongo_get_gaz_industriel.sh $i
    cd ../gaz_elec
    source ./script_mongo_get_gaz_elec.sh $i
    cd ../gaz
  done





