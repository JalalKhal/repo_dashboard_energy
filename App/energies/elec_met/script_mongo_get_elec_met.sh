#!/bin/bash
#sudo mode (run in sudo mode)
#$1: date of gaz data
source ../script_mongo.sh "elec_met_tmp.json" "energy_db" "elec_met_energy_tb" "https://odre.opendatasoft.com/api/records/1.0/search/?dataset=eco2mix-metropoles-tr&q=&rows=10000&sort=date_heure&facet=libelle_metropole&facet=nature&facet=date_heure&refine.date_heure=$1"