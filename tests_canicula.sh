#!/bin/bash


lrs=(0.001 0.0001 0.00001 0.000001 0.0000001)
adapt=(0.9 0.8 0.5)
mkdir -p training_logs/canicula
for lr in ${lrs[@]}; do
  for a in ${adapt[@]}; do
    ./main.py --canicula -n AC -r dose -s c++ -l $lr $a 1 > training_logs/canicula/types_$lr_$a
    ./main.py --canicula --obs_type head -n AC -r dose -s c++ -l $lr $a 1 > training_logs/canicula/head_$lr_$a
    ./main.py  --canicula -t --obs_type head -n AC -r dose -s c++ -l $lr $a 1 > training_logs/canicula/head_tumor_$lr_$a
    ./main.py --canicula -t -n AC -r dose -s c++ -l $lr $a 1 > training_logs/canicula/types_tumor_$lr_$a
  done
done

