#!/bin/bash

mkdir -p training_logs/stlr

lrs=(0.1 0.05 0.01 0.005 0.001 0.0005 0.0001 0.00005 0.00001)
for lr in ${lrs[@]}; do
    ./main.py -n DQN --obs_type head -r killed -e 10 2500 -s c++ -l $lr 1 1 > training_logs/stlr/head-killed-$lr
    ./main.py -n DQN --obs_type types -r killed -e 10 2500 -s c++ -l $lr 1 1 > training_logs/stlr/types-killed-$lr
    ./main.py -n DQN --obs_type head -r dose -e 10 2500 -s c++ -l $lr 1 1 > training_logs/stlr/head-dose-$lr
    ./main.py -n DQN --obs_type types -r dose -e 10 2500 -s c++ -l $lr 1 1 > training_logs/stlr/types-dose-$lr
done