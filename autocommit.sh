#!/bin/bash

python3 ./main.py # Run the python script to generate README.md

git add . && git commit -m "Automated commit: $(date)"
git push origin main
