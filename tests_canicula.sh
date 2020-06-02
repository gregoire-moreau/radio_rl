#!/bin/bash

mkdir -p training_logs/ca_types_dose

#types dose
./main.py --canicula -n AC --obs_type types -r dose --fname ac_dose_ult -e 120 2500 -s c++ -l 0.005 .75 4 > training_logs/ca_types_dose/dose_0.005-.75-4
