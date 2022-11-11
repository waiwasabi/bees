import math
import numpy as np


def normalize(center, x):
    return sigmoid(logit(center) + x)


def sigmoid(x):
    if x >= 0:
        return 1. / (1. + np.exp(-x))
    else:
        return np.exp(x) / (1. + np.exp(x))


def logit(x):
    return math.log(x / (1 - x))


def symlog(x):
    if x == 0:
        return 0
    elif x < 0:
        return -np.log(-x)
    else:
        return np.log(x)
