import math

# Computes surviving fraction of cancer cell after radiotherapy
# Jalalimanesh page 3
# D : dose in Gray
# alpha and beta in Gy-1 and Gy-2
# OER : Oxygen Enhancement ratio due to irradiation
def survival_fraction(D, alpha=0.13, beta = 0.0025, OER = 1):
    return math.exp(-(alpha*D/OER)-(beta*(D**2)/(OER**2)))

