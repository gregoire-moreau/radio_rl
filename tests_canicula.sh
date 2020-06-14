#!/bin/bash

mkdir -p training_logs/dose_dqn_sec

./main.py --canicula -n DQN --obs_type types -r dose  -e 50 2500 -s c++ -l 0.01 0.9 1 --fname dose_dqn_sec > training_logs/dose_dqn_sec/dose


