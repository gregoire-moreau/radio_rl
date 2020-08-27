#!/bin/bash
#./use_network.py -n DQN -r killed --fname baseline > eval_baseline
#./use_network.py -n DQN -r killed --fname killed_dqn_new > eval_killed_dqn
#./use_network.py -n DQN -r dose --fname dose_dqn_new > eval_dose_dqn
#./use_network.py -n DDPG -r killed --fname killed_ddpg > eval_killed_ddpg
#./use_network.py -n DDPG -r dose --fname dose_ddpg_new > eval_dose_ddpg
#./main.py -r dose -n DDPG -e 100 2500 -l 0.0001 0.9 1 --fname dose_ddpg_new > training_logs/ddpg_dose_st/dose
./model_cpp/main 0 1 i 100 10 killed_100_10.csv l > eval_killed_scalar
./model_cpp/main 0 d i 100 10 dose_100_10.csv l > eval_dose_scalar