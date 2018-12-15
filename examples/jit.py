import numba
from numba import cfunc
from numba.types import intc, CPointer, float64
from scipy import LowLevelCallable
import inspect

def jit_integrand(integrand_function):
    jitted_function = numba.jit(integrand_function, nopython=True)
    no_args = len(inspect.getfullargspec(integrand_function).args)

    wrapped = None

    if no_args == 4:
        def wrapped(n, xx):
            return jitted_function(xx[0], xx[1], xx[2], xx[3])
    elif no_args == 5:
        def wrapped(n, xx):
            return jitted_function(xx[0], xx[1], xx[2], xx[3], xx[4])
    elif no_args == 6:
        def wrapped(n, xx):
            return jitted_function(xx[0], xx[1], xx[2], xx[3], xx[4], xx[5])
    elif no_args == 7:
        def wrapped(n, xx):
            return jitted_function(xx[0], xx[1], xx[2], xx[3], xx[4], xx[5], xx[6])
    elif no_args == 8:
        def wrapped(n, xx):
            return jitted_function(xx[0], xx[1], xx[2], xx[3], xx[4], xx[5], xx[6], xx[7])
    elif no_args == 9:
        def wrapped(n, xx):
            return jitted_function(xx[0], xx[1], xx[2], xx[3], xx[4], xx[5], xx[6], xx[7], xx[8])
    elif no_args == 10:
        def wrapped(n, xx):
            return jitted_function(xx[0], xx[1], xx[2], xx[3], xx[4], xx[5], xx[6], xx[7], xx[8], xx[9])
    elif no_args == 11:
        def wrapped(n, xx):
            return jitted_function(xx[0], xx[1], xx[2], xx[3], xx[4], xx[5], xx[6], xx[7], xx[8], xx[9], xx[10])

    cf = cfunc(float64(intc, CPointer(float64)))

    return LowLevelCallable(cf(wrapped).ctypes)

