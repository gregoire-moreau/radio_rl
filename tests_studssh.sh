#!/bin/bash

mkdir -p training_logs/st_killed

#types killed
./main.py -n DQN --obs_type types -r killed  -e 100 2500 -s c++ -l 0.01 0.9 1 --fname st_killed > training_logs/st_killed/killed
