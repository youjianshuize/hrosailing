[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![linter](https://github.com/hrosailing/hrosailing/actions/workflows/linting.yml/badge.svg)](https://github.com/hrosailing/hrosailing/actions/workflows/linting.yml)
[![tester](https://github.com/hrosailing/hrosailing/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/hrosailing/hrosailing/actions/workflows/build-and-test.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/hrosailing/hrosailing/badge)](https://www.codefactor.io/repository/github/hrosailing/hrosailing)

<p align="center">
    <img src="https://raw.githubusercontent.com/hrosailing/hrosailing/main/logo.png" width=300px height=300px alt="hrosailing">
</p>

hrosailing - Sailing made in Rostock
====================================

You can find the documentation [here](https://hrosailing.github.io/hrosailing/ "hrosailing").

### Compatibility 
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)

The `hrosailing` module might also be compatible (in large) with earlier versions of Python (`3.5`, `3.6`), together with some earlier
version of some of the used packages, namely `numpy`, `scipy`, and `matplotlib`, aswell as Python `3.10`, but since it was released 
recently, we can't guarantee that.


### Installation

The recommended way to install `hrosailing` is with 
[pip](http://pypi.python.org/pypi/pip/):
    
    pip install hrosailing

[![PyPI version](https://badge.fury.io/py/hrosailing.svg)](https://badge.fury.io/py/hrosailing)


### License 

The `hrosailing` module is published under the [Apache 2.0 License](https://choosealicense.com/licenses/apache-2.0/), see also [License](LICENSE)

### Examples

Use the hrosailing module for reading, writing and displaying polar performance diagrams.
For a first example, download some table with performance diagram data and save it as testdata.csv.
In this example, we use the data available [here](https://www.seapilot.com/wp-content/uploads/2018/05/60ftmono.txt).
This data is given in a tab seperated format which is supported by the keyword ```fmt=array``` of the ```from_csv``` method.
Since this data is only defined for wind angles between 0° and 180° we use the symmetrize function to obtain a symmetric polar diagram with wind angles between 0° and 360°.

```python
import hrosailing.polardiagram as pol
pd = pol.from_csv("testdata.csv", fmt="array").symmetrize()
```

We can use the supported plot functions to get visualizations of the polar diagram.

```python
import matplotlib.pyplot as plt

ws = [10, 20, 30]

pd.plot_polar(ws=ws, ax=plt.subplot(2, 2, 1, projection="polar"))
pd.plot_convex_hull(ws=ws, ax=plt.subplot(2, 2, 2, projection="polar"))
pd.plot_flat(ws=ws, ax=plt.subplot(2, 2, 3))
pd.plot_color_gradient(ax=plt.subplot(2, 2, 4))

plt.show()
```

This results in the following matplotlib diagram:

![flat_plots](https://user-images.githubusercontent.com/70914876/146026223-fc58a914-9b01-47ae-bf9c-6429113dbf4a.png)

