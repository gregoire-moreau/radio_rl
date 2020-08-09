#!/bin/bash

mkdir -p training_logs/killed_new

./main.py --canicula -n DQN --obs_type densities -r killed  -e 200 2500 -s c++ -l 0.01 0.9 1 --fname killed_new > training_logs/killed_new