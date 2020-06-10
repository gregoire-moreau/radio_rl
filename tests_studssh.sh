#!/bin/bash

mkdir -p training_logs/killed4

./main.py -n DQN --obs_type types -r killed  -e 200 2500 -s c++ -l 0.01 0.9 1 --fname killed4 > training_logs/killed4/killed
