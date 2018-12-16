
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
        double * * grid_args
        integrand func

    cdef void _quad(int num_args, double a, double b, void * args,
                    double epsabs, double epsrel, size_t limit,
                    double * result, double * error)
    cdef void _quad_grid(int num_args, int num_grid_args,  double a, double b,
                         params args, int num, double epsabs, double epsrel,
                         size_t limit, double * result, double * error)
    #cdef void _quad_grid_parallel(int num_args,  double a, double b, params args,
    #                     int num, double * grid1, double * grid2,
    #                     double epsabs, double epsrel, size_t limit,
    #                     double * result, double * error)


def quad(py_integrand, double a, double b, args=(), epsabs=1e-7, epsrel=1e-7,
         limit=200):
    num_args = len(args)
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


def quad_grid(py_integrand, double a, double b, np.float64_t[:, :] grid,
              args=(), epsabs=1e-7, epsrel=1e-7, limit=200, parallel=False):
    # Make sure the array is fortran contiguous
    grid = np.asfortranarray(grid)
    if not isinstance(args, tuple):
        args = (args,)

    cdef int num_args = len(args)
    cdef int num_values = grid.shape[0]
    cdef int num_grid_args = grid.shape[1]

    # jit the integrand
    numba_integrand = cfunc(cfunc_sigs[num_args+num_grid_args+1], nopython=True,
                            cache=True)(py_integrand)
    cdef integrand f = <integrand><size_t>numba_integrand.address

    # prepare arrays to store the integration results
    cdef np.float64_t[:] result = np.zeros(num_values, "float64")
    cdef np.float64_t[:] error = np.zeros(num_values, "float64")

    cdef params p

    # Store the arguments which are fixed for each integral
    p.args = <double *> malloc(sizeof(double) * num_args)
    for i in range(num_args):
        p.args[i] = args[i]

    # Store pointers to the columns in the grid input
    p.grid_args = <double * *> malloc(sizeof(double *) * num_grid_args)
    for i in range(num_grid_args):
        p.grid_args[i] = &grid[0, i]

    # Pointer to the jitted integrand
    p.func = f

    _quad_grid(num_args, num_grid_args, a, b, p, num_values, epsabs,
               epsrel, limit, &result[0], &error[0])

    free(p.args)
    free(p.grid_args)

    return np.asarray(result), np.asarray(error)
