#!/bin/bash
source ~/anaconda3/bin/activate energies_env
./../script_sql.py "App.energies.gaz.ProcessSQLGaz" "ProcessSQLGaz" "energy_db" "gaz_energy_tb"