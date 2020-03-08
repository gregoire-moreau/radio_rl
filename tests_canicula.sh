#!/bin/bash


lrs=(0.001 0.0001 0.00001)
adapt=(0.8 0.65 0.5)
mkdir -p training_logs/canicula
for lr in ${lrs[@]}; do
  for a in ${adapt[@]}; do
    ./main.py --canicula -n AC --obs_type head -r killed -s c++ -l $lr $a 1 > training_logs/canicula/gauss-head-killed-$lr-$a
    ./main.py --canicula -n AC --obs_type head -r killed --no_special -s c++ -l $lr $a 1 > training_logs/canicula/gauss-head-killed-nospecial-$lr-$a
    ./main.py --canicula -n AC --obs_type head -r dose -s c++ -l $lr $a 1 > training_logs/canicula/gauss-head-dose-$lr-$a
    ./main.py --canicula -n AC --obs_type head -r oar -s c++ -l $lr $a 1 > training_logs/canicula/gauss-head-oar-$lr-$a
    ./main.py --canicula -n AC --obs_type types -r oar -s c++ -l $lr $a 1 > training_logs/canicula/gauss-types-oar-$lr-$a
  done
done

