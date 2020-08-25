#!/bin/bash
mkdir -p training_logs/ddpg_dose_st
./use_network.py -n DQN -r killed --fname killed_dqn_new > eval_killed_dqn
./use_network.py -n DQN -r dose --fname dose_dqn_new > eval_dose_dqn
./use_network.py -n DDPG -r killed --fname killed_ddpg > eval_killed_ddpg
./use_network.py -n DDPG -r dose --fname dose_ddpg_n > eval_dose_ddpg
#./main.py -r dose -n DDPG -e 100 2500 -l 0.0001 0.9 1 --fname dose_ddpg_new > training_logs/ddpg_dose_st/dose
