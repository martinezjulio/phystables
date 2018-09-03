"""Some utilities used elsewhere in the package

"""

__all__ = ['mvstdnormcdf', 'mvnormcdf', 'euclidist']

from .mvncdf import mvstdnormcdf, mvnormcdf
import numpy as np


def euclidist(p1, p2):
    dx = p1[0]-p2[0]
    dy = p1[1]-p2[1]
    return np.sqrt(dx*dx + dy*dy)
