#!/bin/bash

# crontab: /bin/bash <PWD>/autocommit.sh
CURDIR=$(dirname "$0")
cd $CURDIR

git fetch origin && git reset --hard origin/main

python3 ./main.py # Run the python script to generate README.md

git add . && git commit -m "Automated commit: $(date)"
git push origin main
