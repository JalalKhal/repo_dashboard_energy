#!/bin/bash
#sudo mode (run in sudo mode)
#$1: date of gaz data
source ../script_mongo.sh "elec_day_tmp.json" "energy_db" "elec_day_energy_tb" "https://data.enedis.fr/api/records/1.0/search/?dataset=bilan-electrique-transpose&q=&facet=categorie&refine.jour=$1"