// Connect to the local 'energy_db' MongoDB database
db = connect( 'mongodb://localhost/energy_db' );

// Create the 'gaz_elec_energy_tb' collection in the database
db.createCollection("gaz_elec_energy_tb")

// Create the 'gaz_energy_tb' collection in the database
db.createCollection("gaz_energy_tb")

// Create the 'gaz_industriel_energy_tb' collection in the database
db.createCollection("gaz_industriel_energy_tb")
