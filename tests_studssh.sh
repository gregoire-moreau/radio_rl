#!/bin/bash

mkdir -p training_logs/stud
./main.py -n DQN --obs_type head -r dose -e 60 2500 --fname head_dose > training_logs/stud/head_dose
./main.py -n DQN --obs_type types -r dose -e 60 2500 --fname types_dose > training_logs/stud/types_dose
./main.py -n DQN --obs_type head -r killed -e 60 2500 --fname head_killed > training_logs/stud/head_killed
./main.py -n DQN --obs_type types -r killed -e 60 2500 --fname types_killed > training_logs/stud/types_killed
