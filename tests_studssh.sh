#!/bin/bash

mkdir -p training_logs/stud
./main.py -n DQN --obs_type head -r dose -e 70 2500 --fname dose > training_logs/stud/dose
