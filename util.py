import math

# Computes surviving fraction of cancer cell after radiotherapy
# Jalalimanesh page 3
# D : dose in Gray
# alpha and beta in Gy-1 and Gy-2
# OER : Oxygen Enhancement ratio due to irradiation
def survival_fraction(D, alpha=0, beta = 0, OER = 1):
    return math.exp(-(alpha*D/OER)-(beta*(D**2)/(OER**2)))

def Q_learning(gamm, delt, lamb, max_iter = 100, rem_threshold = 50):
    for i in range(1, max_iter+1):
        n = delt/i
        remaining = 0