#!/bin/bash

mkdir -p training_logs/dose_ddpg_new

./main.py --canicula -n DDPG --obs_type densities -r dose  -e 100 2500 -s c++ -l 0.001 0.9 1 --fname dose_ddpg_new4 > training_logs/dose_ddpg_new/dose4

./main.py --canicula -n DDPG --obs_type densities --exploration gauss -r dose  -e 100 2500 -s c++ -l 0.001 0.9 1 --fname dose_ddpg_new2 > training_logs/dose_ddpg_new/dose2

./main.py --canicula -n DDPG --obs_type densities --exploration gauss -r dose  -e 100 2500 -s c++ -l 0.0001 0.9 1 --fname dose_ddpg_new3 > training_logs/dose_ddpg_new/dose3

