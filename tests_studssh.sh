#!/bin/bash

mkdir -p training_logs/center
./main.py -n AC --obs_type head -r dose -e 20 2500 > training_logs/center/head_reg
./main.py -n AC --obs_type types -r dose -e 20 2500 > training_logs/center/types_reg
./main.py -n AC --obs_type head -r dose -e 20 2500 --center > training_logs/center/head_center
./main.py -n AC --obs_type types -r dose -e 20 2500 --center > training_logs/center/types_center
./main.py -n AC --obs_type head -r dose -e 20 2500 -t > training_logs/center/head_radius
./main.py -n AC --obs_type types -r dose -e 20 2500 -t > training_logs/center/types_radius
./main.py -n AC --obs_type head -r dose -e 20 2500 --center -t > training_logs/center/head_both
./main.py -n AC --obs_type types -r dose -e 20 2500 --center -t > training_logs/center/types_both