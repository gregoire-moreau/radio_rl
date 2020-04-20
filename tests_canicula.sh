#!/bin/bash


mkdir -p training_logs/canicula
./main.py --canicula -n AC --obs_type head -r dose -e 210 2500 > training_logs/canicula/head
./main.py --canicula -n AC --obs_type types -r dose -e 210 2500 > training_logs/canicula/types