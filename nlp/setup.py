from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules = cythonize("sentiment_analysis.pyx"),
    include_dirs=[numpy.get_include()]
)