#!/bin/bash
source ~/anaconda3/bin/activate energies_env
./../script_sql.py "App.energies.gaz_industriel.ProcessSQLGazIndustriel" "ProcessSQLGazIndustriel" "energy_db" "gaz_industriel_energy_tb"
