#!/bin/bash

mkdir -p training_logs/st_killednosp

#types killed
./main.py -n DQN --obs_type types -r killed  -e 100 2500 -s c++ -l 0.01 0.9 1 --no_special --fname st_killed_no > training_logs/st_killednosp/killed-nosp
