#!/bin/bash

mkdir -p training_logs/st_dose

#types killed
./main.py -n DQN --obs_type types -r dose  -e 100 2500 -s c++ -l 0.01 0.9 1 --fname st_dose > training_logs/st_dose/dose
