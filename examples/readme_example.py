import time
import numpy as np
import scipy.integrate
import pyquad

def test_integrand_func(x, alpha, beta, i, j, k, l):
    return x * alpha * beta + i * j * k

grid = np.random.random((10000000, 2))

res = np.zeros(grid.shape[0])
t0 = time.time()
for i in range(res.shape[0]):
    res[i] = scipy.integrate.quad(
        test_integrand_func, 0, 1, (grid[i, 0], grid[i, 1], 1.0, 1.0, 1.0, 1.0)
    )[0]
print(time.time() - t0)

t0 = time.time()
res = pyquad.quad_grid(test_integrand_func, 0, 1, grid, (1.0, 1.0, 1.0, 1.0))
print(time.time() - t0)
