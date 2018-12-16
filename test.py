import time
import numpy as np
import scipy.integrate
import pyquad

def test_integrand_func(x, alpha, beta, i, j, k, l):
    return x * alpha * beta + i * j * k

pyquad.quad_grid(test_integrand_func, 0, 1, np.array([1.]), (1., 1., 1., 1.,
                                                             1., 1.))
