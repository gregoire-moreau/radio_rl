#!/bin/bash

lrs=(0.001 0.0001 0.00001 0.000001)

for lr in ${lrs[@]}; do
  ./main.py --canicula -n AC -r dose -s c++ -l $lr 0.8 1 > training_logs/canicula_types_$lr 2>/dev/null
  ./main.py --canicula --obs_type head -n AC -r dose -s c++ -l $lr 0.8 1 > training_logs/canicula_head_$lr 2>/dev/null
done