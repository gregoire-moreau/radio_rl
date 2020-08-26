import re
from ast import literal_eval
import matplotlib.pyplot as plt
import numpy as np

def read_data(means, error, step):
    a = re.sub(r"([^[])\s+([^]])", r"\1, \2", means)
    means_data = np.array(literal_eval(a), dtype=float)
    a = re.sub(r"([^[])\s+([^]])", r"\1, \2", error)
    err_data = np.array(literal_eval(a), dtype=float)
    if len(means_data) != len(err_data):
        raise Exception('Not the same size')
    steps = [i * step for i in range(len(means_data))]
    return means_data, err_data, steps

def treatment_var(means_data, err_data, steps, name):
    ind_end = list(means_data).index(0.0)
    plt.errorbar(steps[:ind_end], means_data[:ind_end], yerr=err_data[:ind_end])
    plt.savefig('tmp/' + name + 'var')


