from deer.experiment.base_controllers import Controller, EpsilonController
import numpy as np
import joblib
import os
class GaussianNoiseController(EpsilonController):
    def __init__(self, initial_std_dev=1.0, n_decays=10000, final_std_dev=0.0, evaluate_on='action', periodicity=1, reset_every='none'):
        super().__init__(initial_e=initial_std_dev, e_decays=n_decays, e_min=final_std_dev,
                                             evaluate_on=evaluate_on, periodicity=periodicity, reset_every=reset_every)
    def _reset(self, agent):
        self._count = 0
        agent._train_policy.setStdDev(self._init_e)
        self._e = self._init_e

    def _update(self, agent):
        self._count += 1
        if self._periodicity <= 1 or self._count % self._periodicity == 0:
            agent._train_policy.setStdDev(self._e)
            self._e = max(self._e - self._e_decay, self._e_min)

