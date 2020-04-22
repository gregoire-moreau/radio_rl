#!/bin/bash

mkdir -p training_logs/studssh
./main.py -n AC --obs_type head -r dose -e 20 2500 > training_logs/studssh/head_reg
./main.py -n AC --obs_type types -r dose -e 20 2500 > training_logs/studssh/types_reg
./main.py -n AC --obs_type head -r dose -e 20 2500 --center > training_logs/studssh/head_center
./main.py -n AC --obs_type types -r dose -e 20 2500 --center > training_logs/studssh/types_center
./main.py -n AC --obs_type head -r dose -e 20 2500 -t > training_logs/studssh/head_radius
./main.py -n AC --obs_type types -r dose -e 20 2500 -t > training_logs/studssh/types_radius
./main.py -n AC --obs_type head -r dose -e 20 2500 --center -t > training_logs/studssh/head_both
./main.py -n AC --obs_type types -r dose -e 20 2500 --center -t > training_logs/studssh/types_both