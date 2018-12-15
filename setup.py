from setuptools import setup
from setuptools.extension import Extension
import os
import numpy as np

link_args = ['-fopenmp', '-lgsl', '-lblas']
if os.name == "nt":
    std_libs = []
else:
    std_libs = ["m"]

setup(
    name='pyquad',
    version='0.0.4',
    author="Ashley J Kelly",
    author_email="a.j.kelly@durham.ac.uk",
    description="A python wrapper for the GSL integration routines",
    url="https://github.com/AshKelly/pyquad",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=['cython', 'scipy', 'pytest', 'numba'],
    ext_modules=[Extension("pyquad",
                           ["pyquad/pyquad.pyx"],
                           extra_compile_args=link_args,
                           extra_link_args=link_args,
                           libraries=std_libs,
                           include_dirs=[np.get_include()],
                           language='c')],
)
