#!/bin/bash

# Only uncomment if needing to reinitialize the database. All local data will be lost.
#flask --app cookr init-db
python3 -m venv .venv
. .venv/bin/activate
flask --app cookr run --debug
echo "Website: http://127.0.0.1:5000/"