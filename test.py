import numpy as np
import matplotlib.pyplot as plt
import deer as deer
import cell

if __name__ == '__main__':
    patch = cell.Patch()
    patch.addCell(cell.Cell(patch))
    for i in range(1000):
        print("Time = ", i, ", Number of cells = ", patch.num_cells)
        patch.tick()