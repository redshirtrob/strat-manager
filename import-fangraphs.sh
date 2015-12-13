#!/bin/bash

FILES=./fg-data-files/fg-*.csv

for f in $FILES
do
    echo "Importing data from $f"
    python ./fg-importer.py $f
done

