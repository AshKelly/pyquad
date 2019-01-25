from setuptools import setup
from setuptools.extension import Extension
import sys

try:
    import cython
    import numpy as np
except ImportError:
    raise ImportError(
"""Could not import cython or numpy. Building pyquad from source requires
cython and numpy to be installed. Please install these packages using
the appropriate package manager for your python environment.""")

link_args = ['-lgsl', '-lgslcblas']

if '--openmp' in sys.argv:
    sys.argv.remove('--openmp')
    link_args.append('-fopenmp')

setup(
    name='pyquad',
    version='0.0.2.5',
    author="Ashley J Kelly",
    author_email="a.j.kelly@durham.ac.uk",
    description="A python wrapper for the GSL integration routines",
    url="https://github.com/AshKelly/pyquad",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=['cython', 'numpy', 'wheel', 'scipy', 'numba', 'pytest'],
    ext_modules=[Extension("pyquad",
                           ["pyquad/pyquad.pyx"],
                           extra_compile_args=link_args,
                           extra_link_args=link_args,
                           include_dirs=[np.get_include()],
                           language='c')],
)
