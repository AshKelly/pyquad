from setuptools import setup
from setuptools.extension import Extension
import sys

try:
    import numpy as np
    import cython
except ImportError:
    raise ImportError("Please install numpy and cython before building pyquad!")

link_args = ["-std=c99"]

from sys import platform
if platform == "linux" or platform == "linux2":
    link_args.append("-D LINUX_MACH=1")

src_files = ["pyquad/pyquad.pyx", "pyquad/integration/error.c",
             "pyquad/integration/qk.c", "pyquad/integration/qk21.c",
             "pyquad/integration/qk15.c", "pyquad/integration/qags.c",
             "pyquad/integration/workspace.c", "pyquad/integration/cquad.c",
             "pyquad/integration/cquad_const.c", "pyquad/integration/infnan.c",
             "pyquad/integration/fdiv.c"
             ]

ext_modules=[Extension("pyquad",
                       src_files,
                       extra_compile_args=link_args,
                       extra_link_args=link_args,
                       include_dirs=[np.get_include()],
                       language='c')]

# Cythonize our modules
from Cython.Build import cythonize
ext_modules = cythonize(ext_modules,
                        compiler_directives={'language_level': 3})

setup(
    name='pyquad',
    version='0.6.2',
    author="Ashley J Kelly",
    license="LGPL-3.0",
    author_email="a.j.kelly@durham.ac.uk",
    description="A python wrapper for the GSL integration routines",
    url="https://github.com/AshKelly/pyquad",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License (GPL)"
    ],
    install_requires=['cython>=0.28.0', 'numpy>=1.16.0', 'numba>=0.40.0'],
    extras_require={
        'test': ['pytest', 'scipy'],
    },
    ext_modules=ext_modules,
)
