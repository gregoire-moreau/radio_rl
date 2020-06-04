#!/bin/bash

mkdir -p training_logs/ca_types_killed

#types dose
./main.py --canicula -n AC --obs_type types -r killed  -e 100 2500 -s c++ -l 0.01 .75 4 --no_special --fname ac_killed_no > training_logs/ca_types_killed/killed-.75-4-no
./main.py --canicula -n AC --obs_type types -r killed  -e 100 2500 -s c++ -l 0.01 .75 4 --fname ac_killed > training_logs/ca_types_killed/killed-.75-4