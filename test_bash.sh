#!/bin/bash


lrs=(0.001 0.0001 0.00001 0.000001 0.0000001)
adapt=(0.9 0.8 0.5)
for lr in ${lrs[@]}; do
  for a in ${adapt[@]}; do
    echo "$lr $a"
  done
done

