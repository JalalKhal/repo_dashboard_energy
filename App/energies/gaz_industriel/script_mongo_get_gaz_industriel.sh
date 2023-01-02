#!/bin/bash
#sudo mode (run in sudo mode)
#$1: date of gaz_industriel data
source ../script_mongo.sh "gaz_industriel_tmp.json" "energy_db" "gaz_industriel_energy_tb" "https://odre.opendatasoft.com/api/records/1.0/search/?dataset=consommation-nationale-horaire-de-gaz-donnees-provisoires-grtgaz-terega-v2&q=&rows=10000&sort=date&facet=date&facet=operateur&refine.date=$1"