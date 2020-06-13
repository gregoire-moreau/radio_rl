#!/bin/bash

mkdir -p training_logs/killed_ac_gauss


./main.py -n AC --obs_type types -r killed  -e 100 2500 -s c++ -l 0.01 0.9 1 --fname killed_ac_gauss> training_logs/killed_ac_gauss/killed

