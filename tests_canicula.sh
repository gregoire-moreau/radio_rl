#!/bin/bash

mkdir -p training_logs/dose_ac

./main.py --canicula -n AC --obs_type types -r dose  -e 200 2500 -s c++ -l 0.01 0.9 1 --fname dose_ac > training_logs/dose_ac/dose
