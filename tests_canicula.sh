#!/bin/bash

mkdir -p training_logs/killed2

./main.py --canicula -n DQN --obs_type types -r killed  -e 100 2500 -s c++ -l 0.01 0.9 1 --fname killed2 > training_logs/killed2/killed
