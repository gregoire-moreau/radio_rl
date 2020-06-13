#!/bin/bash

mkdir -p training_logs/dose_ac_gauss


./main.py --canicula -n AC --obs_type types -r dose  -e 100 2500 -s c++ -l 0.01 0.9 1 --fname dose_ac_gauss> training_logs/dose_ac_gauss/dose
