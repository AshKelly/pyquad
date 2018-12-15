# pyquad

A drop-in replacment for `scipy.integrate.quad` which is much faster when
doing repeat integrals over a range of parameters.

## Installing

To get started using the package you need to clone the repository,

```
git clone repo
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

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
