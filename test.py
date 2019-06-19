import numpy as np
import matplotlib.pyplot as plt
import deer as deer
import cell
import random

def act(patch, dose):
    healthy = patch.num_healthy
    cancer = patch.num_cancer
    print("Sending a dose of ", dose, " Gray")
    patch.irradiate(dose)
    return cancer-patch.num_cancer-healthy+patch.num_healthy

def new_patch():
    patch = cell.Patch()
    for i in range(400):
        #print("cancer cells : ", patch.num_cancer, "healthy cells :", patch.num_healthy)
        patch.tick()
    #print("Made a new patch with ", patch.num_cells, " cells")
    return patch


if __name__ == '__main__':
    Q = [0 for i in range(13)]
    A = list(range(13))
    delta = 0.4
    for i in range(1,101):
        print("Start of iteration ", i)
        n = delta/i
        patch = new_patch()
        while patch.num_cancer > 50:
            rand = random.random()
            if rand > n:
                ind = np.argmax(Q)
            else:
                ind = random.randint(0,12)
            rew = act(patch, A[ind])
            Q[ind] = Q[ind]+0.2*rew