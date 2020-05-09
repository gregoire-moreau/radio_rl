#!/bin/bash

mkdir -p training_logs/stud
./main.py -n DQN --obs_type head -r dose -e 100 2500 --fname dose > training_logs/stud/dose
./main.py -n DQN --obs_type types -r dose -e 100 2500 --fname dose > training_logs/stud/dose
