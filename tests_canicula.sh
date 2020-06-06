#!/bin/bash

mkdir -p training_logs/ca_killed
./main.py --canicula -n AC --obs_type types -r killed  -e 100 2500 -s c++ -l 0.001 0.9 1 --fname ca_killed > training_logs/ca_killed/killed
