#!/bin/bash

./model_cpp/main 100 d o 50 5 qvals_dose_log_5.csv > test_dose_log_5
./model_cpp/main 100 n i 50 5 qvals_no_lin_5.csv > test_no_lin_5
./model_cpp/main 100 n o 50 5 qvals_no_log_5.csv > test_no_log_5
