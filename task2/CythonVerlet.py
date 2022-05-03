# install C++ tools from VS (Win SDK, MSVC), add libs to PATH
# python CythonVerlet.py build_ext --inplace --compiler=msvc

import numpy as np
from setuptools import setup
from Cython.Build import cythonize

setup(
      ext_modules = cythonize("CythonVerlet.pyx"),
      include_dirs=[np.get_include()]
)
    