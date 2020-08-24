#!/bin/bash

mkdir -p training_logs/dose_new

./main.py --canicula -n DQN --obs_type densities -r dose  -e 100 2500 -s c++ -l 0.0005 0.9 1 --fname dose_new > training_logs/dose_new/dose

./main.py --canicula -n DQN --obs_type densities -r dose  -e 100 2500 -s c++ -l 0.0005 0.9 1 --fname dose_new3 > training_logs/dose_new/dose3

./main.py --canicula -n DQN --obs_type densities -r dose  -e 100 2500 -s c++ -l 0.0005 0.9 1 --fname dose_new4 > training_logs/dose_new/dose4

