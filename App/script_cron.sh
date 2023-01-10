#!/bin/bash
year_mnth_day=$(date +%Y-%m-%d)
year_mnth=$(date +%Y-%m)
year=$(date +%Y)
cd ./energies
cd ./gaz
source ./script_mongo_get_gaz.sh $year_mnth #monthly update date

cd ../gaz_industriel
source ./script_mongo_get_gaz_industriel.sh $year_mnth_day #daily update of data

cd ../gaz_elec
source ./script_mongo_get_gaz_elec.sh $year #yearly update date

cd ../elec_day
source ./script_mongo_get_elec_day.sh $year_mnth_day #daily update of data

cd ../elec_met
source ./script_mongo_get_elec_met.sh $year_mnth_day #daily update of data
