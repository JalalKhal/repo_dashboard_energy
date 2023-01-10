#!/bin/bash

# ************************************************************
# This script installs dependencies (librairies,packages...) and
# sets up a Docker environment with a SQL Server and MongoDB Server in
# dockers containers.
# ***********************************************************

# !!! run script in sudo mode
# Make the scripts in the 'energies' directory executable.
chmod +x run_app.sh
chmod +x ./script_cron.sh
chmod +x get_datas.sh
chmod +x ./energies/script_mongo.sh
chmod +x ./energies/gaz/script_mongo_get_gaz.sh
chmod +x ./energies/gaz/script_push_sql.sh
chmod +x ./energies/gaz_elec/script_mongo_get_gaz_elec.sh
chmod +x ./energies/gaz_elec/script_push_sql.sh
chmod +x ./energies/gaz_industriel/script_mongo_get_gaz_industriel.sh
chmod +x ./energies/gaz_industriel/script_push_sql.sh
chmod +x ./energies/elec_day/script_mongo_get_elec_day.sh
chmod +x ./energies/elec_day/script_push_sql.sh
chmod +x ./energies/elec_met/script_mongo_get_elec_met.sh
chmod +x ./energies/elec_met/script_push_sql.sh


chmod +x ./energies/script_sql.py #script python
mkdir ./energies/tmp

# Install packages needed for Docker installation
apt-get --yes install curl
apt --yes update
apt --yes install apt-transport-https ca-certificates curl software-properties-common
# Add the Docker repository and install Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository --yes "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
apt-cache --yes policy docker-ce
apt --yes install docker-ce

# Install packages needed for SQL Server
apt-get --yes install odbcinst
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
echo "deb [arch=amd64] https://packages.microsoft.com/ubuntu/21.10/prod impish main" | tee /etc/apt/sources.list.d/mssql-release.list
apt --yes update

# Install the msodbcsql18 package and the mssql-tools package needed to use sqlalchemy library in python
apt --yes install msodbcsql18

curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -yum remove mssql-tools unixODBC-utf16-devel
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/msprod.listecho 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
apt-get --yes update
apt-get --yes install mssql-tools unixodbc-dev
apt-get --yes update
apt-get --yes install mssql-tools



#install pip for python3
apt --yes install python3-pip
#install depedencies(python libraries for python3 interpreter)
python3 -m pip install -r ./requirements.txt

#stop docker containers if exists and remove them and create new containers
docker stop sqlserver mongodb
docker rm sqlserver mongodb
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=Stackover75" -p 1433:1433 --name sqlserver  -d --network host  mcr.microsoft.com/mssql/server:2022-latest #docker container for SQL Server
docker run -d --name mongodb --network host mongo:latest #docker container for mongodb
sleep 231 # time to load containers

#copy the init_mongo.js script in mongodb docker container (server)
x="docker cp ./init_mongo.js mongodb:/tmp/init_mongo.js"
status=$?
y=$(eval "$x")
status=$?
echo $y
# Check the status code of docker command
while [ $status -ne 0 ];
    do
        y=$(eval "$x")
        status=$?
        sleep 3
    done

#launch init_mongo.js script in mongodb server in the docker container
docker exec -it mongodb mongosh --file /tmp/init_mongo.js

#connection to SQL Server in docker container
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
        sleep 3
    done

source get_datas.sh




