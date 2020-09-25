## Model_cpp directory

This directory contains the implementations of the 2D and scalar model in C++, 
as well as the setup files to use the 2D model as a Python package and the Python interface for the deer agent.

The files used in both models are:

* cell.cpp and cell.h: Define the cell classes for the different types of cells (cancer and healthy cells), and describes how these cells react to radiation
* grid.cpp and grid.h: Define a linked list for cells on one pixel and the 2D grid where those cell lists will be placed in the 2D model

Files only used in the 2D model:

* controller.cpp and controller.h: Defines the "Controller" which starts the simulation and simulates additional hours
* model.cpp: Defines the functions that will be available in the Python package interfacing with the C++ implementation
* setup.py: Compiles and creates the Python package
* model_env_cpp.py: Interface between the Python package and the deep reinforcement learning

You can create and install the 2D model Python package locally with:

```
python3 setup.py install --user
```

Files only used in the scalar model:

* scalar_model.cpp and scalar_model.h: Defines the scalar model and the agent trained on this model with tabular Q-learning
* Makefile: Compiles the scalar model into an executable file called "main"

You can install the scalar model by calling 
```
make
```
