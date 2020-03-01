#!/bin/bash


lrs=(0.0001)
adapt=(0.8)
mkdir -p training_logs/canicula
for lr in ${lrs[@]}; do
  for a in ${adapt[@]}; do
    ./main.py --canicula -n AC --obs_type head -r killed -s c++ -l $lr $a 1 > training_logs/canicula/head-killed-$lr-$a
    ./main.py --canicula -n AC --obs_type head -r dose -s c++ -l $lr $a 1 > training_logs/canicula/head-dose-$lr-$a
    ./main.py --canicula -n AC --obs_type head -r oar -s c++ -l $lr $a 1 > training_logs/canicula/head-oar-$lr-$a
    ./main.py --canicula -n AC --obs_type types -r oar -s c++ -l $lr $a 1 > training_logs/canicula/types-oar-$lr-$a
  done
done

