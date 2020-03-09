import matplotlib.pyplot as plt
import pyquad
import numpy as np


INTEGRAL_METHOD = "qags"
REPEATS = 20


def test_func(x, a, b, c):
    return a*a / (x + 1.0) + b * np.sin(np.sqrt(x)) + c * np.log(x + 1) + np.tanh(x*a)


def benchmark_pyquad():
    np.random.seed(101)
    grid = np.random.random((10000, 3))

    for repeat in range(REPEATS):
        res = pyquad.quad_grid(test_func, 0.0, 2.0, grid, method=INTEGRAL_METHOD,
                               num_threads=8)[0]



benchmark_pyquad()
