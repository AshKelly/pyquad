[![Build Status](https://travis-ci.com/AshKelly/pyquad.svg?branch=master)](https://travis-ci.com/AshKelly/pyquad)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3936959.svg)](https://doi.org/10.5281/zenodo.3936959)

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

res, err = pyquad.quad_grid(test_integrand_func, 0, 1, grid, (1.0, 1.0, 1.0, 1.0))
```

which reduces the runtime significantly. For an example of the performance see
the benchmarks below.

## Benchmarks

We first compare a test integral in both pyquad and scipy,

![Comparisons to scipy.integrate.quad()](https://raw.githubusercontent.com/AshKelly/pyquad/master/benchmarking/benchmarks.png)

and then we look in more detail at the scaling of pyquad with an increased
thread count,

![Scaling tests](https://raw.githubusercontent.com/AshKelly/pyquad/master/benchmarking/benchmarks_pyquad.png)

These benchmarks were carried out on cosma7 which has 28 cores (2x Intel Xeon
Gold 5120 CPU @ 2.20GHz). Perfect scaling was never to be expected, given the problem
becomes completely memorybound with a high core count.

## Installing

To get started using the package you can use pip
to download wheels for linux or osx,


```
pip install pyquad --user
```

or you can clone the repository,

```
git clone https://github.com/AshKelly/pyquad.git
```

and then go into the repository and run the setup file,

```
cd pyquad
python setup.py install
```

### Requirements

The package requires that numpy is already installed and we require a C
compiler to build from source.

## Running the tests

The tests are currently incredibly primitive and just do a variety of answer
testing by comparing to `scipy.integrate.quad`. These can be run with,

```
pytest tests
```

inside the pyquad folder. You will need to install pytest and scipy for this
(`pip install pytest scipy --user`)
i

## History

I started to write components of this to help speed up some integrals for
[PyAutoLens](https://github.com/Jammy2211/PyAutoLens/). As it happened, a few
other people in my department were also interested. I attempted to neaten up
the API and roll it out for easy use.

If you want to contribute or want any extra feature implementing please just
get in touch via email or a pull request.

## Authors

* **Ashley Kelly** (a.j.kelly@durham.ac.uk)
* **Arnau Quera** (arnau.quera-bofarull@durham.ac.uk)

## Citations

Please use the following citation:

```
@software{kelly:2020,
  author       = {Ashley J. Kelly},
  title        = {pyquad},
  month        = jul,
  year         = 2020,
  publisher    = {Zenodo},
  version      = {0.6.4},
  doi          = {10.5281/zenodo.3936959},
  url          = {https://doi.org/10.5281/zenodo.3936959}
}
```

## License

This project is licensed under the GPL v3.0 License - see the
[LICENSE.md](LICENSE.md) file for details
