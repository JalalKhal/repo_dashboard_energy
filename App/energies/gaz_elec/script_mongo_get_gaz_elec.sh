#!/bin/bash
#sudo mode (run in sudo mode)
#$1: date of gaz data
source ../script_mongo.sh "gaz_elec_tmp.json" "energy_db" "gaz_elec_energy_tb" "https://opendata.agenceore.fr/api/records/1.0/search/?dataset=conso-elec-gaz-annuelle-par-secteur-dactivite-agregee-region&q=&rows=10000&facet=operateur&facet=annee&facet=filiere&facet=libelle_region&refine.annee=$1"