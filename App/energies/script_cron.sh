#!/bin/bash
source /home/khaldi/anaconda3/bin/activate energies_env
year_mnth=$(date +%Y-%m)
cd ./gaz
source ./script_mongo_get_gaz.sh $year_mnth
cd ../gaz_industriel
source ./script_mongo_get_gaz_industriel.sh $year_mnth
cd ../gaz_elec
source ./script_mongo_get_gaz_elec.sh $(cut -c-4 <<< $year_mnth)

