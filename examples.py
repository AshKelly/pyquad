from pyquad import quad, quad_grid, parallel_quad_grid, cfunc
import time
import numpy as np
import scipy.integrate

def test_integrand_func(x, alpha, beta, i, j, k, l):
    return x * alpha * beta + i*j*k

# First we pass the function to integrate, the lower bound, the upper bound and
# then we pass any extra arguments as a tuple
a = quad(test_integrand_func, 0, 1, (1., 1., 1., 1., 1., 1.))
print(a)

np.random.seed(1)
grid = np.random.random((10000000, 2))
grid = np.asfortranarray(grid)


# In this case, we will integrate the same function but over a wide range of
# alpha and beta. These are defined as the 2nd and 3rd argument.
# We will pass the alphas and betas as a 2D array.
# Column 1 will contain all the alpha values
# Column 2 will contain all the beta values
t0 = time.time()
res = quad_grid(test_integrand_func, 0, 1, grid, (1., 1., 1., 1.))
dt = time.time() - t0
print(np.sum(res))
print("time:  ", dt)


# This is equivlant to the following in scipy (this takes a few minutes)
t0 = time.time()
res = np.zeros(grid.shape[0])
for i in range(res.shape[0]):
    res[i] = scipy.integrate.quad(test_integrand_func, 0, 1, (grid[i, 0], grid[i, 1],
                                                              1., 1., 1., 1.))[0]
dt = time.time() - t0
print(np.sum(res))
print("time:  ", dt)

# We can do the same again in parallel if needed, however it usually needs
# to be a large amount of integerations to be a lot faster
t0 = time.time()
res = parallel_quad_grid(test_integrand_func, 0, 1, grid, (1., 1., 1., 1.))
dt = time.time() - t0
print(np.sum(res))
print("time:  ", dt)
