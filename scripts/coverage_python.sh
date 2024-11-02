#!/bin/sh
set -e

cd server

echo "installing Dependencies"
sudo apt-get update
sudo apt-get install jq

pip install coverage
pip install pylint 

echo "Checking lint"

pylint src ./migrate_db.py 

echo "Start Testing"

coverage run --source=. --omit=test/\* -m unittest discover -s test 
coverage json
json_val=`jq '.totals.percent_covered' coverage.json` 
coverage_percentage=$(echo "$json_val" | sed 's/\..*//')

echo "coverage $coverage_percentage"

required_coverage=98

if [ $coverage_percentage -gt $required_coverage ]
then
    echo 'Test coverage passed'
    coverage html
    exit 0
else
    echo 'Test coverage failed'
    exit 1
fi
