# pyquad

A drop-in replacment for `scipy.integrate.quad` which is much faster for repeat
integrals over a parameter space.

The library provides a thin, parallel wrapper for the [GNU Scientific Library (GSL)
integration routines](https://www.gnu.org/software/gsl/).

## Examples

The code below is a python example of integrating over a grid of parameters
using `scipy.integrate.quad`,

```python
import numpy as np
import scipy.integrate

def test_integrand_func(x, alpha, beta, i, j, k, l):
    return x * alpha * beta + i * j * k

grid = np.random.random((10000000, 2))

res = np.zeros(grid.shape[0])
for i in range(res.shape[0]):
    res[i] = scipy.integrate.quad(
        test_integrand_func, 0, 1, (grid[i, 0], grid[i, 1], 1.0, 1.0, 1.0, 1.0)
    )[0]
```

this can be replaced with,

```python
import numpy as np
import pyquad

def test_integrand_func(x, alpha, beta, i, j, k, l):
    return x * alpha * beta + i * j * k


grid = np.random.random((10000000, 2))

res = pyquad.quad_grid(test_integrand_func, 0, 1, grid, (1.0, 1.0, 1.0, 1.0))
```

which reduces the runtime from 107.8 seconds to 1.7 seconds on my laptop. This
can also be sped up be replacing `pyquad.quad_grid` with
`pyquad.parallel_quad_grid` which takes advantage of openMP. My laptop can get
a 3-4x speed up using the parallel version.

## Installing

To get started using the package you need to clone the repository,

```
git clone https://github.com/AshKelly/pyquad.git
```

and then go into the repository and run the setup file,

```
cd pyquad
python setup.py install
```

### Requirements

The packacge requires that cython and numpy are already installed. We also
require a C compiler (GCC) and the GNU Scientific Library (GSL) to be available
to link against. Using the Aptitude Package Manager these can be installed with,

```
sudo apt-get install libgsl-dev
sudo apt-get install libblas-dev
```

## Running the tests

The tests are currently incredibly primitive and just do a variety of answer
testing by comparing to `scipy.integrate.quad`. These can be run with,

```
pytest tests
```

inside the pyquad folder. You will need to install pytest for this (`pip
install pytest --user`)

## Examples

## Authors

* **Ashley Kelly**

## License

This project is licensed under the LGPL v3.0 License - see the [LICENSE.md](LICENSE.md) file for details
