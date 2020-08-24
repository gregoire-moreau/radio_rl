#!/bin/bash

./model_cpp/main 500 d i 100 10 dose_big4.csv > dose_big4

cd model_cpp
make
cd ..

./model_cpp/main 500 d i 100 10 dose_big5.csv > dose_big5
