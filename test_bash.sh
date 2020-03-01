#!/bin/bash


lrs=(0.001)
adapt=(0.9)
for lr in ${lrs[@]}; do
  for a in ${adapt[@]}; do
    echo "$lr $a" > "types-$lr-$a"
  done
done

