#!/bin/bash

mkdir -p training_logs/ca_killed

#types dose
./main.py --canicula -n AC --obs_type types -r killed  -e 100 2500 -s c++ -l 0.001 0.9 1 --fname ca_killed_sp > training_logs/ca_killed/killed-sp
./main.py --canicula -n AC --obs_type types -r killed  -e 100 2500 -s c++ -l 0.001 0.9 1 --no-special --fname ca_killed_no > training_logs/ca_killed/killed-nosp