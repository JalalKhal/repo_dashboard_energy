#!/bin/bash
source ~/anaconda3/bin/activate energies_env
./../script_sql.py "App.energies.gaz_elec.ProcessSQLGazElec" "ProcessSQLGazElec" "energy_db" "gaz_elec_energy_tb"