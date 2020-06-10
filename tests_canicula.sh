#!/bin/bash

mkdir -p training_logs/killed_ac

./main.py --canicula -n AC --obs_type types -r killed  -e 200 2500 -s c++ -l 0.005 0.9 1 --fname killed_ac > training_logs/killed_ac/killed
