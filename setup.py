from setuptools import setup
from setuptools.extension import Extension
import sys
import numpy as np

link_args = []

if '--openmp' in sys.argv:
    sys.argv.remove('--openmp')
    link_args.append('-fopenmp')

src_files = ["pyquad/pyquad.pyx", "pyquad/integration/error.c",
             "pyquad/integration/qk.c", "pyquad/integration/qk21.c",
             "pyquad/integration/qk15.c", "pyquad/integration/qags.c",
             "pyquad/integration/workspace.c"
             ]

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
                           src_files,
                           extra_compile_args=link_args,
                           extra_link_args=link_args,
                           include_dirs=[np.get_include()],
                           language='c')],
)
