#!/bin/bash


mkdir -p training_logs/cani
./main.py --canicula -n AC --obs_type head -r dose -e 120 2500 --fname head_dose > training_logs/cani/head_dose
./main.py --canicula -n AC --obs_type types -r dose -e 120 2500 --fname types_dose > training_logs/cani/types_dose
./main.py --canicula -n AC --obs_type head -r killed -e 120 2500 --fname head_killed > training_logs/cani/head_killed
./main.py --canicula -n AC --obs_type types -r killed -e 120 2500 --fname head_killed > training_logs/cani/types_killed
./main.py --canicula -n AC --obs_type head -r dose -e 120 2500 -t --fname head_dose_radius > training_logs/cani/head_dose_radius
./main.py --canicula -n AC --obs_type types -r dose -e 120 2500 -t --fname types_dose_radius > training_logs/cani/types_dose_radius
./main.py --canicula -n AC --obs_type head -r killed -e 120 2500 -t --fname head_killed_radius > training_logs/cani/head_killed_radius
./main.py --canicula -n AC --obs_type types -r killed -e 120 2500 -t --fname types_killed_radius > training_logs/cani/types_killed_radius