#!/bin/bash

mkdir -p training_logs/dosemod_ddpg

./main.py --canicula -n DDPG --obs_type densities -r dose  -e 200 2500 -s c++ -l 0.01 0.9 1 --fname dosemod_ddpg > training_logs/dosemod_ddpg/dose