#!/bin/bash

mkdir -p training_logs/st_types_killed

#types killed
./main.py -n DQN --obs_type types -r killed  -e 100 2500 -s c++ -l 0.01 .75 4 --no_special --fname dqn_killed_no > training_logs/st_types_killed/killed-.75-4-no
./main.py -n DQN --obs_type types -r killed  -e 100 2500 -s c++ -l 0.01 .75 4 --fname dqn_killed > training_logs/st_types_killed/killed-.75-4