import time
import numpy as np
from model.controller import MultiThreadController
from model.grid import Grid

times = [float('inf')]
i = 1
for i in range(1,65):
    sum = 0
    for _ in range(3):
        grid = Grid(50, 50, glucose=True, oxygen=True, cells=True, border=False, sources=50)
        controller = MultiThreadController(grid, 500, i)
        start = time.time()
        controller.go(1000)
        end = time.time()
        sum += end-start
    times.append(sum/3)
    if times[i] >= times[i-1]:
        break
print(times)
print("The best number of threads is", np.argmin(times),'.')