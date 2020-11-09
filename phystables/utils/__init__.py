"""Some utilities used elsewhere in the package

"""

__all__ = ['mvstdnormcdf', 'mvnormcdf', 'euclidist', 'approx_eq',
           'check_counterclockwise', 'safe_winding_vertices']

from .mvncdf import mvstdnormcdf, mvnormcdf
import numpy as np
import copy


def euclidist(p1, p2):
    dx = p1[0]-p2[0]
    dy = p1[1]-p2[1]
    return np.sqrt(dx*dx + dy*dy)

def approx_eq(x, y, tol=1e-8):
    return (abs(x - y) < tol)


def check_counterclockwise(pointlist):
    """Checks if a series of vertices is counterclockwise-winding

    Args:
        pointlist (list): A list of (x,y) vertices

    Returns:
        Boolean indicating whether the vertices are counterclockwise-winding
    """
    pointlist = [(p[0], p[1]) for p in pointlist]
    if len(pointlist) < 3:
        return True
    a = np.array(pointlist[0])
    b = np.array(pointlist[1])
    for i in range(2, len(pointlist)):
        c = np.array(pointlist[i])
        l1 = b - a
        l2 = c - b
        if np.cross(l1, l2) > 0:
            return False
        a = b
        b = c
    c = np.array(pointlist[0])
    l1 = b - a
    l2 = c - b
    if np.cross(l1, l2) > 0:
        return False
    return True


def safe_winding_vertices(pointlist):
    if check_counterclockwise(pointlist):
        return pointlist
    else:
        pl2 = copy.deepcopy(pointlist)
        pl2.reverse()
        return pl2
