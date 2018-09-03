"""Helper functions for rectangle functions on tables

"""

from __future__ import division
import sys
import os
import time
import copy
from ..objects import *

__all__ = ['rect_diff', 'break_rect', 'unique_occs']


def rect_diff(rbase, rsub):
    runion = rbase.clip(rsub)
    if runion == rbase:
        return None
    if runion.width == 0 or runion.height == 0:
        return [rbase]
    # Test for full block of one dimension
    if rbase.width == runion.width:
        if rbase.top < runion.top:
            if rbase.bottom == runion.bottom:
                return [ptRect(rbase.left, rbase.top, runion.width, runion.top - rbase.top)]
            else:
                return [ptRect(rbase.left, rbase.top, runion.width, runion.top - rbase.top),
                        ptRect(rbase.left, runion.bottom, runion.width, rbase.bottom - runion.bottom)]
        else:
            return [ptRect(rbase.left, runion.bottom, runion.width, rbase.bottom - runion.bottom)]
    if rbase.height == runion.height:
        if rbase.left < runion.left:
            if rbase.right == runion.right:
                return [ptRect(rbase.left, rbase.top, runion.left - rbase.left, rbase.height)]
            else:
                return [ptRect(rbase.left, rbase.top, runion.left - rbase.left, rbase.height),
                        ptRect(runion.right, rbase.top, rbase.right - runion.right, rbase.height)]
        else:
            return [pg.Rect(runion.right, rbase.top, rbase.right - runion.right, rbase.height)]

    if rbase.top < runion.top:
        if rbase.left < runion.left:
            if rbase.right == runion.right:
                if rbase.bottom == runion.bottom:
                    return [ptRect(rbase.left, rbase.top, runion.left - rbase.left, rbase.height),
                            ptRect(runion.left, rbase.top, runion.width, runion.top - rbase.top)]
                else:
                    return [ptRect(rbase.left, rbase.top, rbase.width, runion.top - rbase.top),
                            ptRect(rbase.left, runion.top, runion.left - rbase.left, runion.height),
                            ptRect(rbase.left, runion.bottom, rbase.width, rbase.bottom - runion.bottom)]
            else:
                return [ptRect(rbase.left, rbase.top, rbase.width, runion.top - rbase.top),
                        ptRect(rbase.left, runion.top, runion.left - rbase.left, runion.height),
                        ptRect(runion.right, runion.top, rbase.right - runion.right, runion.height)]

        else:
            if rbase.bottom == runion.bottom:
                return [ptRect(rbase.left, rbase.top, rbase.width, runion.top - rbase.top),
                        ptRect(runion.right, runion.top, rbase.right - runion.right, rbase.bottom - runion.top)]
            else:
                return [ptRect(rbase.left, rbase.top, rbase.width, runion.top - rbase.top),
                        ptRect(runion.right, runion.top, rbase.right - runion.right, runion.height),
                        ptRect(rbase.left, runion.bottom, rbase.width, rbase.bottom - runion.bottom)]
    else:
        if rbase.left < runion.left:
            if rbase.right == runion.right:
                return [ptRect(rbase.left, rbase.top, runion.left - rbase.left, rbase.height),
                        ptRect(runion.left, runion.bottom, runion.width, rbase.bottom - runion.bottom)]
            else:
                return [ptRect(rbase.left, rbase.top, runion.left - rbase.left, rbase.height),
                        ptRect(runion.left, runion.bottom, runion.width,
                               rbase.bottom - runion.bottom),
                        ptRect(runion.right, rbase.top, rbase.right - runion.right, rbase.height)]
        else:
            return [ptRect(rbase.left, runion.bottom, rbase.width, rbase.bottom - runion.bottom),
                    ptRect(runion.right, runion.top, rbase.right - runion.right, runion.height)]


def break_rect(r, breaklist):
    if len(breaklist) == 0:
        return [r]
    b = breaklist[0]
    bleft = breaklist[1:]
    brk = rect_diff(r, b)
    if brk is None:
        return []
    ret = []
    for s in brk:
        ret.extend(break_rect(s, bleft))
    return ret


def unique_occs(occs, walls=[]):
    uos = []
    block = copy.copy(walls)
    for o in occs:
        nos = break_rect(o, block)
        uos.extend(nos)
        block.extend(nos)
    # Test code - check for overlaps
    for i in range(len(uos)):
        if uos[i].collidelist(uos[:i] + uos[i + 1:]) != -1:
            print (uos)
            raise RuntimeError("FOUND COLLLISION!!!")
    return uos
