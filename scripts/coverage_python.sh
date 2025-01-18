#!/bin/sh
set -e

cd app/server

echo "Installing Dependencies"
sudo apt-get update
sudo apt-get install jq

pip install coverage
pip install pylint 

echo "Checking lint"

pylint src ./migrate_db.py || true
PYLINT_EXIT_CODE=$?

if [ $PYLINT_EXIT_CODE -ne 0 ]; then
  echo "Pylint found issues, but continuing the script..."
else
  echo "Pylint completed successfully."
fi
required_score=9.9
output=$(pylint src ./migrate_db.py --output-format=text || true)

last_line=$(echo "$output" | tail -n 1)

last_second_value=$(echo "$last_line" | awk '{print $(NF-1)}')
lint_score=$(echo "$last_second_value" | awk -F'/' '{print $1}')

echo "Pylint score: $lint_score"

if (( $(echo "$lint_score > $required_score" | bc -l) ))
then
    echo "Pylint score is excellent: $lint_score"
else
    echo "Warning: Pylint score is less than $required_score"
fi

echo "Generating gRPC python service"

python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/broker.proto

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
