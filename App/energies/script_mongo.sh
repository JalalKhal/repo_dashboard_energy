#!/bin/bash
#sudo mode (run in sudo mode)
#$1 name of the json tmp file for the data given by curl
#$2 name of mongo DataBase
#$3 name of the collection of mongo DataBase
#$4 url of http request
curl --http1.1 $4 -o ../tmp/$1
docker cp ../tmp/$1 mongodb:/tmp/$1
docker exec mongodb mongoimport --db $2 --collection $3 --file /tmp/$1

# Check the status code of the mongoimport command
if [ $? -eq 0 ]; then
  # Call the Python script if the mongoimport command was successful
  ./script_push_sql.sh
else
  # Do something else if the mongoimport command failed
  echo "mongoimport failed with exit code $?"
fi

rm -r ../tmp/* #delete all content of tmp directory

