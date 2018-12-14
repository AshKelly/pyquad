from pyquad import quad, cfunc
import numpy as np

@cfunc("float64(float64, float64, float64, float64, float64, float64, float64)")
def deflection_func(x, alpha, beta, i, j, k, l):
    return x * alpha * beta + i*j*k

quad(deflection_func, np.ones(6))
