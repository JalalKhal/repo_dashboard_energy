#permissions
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

#run the main application
python3 ./energies/dash_main.py
echo "----- ********* HERE is your App Url  ******************  ----- "
