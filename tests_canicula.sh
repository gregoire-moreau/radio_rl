#!/bin/bash


mkdir -p training_logs/cani
./main.py --canicula -n AC --obs_type head -r dose -e 70 2500 --fname dose > training_logs/cani/dose
