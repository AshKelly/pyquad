cimport cython
cimport numpy as np

import inspect
import numba
import numpy as np
import warnings

from numba import cfunc
from libc.stdlib cimport malloc, free

__version__ = '0.6'

INTEGRATION_MAP = {
    "qags": 0,
    "cquad": 1,
}

GSL_ERROR_DICT = {
    22 : "Integral is divergent, or slowly convergent.",
    21 : "Bad integrand behavior found in the integration interval.",
    18 : "Cannot reach tolerance because of roundoff error.",
    14 : "Failed to reach the specified tolerance.",
    13 : "Tolerance cannot be achieved with given epsabs and epsrel.",
    12 : "Tried to divide by zero.",
    11 : "Exceeded max number of iterations.",
    4 : "Iteration limit exceeds available workspace.",
    2 : "Output range error, e.g. exp(1e100).",
    1 : "Input domain error, e.g sqrt(-1).",
   -1 : "Integration failed!",
}


cdef extern from "quad.c":
    ctypedef double (*integrand)(double,  ...)

    ctypedef struct params:
        double * args
        double * grid_args
        integrand func

    cdef void _quad(int num_args, double a, double b, void * args,
                    double epsabs, double epsrel, size_t limit,
                    double * result, double * error, int * status,
                    int integration_method)
    cdef void _quad_grid(int num_args, int num_grid_args, double a, double b,
                    params args, int num, double epsabs, double epsrel,
                    size_t limit, double *, double * result, double * error,
                    int * status, int integration_method)
    cdef void _quad_grid_parallel_wrapper(int num_args, int num_grid_args,
                    double a, double b, params args, int num, double epsabs,
                    double epsrel, size_t limit, double *, double * result,
                    double * error, int num_threads, int pin_threads,
                    int * status, int integration_method) nogil


def cfunc_sig_generator(int num_args):
    sig = "float64("
    for i in range(num_args):
        sig += "float64,"
    sig += ")"
    return sig


def quad(py_integrand, double a, double b, args=(), epsabs=1e-7, epsrel=1e-7,
         limit=50, method="qags"):
    num_args = len(args)

    # Attempt to jit the integrand
    try:
        numba_integrand = cfunc(cfunc_sig_generator(num_args+1), nopython=True,
                                cache=True, fastmath=True)(py_integrand)
    except:
        msg = ("Failed to jit the integrand. Your integrand may use functions"+
               "which are unknown to numba and so nopython should be disabled!")
        raise NotImplementedError(msg)


    cdef integrand f = <integrand><size_t>numba_integrand.address
    cdef int integration_method = INTEGRATION_MAP[method]

    cdef double result = 0.0
    cdef double error = 0.0
    cdef int status = 0

    # Parameter stucture
    cdef params p
    p.args = <double *> malloc(sizeof(double) * num_args)
    for i in range(num_args):
        p.args[i] = args[i]
    p.func = f

    # Perform integral
    _quad(num_args, a, b,  <void *>&p, epsabs, epsrel, limit, &result, &error,
          &status, integration_method);

    free(p.args)

    if status:
        if status in GSL_ERROR_DICT:
            wrng_msg = GSL_ERROR_DICT[status]
        else:
            wrng_msg = "Integration failed."

        warnings.warn("[pyquad] " + wrng_msg)

    return result, error


@cython.boundscheck(False)
def quad_grid(py_integrand, double a, double b,
              np.ndarray[np.float64_t, ndim=2] grid,
              args=(), double epsabs=1e-7, double epsrel=1e-7, int limit=50,
              parallel=True, nopython=True, cache=True, int num_threads=8,
              int pin_threads=0, method="qags"):

    cdef int integration_method = INTEGRATION_MAP[method]

    # Ensure we have a tuple for the arguments
    if not isinstance(args, tuple):
        args = (args,)

    cdef int num_args = len(args)
    cdef int num_values = grid.shape[0]
    cdef int num_grid_args = grid.shape[1]

    # Flattened grid
    cdef np.float64_t[::1] flat_grid = grid.flatten()

    # Attempt to jit the integrand
    try:
        numba_integrand = cfunc(cfunc_sig_generator(num_args+num_grid_args+1),
                    nopython=nopython, cache=cache)(py_integrand)
    except:
        msg = ("Failed to jit the integrand. Your integrand may use functions"+
               "which are unknown to numba and so nopython should be disabled!")
        raise NotImplementedError(msg)

    cdef integrand f = <integrand><size_t>numba_integrand.address

    # Prepare arrays to store the integration results
    cdef np.float64_t[:] result = np.zeros(num_values, dtype="float64")
    cdef np.float64_t[:] error = np.zeros(num_values, dtype="float64")
    cdef int[:] status = np.zeros(num_values, dtype=np.dtype("i"))

    # Store the arguments which are fixed for each integral
    cdef params p
    p.args = <double *> malloc(sizeof(double) * num_args)
    for i in range(num_args):
        p.args[i] = args[i]
    p.func = f

    if parallel and nopython:
        if pin_threads == 1:
            warnings.warn("[pyquad] Pinned threads can cause strange behaviour"+
                          "in some environments - use this feature with care!")
        with nogil:
            _quad_grid_parallel_wrapper(num_args, num_grid_args, a, b, p,
                    num_values, epsabs, epsrel, limit, &flat_grid[0],
                    &result[0], &error[0], num_threads, pin_threads, &status[0],
                    integration_method)
    else:
        _quad_grid(num_args, num_grid_args, a, b, p, num_values, epsabs, epsrel,
                   limit, &flat_grid[0], &result[0], &error[0], &status[0],
                   integration_method)

    free(p.args)

    # check errors and print warnings
    for status_i in set(np.asarray(status)):
        if status_i:
            if status_i in GSL_ERROR_DICT:
                wrng_msg = GSL_ERROR_DICT[status_i]
            else:
                wrng_msg = "Integration failed."
            warnings.warn("[pyquad] " + wrng_msg)

    return np.asarray(result), np.asarray(error)
