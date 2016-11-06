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

# Initialize MLB Teams
echo "Initializing MLB Teams"
python ./mlb-importer.py $DB ./fixtures/mlb.csv

# Initialize FG Data
FILES=./fixtures/fg-*.csv

for f in $FILES
do
    echo "Importing data from $f"
    python ./fg-importer.py $DB $f
done
