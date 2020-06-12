#!/bin/bash

mkdir -p training_logs/dose_dqn

./main.py -n DQN --obs_type types -r dose  -e 200 2500 -s c++ -l 0.1 0.9 1 --fname dose_dqn> training_logs/dose_dqn/dose