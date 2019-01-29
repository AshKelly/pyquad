from setuptools import setup
from setuptools.extension import Extension
import sys

from pyquad import __version__

try:
    import numpy as np
except ImportError:
    raise ImportError("Please install numpy before building pyquad!")

link_args = ["-std=c99"]

if '--openmp' in sys.argv:
    sys.argv.remove('--openmp')
    link_args.append('-fopenmp')
    link_args.append('-D OMP_ON=1')

src_files = ["pyquad/pyquad.pyx", "pyquad/integration/error.c",
             "pyquad/integration/qk.c", "pyquad/integration/qk21.c",
             "pyquad/integration/qk15.c", "pyquad/integration/qags.c",
             "pyquad/integration/workspace.c"
             ]

setup(
    name='pyquad',
    version=__version__,
    author="Ashley J Kelly",
    author_email="a.j.kelly@durham.ac.uk",
    description="A python wrapper for the GSL integration routines",
    url="https://github.com/AshKelly/pyquad",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=['cython', 'numpy', 'numba'],
    extras_require={
        'test': ['pytest', 'scipy'],
    },
    ext_modules=[Extension("pyquad",
                           src_files,
                           extra_compile_args=link_args,
                           extra_link_args=link_args,
                           include_dirs=[np.get_include()],
                           language='c')],
)
