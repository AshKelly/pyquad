from setuptools import setup
from setuptools.extension import Extension
import os
import numpy as np

VERSION = "0.1"

link_args = ['-fopenmp', '-lgsl', '-lblas']
if os.name == "nt":
    std_libs = []
else:
    std_libs = ["m"]

setup(
    name='pyquad',
    version='0.0.1',
    install_requires=['numba', 'scipy'],
    ext_modules=[Extension("pyquad",
                           ["pyquad/pyquad.pyx"],
                           extra_compile_args=link_args,
                           extra_link_args=link_args,
                           libraries=std_libs,
                           include_dirs=[np.get_include()],
                           language='c')],
)
