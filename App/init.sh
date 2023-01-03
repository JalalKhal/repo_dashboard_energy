#!/bin/bash

# ************************************************************
# This script will allow you install all dependency you've need
# Especially Panda, Docker image,
# ***********************************************************

# !!! run script in sudo mode

a="which python3"
echo $(eval "$a")

mkdir ./energies/tmp

apt-get --yes install curl
apt --yes update
apt --yes install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository --yes "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
apt-cache --yes policy docker-ce
apt --yes install docker-ce

apt-get --yes install odbcinst
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
echo "deb [arch=amd64] https://packages.microsoft.com/ubuntu/21.10/prod impish main" | tee /etc/apt/sources.list.d/mssql-release.list
apt --yes update

apt --yes install msodbcsql18

curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -yum remove mssql-tools unixODBC-utf16-devel
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/msprod.listecho 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
apt-get --yes update
apt-get --yes install mssql-tools unixodbc-dev
apt-get --yes update
apt-get --yes install mssql-tools
#echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
#echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
#source ~/.bashrc




apt --yes install python3-pip
python3 -m pip install -r ./requirements.txt


docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=Stackover75" -p 1433:1433 --name sqlserver  -d --network host  mcr.microsoft.com/mssql/server:2022-latest #docker container for SQL Server
docker run -d --name mongodb --network host mongo:latest #docker container for mongodb
sleep 5

docker cp ./init_mongo.js mongodb:/tmp/init_mongo.js
docker exec -it mongodb mongosh --file /tmp/init_mongo.js


x="/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P 'Stackover75' -Q 'CREATE DATABASE energy_dbs'"
status=$?
y=$(eval "$x")
status=$?

echo $y
# Check the status code of sqlcmd command
while [ $status -ne 0 ];
    do
        y=$(eval "$x")
        status=$?
        sleep 1
    done

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






