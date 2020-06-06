#!/bin/bash

mkdir -p training_logs/ca_killed_nosp
./main.py --canicula -n AC --obs_type types -r killed  -e 100 2500 -s c++ -l 0.001 0.9 1 --no_special --fname ca_killed_no > training_logs/ca_killed_nosp/killed-nosp
