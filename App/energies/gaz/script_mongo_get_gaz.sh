#!/bin/bash
#sudo mode (run in sudo mode)
#$1: date of gaz data
source ../script_mongo.sh "gaz_tmp.json" "energy_db" "gaz_energy_tb" "https://odre.opendatasoft.com/api/records/1.0/search/?dataset=courbe-de-charge-eldgrd-regional-grtgaz-terega&q=&rows=10000&sort=date&Facet=date&facet=operateur&facet=region&refine.date=$1"