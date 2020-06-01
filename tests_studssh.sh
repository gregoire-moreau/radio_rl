#!/bin/bash

mkdir -p training_logs/st_types_dose

#types dose
./main.py -n DQN --obs_type types -r dose --fname dqn_dose_ult -e 200 2500 -s c++ -l 0.005 .75 4 > training_logs/st_types_dose/dose_0.005-.75-4