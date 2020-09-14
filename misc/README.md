## Miscellaneous directory

This directory contains files that don't fit in other directories.

These files are:

* draw_treatment.py: Used by use_network.py in the root directory to show the effects of an agent's treatment on the simulation.
* GaussianNoiseExplorationPolicy.py: Creates an exploration policy based on adding Gaussian noise to chosen actions for algorithms with continuous action domains.
* other_controllers.py: Contains GaussianNoiseExplorationController which is used to reduce the standard deviation of Gaussian noise during training.
* treatment_var.py: Used by use_network.py in the root directory to show the shape of treatments chosen by agents.