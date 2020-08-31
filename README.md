The model folder contains the code of the Python implementation of the simulation.

The model_cpp folder contains the code of the C++ implementation of the simulation.
To use this implementation, it is necessary to use the command:  
        python3 setup.py install --user   
inside the folder to create a module that can be used inside Python code.


The nnets folder contains the neural networks trained with different algorithms and reward functions as explained in the manuscript.

The training_logs folder contains the training log files of the four agents described in the manuscript inside zip archives.

cell_environment.py acts as an interface between the Python implementation of the simulation and the agent.

main.py is used to train an agent.

use_network.py evaluates a neural network using the performance indicators described in the manuscript.

draw_treatment.py is used by use_network.py to show the evolution of a tumour and a dose map in an example treatment suggested by the agent.

GaussianNoiseExplorationPolicy.py implements an exploration strategy based on Gaussian noise for the DDPG algorithm.

other_controllers.py contains a controller that can be used to change the magnitude of this Gaussian Noise strategy during the treatment as well as a controller that automatically adapts the learning rate during the treatment.

