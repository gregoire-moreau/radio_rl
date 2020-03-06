#!/bin/bash

lrs=(0.001 0.00001)
adapt=(0.8 0.65 0.5)
mkdir -p training_logs/studssh
for lr in ${lrs[@]}; do
  for a in ${adapt[@]}; do
    ./main.py  -n DQN --obs_type head -r killed -s c++ -l $lr $a 1 > training_logs/studssh/head-killed-$lr-$a
    ./main.py  -n DQN --obs_type head -r killed --no_special -s c++ -l $lr $a 1 > training_logs/studssh/head-killed-nospecial-$lr-$a
    ./main.py  -n DQN --obs_type head -r dose -s c++ -l $lr $a 1 > training_logs/studssh/head-dose-$lr-$a
    ./main.py  -n DQN --obs_type head -r oar -s c++ -l $lr $a 1 > training_logs/studssh/head-oar-$lr-$a
    ./main.py  -n DQN --obs_type types -r oar -s c++ -l $lr $a 1 > training_logs/studssh/types-oar-$lr-$a
  done
done

