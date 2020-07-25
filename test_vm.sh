#!/bin/bash

mkdir -p training_logs/dosemod_dqn

./main.py -n DQN --obs_type densities -r dose  -e 200 2500 -s c++ -l 0.01 0.9 1 --fname dosemod_dqn > training_logs/dosemod_dqn/dose