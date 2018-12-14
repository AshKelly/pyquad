cimport cython
cimport numpy as np
import numpy as np

import inspect
import numba
from numba import cfunc

cdef extern from "quad.c":
    ctypedef double (*integrand)(double,  ...)

    ctypedef struct params:
        double * args
        integrand func

    cdef void _quad(int num_args, void * args, double * result, double * error)
    cdef void _quad_grid(int num_args, params args, int num, double * grid1,
                         double * grid2, double * result, double * error)


def quad(numba_integrand, np.float64_t[:] args):
    # Grab a pointer to the jitted function
    cdef integrand f = <integrand><size_t>numba_integrand.address
    cdef double result = 0.0
    cdef double error = 0.0

    # Parameter stucture
    cdef params p
    p.args = &args[0]
    p.func = f

    # Perform integral
    _quad(args.shape[0], <void *>&p, &result, &error);

    return result


def quad_grid(numba_integrand, np.float64_t[::1, :] grid, np.float64_t[:] args):
    # Grab a pointer to the jitted function
    cdef integrand f = <integrand><size_t>numba_integrand.address
    cdef int num = grid.shape[0]
    cdef np.float64_t[:] result, error
    result = np.zeros(num, "float64")
    error = np.zeros(num, "float64")

    # Parameter stucture
    cdef params p
    p.args = &args[0]
    p.func = f

    _quad_grid(args.shape[0], p, num, &grid[0, 0], &grid[0, 1],
               &result[0], &error[0]);

    return np.asarray(result)
