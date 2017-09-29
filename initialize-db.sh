#!/bin/bash

function usage {
    echo "usage: intialize-db.sh <DB File>"
    echo "    DB File: The name of the SQLite file"
    exit 1
}

if [ $# -ne 1 ]; then
    usage
fi

DB=$1

# Create all the tables
echo "Creating the database"
python ./sql-bootstrap.py

# Initialize MLB Teams
echo "Initializing MLB Teams"
./mlb-importer.py $DB ./fixtures/mlb.csv

# Initialize FG Data
FILES=./fixtures/fg-*.csv

for f in $FILES
do
    echo "Importing data from $f"
    ./fg-importer.py $DB $f
done

# Initialize BLB League
echo "Initializing BLB League"
./create-blb.py $DB ./fixtures/blb.json
