#!/bin/bash

mkdir -p training_logs/dose_new

./main.py --canicula -n DQN --obs_type densities -r dose  -e 200 2500 -s c++ -l 0.01 0.9 1 --fname dose_new > training_logs/dose_new/dose

