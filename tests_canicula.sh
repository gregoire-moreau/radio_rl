#!/bin/bash

mkdir -p training_logs/killed_ac_ilr

./main.py --canicula -n AC --obs_type types -r killed  -e 5 2500 -s c++ -l 0.1 0.9 1 > training_logs/killed_ac_ilr/killed-0.1
./main.py --canicula -n AC --obs_type types -r killed  -e 5 2500 -s c++ -l 0.05 0.9 1 > training_logs/killed_ac_ilr/killed-0.05
./main.py --canicula -n AC --obs_type types -r killed  -e 5 2500 -s c++ -l 0.01 0.9 1 > training_logs/killed_ac_ilr/killed-0.01
./main.py --canicula -n AC --obs_type types -r killed  -e 5 2500 -s c++ -l 0.005 0.9 1 > training_logs/killed_ac_ilr/killed-0.005
./main.py --canicula -n AC --obs_type types -r killed  -e 5 2500 -s c++ -l 0.001 0.9 1 > training_logs/killed_ac_ilr/killed-0.001
./main.py --canicula -n AC --obs_type types -r killed  -e 5 2500 -s c++ -l 0.0005 0.9 1 > training_logs/killed_ac_ilr/killed-0.0005
./main.py --canicula -n AC --obs_type types -r killed  -e 5 2500 -s c++ -l 0.0001 0.9 1 > training_logs/killed_ac_ilr/killed-0.0001
./main.py --canicula -n AC --obs_type types -r killed  -e 5 2500 -s c++ -l 0.00005 0.9 1 > training_logs/killed_ac_ilr/killed-0.00005
./main.py --canicula -n AC --obs_type types -r killed  -e 5 2500 -s c++ -l 0.00001 0.9 1 > training_logs/killed_ac_ilr/killed-0.00001
./main.py --canicula -n AC --obs_type types -r killed  -e 5 2500 -s c++ -l 0.000005 0.9 1 > training_logs/killed_ac_ilr/killed-0.000005
