#!/bin/bash

mkdir -p training_logs/stlra

#types dose
./main.py -n DQN --obs_type types -r dose -e 25 2500 -s c++ -l 0.005 1 1 > training_logs/stlra/types-dose-0.005-1-1
./main.py -n DQN --obs_type types -r dose -e 25 2500 -s c++ -l 0.005 0.75 1 > training_logs/stlra/types-dose-0.005-.75-1
./main.py -n DQN --obs_type types -r dose -e 25 2500 -s c++ -l 0.005 0.5 1 > training_logs/stlra/types-dose-0.005-.5-1
./main.py -n DQN --obs_type types -r dose -e 25 2500 -s c++ -l 0.005 0.75 2 > training_logs/stlra/types-dose-0.005-.75-2
./main.py -n DQN --obs_type types -r dose -e 25 2500 -s c++ -l 0.005 0.5 2 > training_logs/stlra/types-dose-0.005-.5-2
./main.py -n DQN --obs_type types -r dose -e 25 2500 -s c++ -l 0.005 0.75 4 > training_logs/stlra/types-dose-0.005-.75-4
./main.py -n DQN --obs_type types -r dose -e 25 2500 -s c++ -l 0.005 0.5 4 > training_logs/stlra/types-dose-0.005-.5-4
./main.py -n DQN --obs_type types -r dose -e 25 2500 -s c++ -l 0.001 1 1 > training_logs/stlra/types-dose-0.001-1-1
./main.py -n DQN --obs_type types -r dose -e 25 2500 -s c++ -l 0.001 0.75 1 > training_logs/stlra/types-dose-0.001-.75-1
./main.py -n DQN --obs_type types -r dose -e 25 2500 -s c++ -l 0.001 0.5 1 > training_logs/stlra/types-dose-0.001-.5-1
./main.py -n DQN --obs_type types -r dose -e 25 2500 -s c++ -l 0.001 0.75 2 > training_logs/stlra/types-dose-0.001-.75-2
./main.py -n DQN --obs_type types -r dose -e 25 2500 -s c++ -l 0.001 0.5 2 > training_logs/stlra/types-dose-0.001-.5-2
./main.py -n DQN --obs_type types -r dose -e 25 2500 -s c++ -l 0.001 0.75 4 > training_logs/stlra/types-dose-0.001-.75-4
./main.py -n DQN --obs_type types -r dose -e 25 2500 -s c++ -l 0.001 0.5 4 > training_logs/stlra/types-dose-0.001-.5-4
