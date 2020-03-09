import matplotlib.pyplot as plt
import scipy.integrate
import pyquad
import numpy as np
import time

from jit import jit_integrand


np.random.seed(101)

PROBLEM_SIZES = [1000,10000,100000,1000000]
REPEATS = 1
NUM_THREADS = [1, 2, 8]
COLORS = ["red", "blue", "green", "purple", "orange"]


INTEGRAL_METHOD = "qags"

SCIPY_TTS = []
PYQUAD_TTS = {}


def test_func(x, a, b, c):
    return a*a / (x + 1.0) + b * np.sin(np.sqrt(x)) + c * np.log(x + 1) + np.tanh(x*a)


@jit_integrand
def test_func_jit(x, a, b, c):
    return a*a / (x + 1.0) + b * np.sin(np.sqrt(x)) + c * np.log(x + 1) + np.tanh(x*a)


def benchmark_pyquad():
    for threads in NUM_THREADS:
        PYQUAD_TTS[threads] = []

    for problem in PROBLEM_SIZES:
        np.random.seed(101)
        grid = np.random.random((problem, 3))

        for threads in NUM_THREADS:
            t0 = time.time()
            for repeat in range(REPEATS):
                res = pyquad.quad_grid(test_func, 0.0, 2.0, grid, method=INTEGRAL_METHOD,
                                       num_threads=threads)[0]
            t1 = time.time()

            PYQUAD_TTS[threads].append((t1 - t0)/REPEATS)


def benchmark_scipy_jit():
    for problem in PROBLEM_SIZES:
        np.random.seed(101)
        grid = np.random.random((problem, 3))
        res = np.zeros(grid.shape[0])

        t0 = time.time()
        for repeat in range(REPEATS):
            for i in range(res.shape[0]):
                res[i] = scipy.integrate.quad(
                    test_func_jit, 0, 2.0, (grid[i, 0], grid[i, 1], grid[i, 2])
                )[0]
        t1 = time.time()

        SCIPY_TTS.append((t1 - t0)/REPEATS)

if __name__ == "__main__":
    benchmark_pyquad()
    benchmark_scipy_jit()


    fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=300)

    ax.plot(PROBLEM_SIZES, SCIPY_TTS, color="black", label="scipy jit")
    ax.scatter(PROBLEM_SIZES, SCIPY_TTS, color="black", marker="x")

    for color, threads in zip(COLORS, NUM_THREADS):
        ax.plot(PROBLEM_SIZES, PYQUAD_TTS[threads], color=color, label="pyquad ({0} threads)".format(threads))
        ax.scatter(PROBLEM_SIZES, PYQUAD_TTS[threads], color=color, marker="x")

    ax.plot(PROBLEM_SIZES, np.asarray(PROBLEM_SIZES)/PROBLEM_SIZES[0]*PYQUAD_TTS[8][1], color="grey",
               linestyle="--", label="Linear")

    ax.legend(loc="best")

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.set_xlabel("Number of integrations / #")
    ax.set_ylabel("Wall clock / s")

    fig.tight_layout()
    fig.savefig("benchmarks.png", dpi=300)


    fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=300)

    for i, color, problem in zip(range(len(PROBLEM_SIZES)), COLORS, PROBLEM_SIZES):
        if problem == 1000000:
            TTS = []
            for threads in NUM_THREADS:
                TTS.append(PYQUAD_TTS[threads][i])
            ax.plot(NUM_THREADS, TTS, color=color, label="{0} integrations".format(problem))
            ax.scatter(NUM_THREADS, TTS, color=color, marker="s")

    ax.plot(NUM_THREADS, TTS[0] / np.asarray(NUM_THREADS), color="grey",
               linestyle="--", label="Linear")

    ax.legend(loc="best")

    ax.set_xlabel("Number of threads / #")
    ax.set_ylabel("Wall clock / s")

    ax.set_xlim(0, max(NUM_THREADS)+1)
    ax.set_ylim(0, max(NUM_THREADS)+1)

    fig.tight_layout()
    fig.savefig("benchmarks_pyquad.png", dpi=300)
