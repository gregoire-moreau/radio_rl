#!/usr/bin/env python3

import re
from ast import literal_eval
import matplotlib.pyplot as plt
import numpy as np
import sys

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
                means.append(float(a[1]))
                std_errs.append(float(a[2]))
            elif "mean, std_error" in line:
                found = True
    steps = [i * 24 for i in range(len(means))]
    return means, std_errs, steps


def treatment_var(means_data, err_data, steps, name):
    ind_end= len(means_data)
    while means_data[ind_end-1] == np.nan or means_data[ind_end-1] == 0.0:
        ind_end -= 1
    plt.errorbar(steps[:ind_end], means_data[:ind_end], yerr=err_data[:ind_end], fmt='o-', color='b')
    if 'baseline' not in name:
        if 'scalar' in name:
            means_b, std_errs_b, steps_b = read_csv_scalar('eval/eval_scalar_baseline')
        else:
            means_b, std_errs_b, steps_b = load_other('baseline')
        plt.errorbar(steps_b, means_b, yerr=std_errs_b, fmt='o-', color='b')

    plt.xlabel('Treatment time (h)')
    plt.ylabel('Dose (Gy)')
    plt.xlim((-10, steps[ind_end-1]+10))
    plt.ylim((-0.1, 5.1))
    plt.savefig('tmp/' + name + 'var.pdf', format='pdf')


def load_other(name):
    treats = np.load('eval/'+name+'_treatments.npy')
    treats[np.isnan(treats)] = 0.0
    means = np.mean(treats, 0)
    errs = np.std(treats, 0)
    steps = [i*(12 if 'ddpg' in name else 24) for i in range(len(means))]
    return means, errs, steps


if __name__ == '__main__':
    reward = sys.argv[1]
    means, std_errs, steps = read_csv_scalar('eval/eval_' + reward + '_scalar')
    treatment_var(means, std_errs, steps, reward + '_scalar')

