#!/bin/bash

./model_cpp/main 100 k i 50 5 qvals_killed_lin_5.csv > test_killed_lin_5
./model_cpp/main 100 k o 50 5 qvals_killed_log_5.csv > test_killed_log_5
./model_cpp/main 100 d i 50 5 qvals_dose_lin_5.csv > test_dose_lin_5
./model_cpp/main 100 d o 50 5 qvals_dose_log_5.csv > test_dose_log_5
./model_cpp/main 100 n i 50 5 qvals_no_lin_5.csv > test_no_lin_5
./model_cpp/main 100 n o 50 5 qvals_no_log_5.csv > test_no_log_5
./model_cpp/main 100 k i 50 10 qvals_killed_lin_10.csv > test_killed_lin_10
./model_cpp/main 100 k o 50 10 qvals_killed_log_10.csv > test_killed_log_10
./model_cpp/main 100 d i 50 10 qvals_dose_lin_10.csv > test_dose_lin_10
./model_cpp/main 100 d o 50 10 qvals_dose_log_10.csv > test_dose_log_10
./model_cpp/main 100 n i 50 10 qvals_no_lin_10.csv > test_no_lin_10
./model_cpp/main 100 n o 50 10 qvals_no_log_10.csv > test_no_log_10