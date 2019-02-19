cimport cython
cimport numpy as np

import inspect
import numba
import numpy as np

from numba import cfunc
from libc.stdlib cimport malloc, free

cfunc_sigs = {}
cfunc_sigs[1] = "float64(float64)"
cfunc_sigs[2] = "float64(float64, float64)"
cfunc_sigs[3] = "float64(float64, float64, float64)"
cfunc_sigs[4] = "float64(float64, float64, float64, float64)"
cfunc_sigs[5] = "float64(float64, float64, float64, float64, float64)"
cfunc_sigs[6] = "float64(float64, float64, float64, float64, float64, float64)"
cfunc_sigs[7] = "float64(float64, float64, float64, float64, float64, float64, float64)"
cfunc_sigs[8] = "float64(float64, float64, float64, float64, float64, float64, float64, float64)"
cfunc_sigs[9] = "float64(float64, float64, float64, float64, float64, float64, float64, float64, float64)"
cfunc_sigs[10] = "float64(float64, float64, float64, float64, float64, float64, float64, float64, float64, float64)"
cfunc_sigs[11] = "float64(float64, float64, float64, float64, float64, float64, float64, float64, float64, float64, float64)"
cfunc_sigs[12] = "float64(float64, float64, float64, float64, float64, float64, float64, float64, float64, float64, float64, float64)"


cdef extern from "quad.c":
    ctypedef double (*integrand)(double,  ...)

    ctypedef struct params:
        double * args
        double * grid_args
        integrand func

    cdef void _quad(int num_args, double a, double b, void * args,
                    double epsabs, double epsrel, size_t limit,
                    double * result, double * error)
    cdef void _quad_grid(int num_args, int num_grid_args, double a, double b,
                    params args, int num, double epsabs, double epsrel,
                    size_t limit, double *, double * result, double * error)
    cdef void _quad_grid_parallel_wrapper(int num_args, int num_grid_args,
                    double a, double b, params args, int num, double epsabs,
                    double epsrel, size_t limit, double *, double * result,
                    double * error) nogil


def quad(py_integrand, double a, double b, args=(), epsabs=1e-7, epsrel=1e-7,
         limit=200):
    num_args = len(args)

    # Jit the integrand
    numba_integrand = cfunc(cfunc_sigs[num_args+1], nopython=True, cache=True)(py_integrand)
    cdef integrand f = <integrand><size_t>numba_integrand.address

    cdef double result = 0.0
    cdef double error = 0.0

    # Parameter stucture
    cdef params p
    p.args = <double *> malloc(sizeof(double) * num_args)
    for i in range(num_args):
        p.args[i] = args[i]
    p.func = f

    # Perform integral
    _quad(num_args, a, b,  <void *>&p, epsabs, epsrel, limit, &result, &error);

    free(p.args)

    return result, error


def quad_grid(py_integrand, double a, double b,
              np.ndarray[np.float64_t, ndim=2] grid,
              args=(), double epsabs=1e-7, double epsrel=1e-7, int limit=250,
              parallel=True, nopython=True, cache=True):

    # Ensure we have a tuple for the arguments
    if not isinstance(args, tuple):
        args = (args,)

    cdef int num_args = len(args)
    cdef int num_values = grid.shape[0]
    cdef int num_grid_args = grid.shape[1]

    # Flattened grid
    cdef np.float64_t[::1] flat_grid = grid.flatten()

    # jit the integrand
    numba_integrand = cfunc(cfunc_sigs[num_args+num_grid_args+1],
                            nopython=nopython, cache=cache)(py_integrand)
    cdef integrand f = <integrand><size_t>numba_integrand.address

    # Prepare arrays to store the integration results
    cdef np.float64_t[:] result = np.zeros(num_values, "float64")
    cdef np.float64_t[:] error = np.zeros(num_values, "float64")

    # Store the arguments which are fixed for each integral
    cdef params p
    p.args = <double *> malloc(sizeof(double) * num_args)
    for i in range(num_args):
        p.args[i] = args[i]
    p.func = f

    if parallel:
        with nogil:
            _quad_grid_parallel_wrapper(num_args, num_grid_args, a, b, p,
                    num_values, epsabs, epsrel, limit, &flat_grid[0],
                    &result[0], &error[0])
    else:
        _quad_grid(num_args, num_grid_args, a, b, p, num_values, epsabs, epsrel,
                   limit, &flat_grid[0], &result[0], &error[0])

    free(p.args)

    return np.asarray(result), np.asarray(error)
