db = connect( 'mongodb://localhost/energy_db' );
db.createCollection("gaz_elec_energy_tb")
db.createCollection("gaz_energy_tb")
db.createCollection("gaz_industriel_energy_tb")

