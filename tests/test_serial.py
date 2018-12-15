import scipy.integrate
import pyquad
import numpy as np

def function1(x, a, b, c):
    return x*a*a + b + c


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

    print(res1, err1, res2, err2)
    assert np.abs(res1 - res2) < err1

def test_function3():
    res1, err1 = pyquad.quad(function3, 0., 4., (0.23, 0.7, 0.13))
    res2, err2  = scipy.integrate.quad(function3, 0., 4., (0.23, 0.7, 0.13),
                                       limit=200)


    print(res1, err1, res2, err2)
    assert np.abs(res1 - res2) < err1
