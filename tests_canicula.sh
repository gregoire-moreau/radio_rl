#!/bin/bash

mkdir -p training_logs/ca_dose
./main.py --canicula -n AC --obs_type types -r dose  -e 100 2500 -s c++ -l 0.001 0.9 1 --fname ca_dose > training_logs/ca_dose/dose
