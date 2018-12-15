import scipy.integrate
import pyquad
import matplotlib.pyplot as plt
import numpy as np


def func(x, a, b, c):
    return a * a / x + b * np.sin(x) + c * np.log(x + 1)


plt.figure(figsize=(10, 10))

for lim in range(200, 1000, 50):
    res, err = scipy.integrate.quad(func, 0.0, 1.0, (0.3, 0.1, 0.7), limit=lim)

    plt.errorbar(lim, res, yerr=err, c="k", marker="x")

for lim in range(200, 1000, 50):
    res, err = pyquad.quad(func, 0.0, 1.0, (0.3, 0.1, 0.7), limit=lim)

    plt.errorbar(lim + 5, res, yerr=err, c="red", marker="x")

plt.ylabel("Integral and error from scipy.integrate.quad and pyquad.quad")
plt.xlabel("Limit")

plt.savefig("results.png")
plt.show()
