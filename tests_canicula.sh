#!/bin/bash

mkdir -p training_logs/calra

#types dose
./main.py --canicula -n AC --obs_type types -r dose -e 25 2500 -s c++ -l 0.005 1 1 > training_logs/calra/types-dose-0.005-1-1
./main.py --canicula -n AC --obs_type types -r dose -e 25 2500 -s c++ -l 0.005 0.75 1 > training_logs/calra/types-dose-0.005-.75-1
./main.py --canicula -n AC --obs_type types -r dose -e 25 2500 -s c++ -l 0.005 0.5 1 > training_logs/calra/types-dose-0.005-.5-1
./main.py --canicula -n AC --obs_type types -r dose -e 25 2500 -s c++ -l 0.005 0.75 2 > training_logs/calra/types-dose-0.005-.75-2
./main.py --canicula -n AC --obs_type types -r dose -e 25 2500 -s c++ -l 0.005 0.5 2 > training_logs/calra/types-dose-0.005-.5-2
./main.py --canicula -n AC --obs_type types -r dose -e 25 2500 -s c++ -l 0.005 0.75 4 > training_logs/calra/types-dose-0.005-.75-4
./main.py --canicula -n AC --obs_type types -r dose -e 25 2500 -s c++ -l 0.005 0.5 4 > training_logs/calra/types-dose-0.005-.5-4
./main.py --canicula -n AC --obs_type types -r dose -e 25 2500 -s c++ -l 0.0001 1 1 > training_logs/calra/types-dose-0.0001-1-1
./main.py --canicula -n AC --obs_type types -r dose -e 25 2500 -s c++ -l 0.0001 0.75 1 > training_logs/calra/types-dose-0.0001-.75-1
./main.py --canicula -n AC --obs_type types -r dose -e 25 2500 -s c++ -l 0.0001 0.5 1 > training_logs/calra/types-dose-0.0001-.5-1
./main.py --canicula -n AC --obs_type types -r dose -e 25 2500 -s c++ -l 0.0001 0.75 2 > training_logs/calra/types-dose-0.0001-.75-2
./main.py --canicula -n AC --obs_type types -r dose -e 25 2500 -s c++ -l 0.0001 0.5 2 > training_logs/calra/types-dose-0.0001-.5-2
./main.py --canicula -n AC --obs_type types -r dose -e 25 2500 -s c++ -l 0.0001 0.75 4 > training_logs/calra/types-dose-0.0001-.75-4
./main.py --canicula -n AC --obs_type types -r dose -e 25 2500 -s c++ -l 0.0001 0.5 4 > training_logs/calra/types-dose-0.0001-.5-4


