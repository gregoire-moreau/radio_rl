#!/bin/bash

./use_network.py -n DQN -r killed --fname killed_dqn_new > eval_killed_dqn
./use_network.py -n DQN -r dose --fname dose_dqn_new > eval_dose_dqn
./use_network.py -n DDPG -r killed --fname killed_ddpg > eval_killed_ddpg
./use_network.py -n DDPG -r dose --fname dosemod_ddpg > eval_dose_ddpg
