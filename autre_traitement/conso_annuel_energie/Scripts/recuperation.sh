#!/bin/bash

# Komlan Godwin AMEGAH
# made in 10 nov 2022
# copyright - 2022-ue_linux


######## Version with horodate - Using curl #########

# you can get same result using <wget>
# get current time
current_time=$(date "+%Y.%m.%d-%H.%M.%S")
echo "Current Time : $current_time"

file_name="/home/godwin/Documents/Uparis/M1MLSD/ue_linux/projet/App/Data/conso-elec-gaz-annuelle-par-secteur-dactivite-agregee-region"
ext="json"
new_fileName=$file_name-$current_time."-sh".$ext

# Retrieve data from url and store it as new_json_file
curl "https://opendata.agenceore.fr/api/records/1.0/search/?dataset=conso-elec-gaz-annuelle-par-secteur-dactivite-agregee-region&q=&rows=3000&facet=operateur&facet=annee&facet=filiere&facet=libelle_region" -o "$new_fileName"


# just for displaying
# shellcheck disable=SC2028
echo "\n New FileName: " "$new_fileName"

# store data onto Mongo db database
