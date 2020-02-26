#!/bin/bash

lrs=(0.001 0.0001 0.00001 0.000001 0.0000001)
adapt=(0.9 0.8 0.5)
mkdir -p training_logs/studssh
for lr in ${lrs[@]}; do
  for a in ${adapt[@]}; do
    ./main.py -n DQN -r dose -s c++ -l $lr $a 1 > training_logs/studssh/types_$lr_$a 2>/dev/null
    ./main.py --obs_type head -n DQN -r dose -s c++ -l $lr $a 1 > training_logs/studssh/head_$lr_$a 2>/dev/null
    ./main.py -t --obs_type head -n DQN -r dose -s c++ -l $lr $a 1 > training_logs/studssh/head_tumor_$lr_$a 2>/dev/null
    ./main.py -t -n DQN -r dose -s c++ -l $lr $a 1 > training_logs/studssh/types_tumor_$lr_$a 2>/dev/null
  done
done

