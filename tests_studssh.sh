#!/bin/bash

mkdir -p training_logs/st_killed_ilr

#types killed
./main.py -n DQN --obs_type types -r killed  -e 5 2500 -s c++ -l 0.1 1 1 > training_logs/st_killed_ilr/killed-.0.1
./main.py -n DQN --obs_type types -r killed  -e 5 2500 -s c++ -l 0.01 1 1 > training_logs/st_killed_ilr/killed-.0.01
./main.py -n DQN --obs_type types -r killed  -e 5 2500 -s c++ -l 0.001 1 1 > training_logs/st_killed_ilr/killed-.0.001
./main.py -n DQN --obs_type types -r killed  -e 5 2500 -s c++ -l 0.0001 1 1 > training_logs/st_killed_ilr/killed-.0.0001
./main.py -n DQN --obs_type types -r killed  -e 5 2500 -s c++ -l 0.00001 1 1 > training_logs/st_killed_ilr/killed-.0.00001
./main.py -n DQN --obs_type types -r killed  -e 5 2500 -s c++ -l 0.000001 1 1 > training_logs/st_killed_ilr/killed-.0.000001