## Python implementation of the tumoural development model

This directory contains the files implementing the tumoural development model in Python.

* cell.py: Implementations of the different classes of cells in the model.
* grid.py: Implementation of the grid on which the cells are placed in the 2D model.
* controller.py: Starts and controls the simulation of the model.
* cell_environment.py: Interface between the 2D model and the deep reinforcement learning agents.
* scalar_model.py: Implements the scalar model (collapse of the 2D model elements to 0 dimensions) and the agents that use tabular Q-learning to optimise treatments on this model.