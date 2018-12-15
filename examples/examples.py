import time
import numpy as np
import scipy.integrate
from jit import jit_integrand

from pyquad import quad, quad_grid, parallel_quad_grid, cfunc

def test_integrand_func(x, alpha, beta, i, j, k, l):
    return x * alpha * beta + i * j * k

# Serial pyquad.quad can be used as drop in replacement for
# scipy.integrate.quad
res = quad(test_integrand_func, 0, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0), limit=50)

# res will be a tuple with the integral result as the first value and the erorr
# as the second value


# but the main purpose of the pyquad is to do lots of integrals faster
# so we have pyquad.quad_grid and pyquad.parallel_quad_grid
# so consider a random grid of the form of 2 columns
np.random.seed(1)
grid = np.random.random((10000000, 2))
grid = np.asfortranarray(grid)

# we can then integrate over a grid of the 2 of the parameters with the
# remainder of the parameters fixed
t0 = time.time()

res = quad_grid(test_integrand_func, 0, 1, grid, (1.0, 1.0, 1.0, 1.0))

dt = time.time() - t0
print("pyquad grid time:  ", dt)

# which is directly equivalent to the following with scipy,
t0 = time.time()

res = np.zeros(grid.shape[0])
for i in range(res.shape[0]):
    res[i] = scipy.integrate.quad(
        test_integrand_func, 0, 1, (grid[i, 0], grid[i, 1], 1.0, 1.0, 1.0, 1.0)
    )[0]

dt = time.time() - t0
print("scipy naive grid time:  ", dt)
