#!/bin/bash

lrs=(0.001 0.0001 0.00001 0.000001)

for lr in ${lrs[@]}; do
  ./main.py -n DQN -r dose -s c++ -l $lr 0.8 1 > training_logs/studssh_types_$lr 2>/dev/null
  ./main.py --obs_type head -n DQN -r dose -s c++ -l $lr 0.8 1 > training_logs/studssh_head_$lr 2>/dev/null
done
