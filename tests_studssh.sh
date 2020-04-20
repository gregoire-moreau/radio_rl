#!/bin/bash

mkdir -p training_logs/studssh
./main.py -n DQN --obs_type head -r dose -e 210 2500 > training_logs/studssh/head
./main.py -n DQN --obs_type types -r dose -e 210 2500 > training_logs/studssh/types