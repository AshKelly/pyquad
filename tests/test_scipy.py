import scipy.integrate
import pyquad
import numpy as np


def function1(x, a, b, c):
    return x*a*a + c*b - c*b / (x  + 1e-5)


def function2(x, a, b, c):
    return a*a / (x + 1.0) + b * (1 - x) + c


def function3(x, a, b, c):
    return a*a / (x + 1.0) + b * np.sin(x) + c * np.log(x + 1)


def test_function1():
    res1, err1 = pyquad.quad(function1, 0., 1., (0.3, 0.1, 0.7))
    res2, err2  = scipy.integrate.quad(function1, 0., 1., (0.3, 0.1, 0.7),
                                       limit=200)
    assert np.abs(res1 - res2) < err1


def test_function2():
    res1, err1 = pyquad.quad(function2, 0., 1., (0.99, 2.1, 1.3))
    res2, err2  = scipy.integrate.quad(function2, 0., 1., (0.99, 2.1, 1.3),
                                       limit=200)
    assert np.abs(res1 - res2) < err1


def test_function3():
    res1, err1 = pyquad.quad(function3, 0., 4., (0.23, 0.7, 0.13))
    res2, err2  = scipy.integrate.quad(function3, 0., 4., (0.23, 0.7, 0.13),
                                       limit=200)
    assert np.abs(res1 - res2) < err1


def test_grid_single_column():
    np.random.seed(101)
    grid = np.random.random((100, 1))

    res = np.zeros(grid.shape[0])
    for i in range(res.shape[0]):
        res[i] = scipy.integrate.quad(
            function1, 0, 1, (grid[i, 0], 1.0, 1.0)
        )[0]

    res2 = pyquad.quad_grid(function1, 0, 1, grid, (1.0, 1.0))[0]

    assert np.abs(np.sum(res) - np.sum(res2)) < 1e-5


def test_grid_one_column_with_args():
    np.random.seed(101)
    grid = np.random.random((100, 1))

    res = np.zeros(grid.shape[0])
    for i in range(res.shape[0]):
        res[i] = scipy.integrate.quad(
            function2, 0, 1, (grid[i, 0], 1.0, 2.0),
        )[0]

    res2 = pyquad.quad_grid(function2, 0, 1, grid, args=(1.0, 2.0))[0]

    assert np.abs(np.sum(res) - np.sum(res2)) < 1e-5


def test_grid_two_column_with_args():
    np.random.seed(101)
    grid = np.random.random((100, 2))

    res = np.zeros(grid.shape[0])
    for i in range(res.shape[0]):
        res[i] = scipy.integrate.quad(
            function2, 0, 1, (grid[i, 0], grid[i, 1], 1.0),
        )[0]

    res2 = pyquad.quad_grid(function2, 0, 1, grid, args=(1.0))[0]

    assert np.abs(np.sum(res) - np.sum(res2)) < 1e-5


def test_grid_full_column():
    np.random.seed(101)
    grid = np.random.random((100, 3))

    res = np.zeros(grid.shape[0])
    for i in range(res.shape[0]):
        res[i] = scipy.integrate.quad(
            function1, 0, 1, (grid[i, 0], grid[i, 1], grid[i, 2])
        )[0]

    res2 = pyquad.quad_grid(function1, 0, 1, grid)[0]

    assert np.abs(np.sum(res) - np.sum(res2)) < 1e-5
