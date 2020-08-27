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

def read_csv_scalar(filename):
    with open(filename, 'r') as f:
        found = False
        means = []
        std_errs = []
        for line in f:
            if found:
                a = line.strip().split(', ')
                means.append(float(a[0]))
                std_errs.append(float(a[1]))
            elif "mean, std_error" in line:
                found = True
    steps = [i * 24 for i in range(len(means))]
    return means, std_errs, steps


def treatment_var(means_data, err_data, steps, name):
    ind_end= len(means_data)
    while means_data[ind_end-1] == np.nan:
        ind_end -= 1
    plt.errorbar(steps[:ind_end], means_data[:ind_end], yerr=err_data[:ind_end], fmt='o-')
    plt.xlabel('Treatment time (h)')
    plt.ylabel('Dose (Gy)')
    plt.ylim((-0.1, 5.1))
    plt.savefig('tmp/' + name + 'var')


if __name__ == '__main__':
    means, std_errs, steps = read_csv_scalar('eval_dose_scalar')
    treatment_var(means, std_errs, steps, 'dose_scalar')