import inspect
import time
import numba
import numpy as np
import scipy.integrate

from pyquad import quad, quad_grid, parallel_quad_grid, cfunc
from numba.types import intc, CPointer, float64
from scipy import LowLevelCallable


def jit_integrand(integrand_function):
    jitted_function = numba.jit(integrand_function, nopython=True, cache=True)
    no_args = len(inspect.getfullargspec(integrand_function).args)

    wrapped = None

    if no_args == 4:
        # noinspection PyUnusedLocal
        def wrapped(n, xx):
            return jitted_function(xx[0], xx[1], xx[2], xx[3])

    elif no_args == 5:
        # noinspection PyUnusedLocal
        def wrapped(n, xx):
            return jitted_function(xx[0], xx[1], xx[2], xx[3], xx[4])

    elif no_args == 6:
        # noinspection PyUnusedLocal
        def wrapped(n, xx):
            return jitted_function(xx[0], xx[1], xx[2], xx[3], xx[4], xx[5])

    elif no_args == 7:
        # noinspection PyUnusedLocal
        def wrapped(n, xx):
            return jitted_function(xx[0], xx[1], xx[2], xx[3], xx[4], xx[5], xx[6])

    elif no_args == 8:
        # noinspection PyUnusedLocal
        def wrapped(n, xx):
            return jitted_function(
                xx[0], xx[1], xx[2], xx[3], xx[4], xx[5], xx[6], xx[7]
            )

    elif no_args == 9:
        # noinspection PyUnusedLocal
        def wrapped(n, xx):
            return jitted_function(
                xx[0], xx[1], xx[2], xx[3], xx[4], xx[5], xx[6], xx[7], xx[8]
            )

    elif no_args == 10:
        # noinspection PyUnusedLocal
        def wrapped(n, xx):
            return jitted_function(
                xx[0], xx[1], xx[2], xx[3], xx[4], xx[5], xx[6], xx[7], xx[8], xx[9]
            )

    elif no_args == 11:
        # noinspection PyUnusedLocal
        def wrapped(n, xx):
            return jitted_function(
                xx[0],
                xx[1],
                xx[2],
                xx[3],
                xx[4],
                xx[5],
                xx[6],
                xx[7],
                xx[8],
                xx[9],
                xx[10],
            )

    cf = cfunc(float64(intc, CPointer(float64)))

    return LowLevelCallable(cf(wrapped).ctypes)


def test_integrand_func(x, alpha, beta, i, j, k, l):
    return x * alpha * beta + i * j * k


@jit_integrand
def test_integrand_func_jit(x, alpha, beta, i, j, k, l):
    return x * alpha * beta + i * j * k


# Serial pyquad
t0 = time.time()
a = quad(test_integrand_func, 0, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0), limit=50)
dt = time.time() - t0
print("pyquad time:  ", dt)

# Serial scipy
t0 = time.time()
a = scipy.integrate.quad(test_integrand_func, 0, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0))
dt = time.time() - t0
print("scipy time:  ", dt)


# Grid
np.random.seed(1)
grid = np.random.random((10000000, 2))
grid = np.asfortranarray(grid)

# pyquad
t0 = time.time()
res = quad_grid(test_integrand_func, 0, 1, grid, (1.0, 1.0, 1.0, 1.0))
dt = time.time() - t0
print("pyquad grid time:  ", dt)

# scipy with jit
t0 = time.time()
res = np.zeros(grid.shape[0])
for i in range(res.shape[0]):
    res[i] = scipy.integrate.quad(
        test_integrand_func_jit, 0, 1, (grid[i, 0], grid[i, 1], 1.0, 1.0, 1.0, 1.0)
    )[0]
dt = time.time() - t0
print("scipy jit grid time:  ", dt)

# scipy naive
t0 = time.time()
res = np.zeros(grid.shape[0])
for i in range(res.shape[0]):
    res[i] = scipy.integrate.quad(
        test_integrand_func, 0, 1, (grid[i, 0], grid[i, 1], 1.0, 1.0, 1.0, 1.0)
    )[0]
dt = time.time() - t0
print("scipy grid time:  ", dt)

# pyquad parallel grid
t0 = time.time()
res = parallel_quad_grid(test_integrand_func, 0, 1, grid, (1.0, 1.0, 1.0, 1.0))
dt = time.time() - t0
print("parallel pyquad grid time:  ", dt)
