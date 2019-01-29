from setuptools import setup
from setuptools.extension import Extension
import sys

try:
    import numpy as np
    import cython
except ImportError:
    raise ImportError("Please install numpy and cython before building pyquad!")

link_args = ["-std=c99"]

# detect if openmp was passed, if so enable and strip
if '--openmp' in sys.argv:
    sys.argv.remove('--openmp')
    link_args.append('-fopenmp')
    link_args.append('-D OMP_ON=1')

src_files = ["pyquad/pyquad.pyx", "pyquad/integration/error.c",
             "pyquad/integration/qk.c", "pyquad/integration/qk21.c",
             "pyquad/integration/qk15.c", "pyquad/integration/qags.c",
             "pyquad/integration/workspace.c"
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
    version='0.0.3.5',
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
    install_requires=['cython', 'numpy', 'numba'],
    extras_require={
        'test': ['pytest', 'scipy'],
    },
    ext_modules=ext_modules,
)
