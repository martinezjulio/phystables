"""Trial objects for storing uninstantiated SimpleTables

Trials come in a number of flavors: SimpleTrial, PongTrial, and RedGreenTrial.
These generally have similar functionality and unpack to be a SimpleTable

Examples:

    > TBD

"""

from __future__ import division, print_function
from future.builtins.misc import input
import sys
import os
import warnings
from .tables import *
from .constants import *
import pickle
from math import sqrt
import json
import numpy as np

__all__ = ['SimpleTrial', 'RedGreenTrial', 'PongTrial', 'load_trial',
           'load_json', 'load_pickle']

def _safe_listify(tolist):
    """Turns things into a list in a way that respects nesting"""
    if hasattr(tolist, '__iter__') or type(tolist).__name__ == 'Color':
        return [_safe_listify(l) for l in tolist]
    else:
        return tolist

def _unnumpy(tolist):
    """Removes numpy types from items in a list"""
    if hasattr(tolist, '__iter__') or type(tolist).__name__ == 'Color':
        return [_unnumpy(l) for l in tolist]
    else:
        if type(tolist).__module__ == 'numpy':
            return tolist.item()
        else:
            return tolist


# Solution to making sure np objects can be serialized
# From https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class SimpleTrial(object):
    """The most basic trial type

    Has basic functionality to create trials, but only checks that objects
    are not overlapping
    """

    def __init__(self, name, dims, closed_ends=[LEFT, RIGHT, BOTTOM, TOP],
                 background_cl=WHITE, def_ball_vel=600, def_ball_rad=20,
                 def_ball_cl=BLUE, def_pad_len=100, def_wall_cl=BLACK,
                 def_occ_cl=GREY, def_pad_cl=BLACK):
        """Initializes a SimpleTrial

        Args:
            name (str): The name of the trial
            dims ([int,int]): The [x,y] dimensions of the trial
            closed_ends (list): A list of the directions to close off
            background_cl (color): The color to paint the table background
            def_ball_vel (float): The default speed to normalize the ball to
            def_ball_rad (int): The ball radius if not otherwise set
            def_ball_cl (color): Default color of the ball
            def_pad_len (int): Default length of a paddle in px
            def_wall_cl (color): Default color of Wall objects
            def_occ_cl (color): Default color of Occluders
            def_pad_cl (color): Default color of Paddle objects
        """
        self.name = name
        self.dims = dims
        self.ce = closed_ends
        self.bkc = background_cl
        self.dbr = def_ball_rad
        self.dbc = def_ball_cl
        self.dpl = def_pad_len
        self.dwc = def_wall_cl
        self.doc = def_occ_cl
        self.dpc = def_pad_cl
        self.dbv = def_ball_vel

        self.ball = None
        self.normwalls = []
        self.abnormwalls = []
        self.occs = []
        self.goals = []
        self.paddle = None

    def add_ball(self, initpos, initvel, rad=None, color=None, elast=1.):
        """Add a ball to this trial

        Args:
            TBD
        """
        if self.ball is not None:
            raise Exception('Cannot add a second ball to a SimpleTrial')
        if rad is None:
            rad = self.dbr
        if color is None:
            color = self.dbc
        self.ball = (initpos, initvel, rad, color, elast)

    def add_wall(self, upperleft, lowerright, color=None, elast=1.):
        """Add a wall to this trial

        Args:
            TBD
        """
        if color is None:
            color = self.dwc
        self.normwalls.append((upperleft, lowerright, color, elast))

    def add_abnorm_wall(self, vertexlist, color=None, elast=1.):
        """Add a non-rectangular wall to this trial

        Args:
            TBD
        """
        if color is None:
            color = self.dwc
        self.abnormwalls.append((vertexlist, color, elast))

    def add_goal(self, upperleft, lowerright, onreturn, color=None):
        """Add a goal to this trial

        Args:
            TBD
        """
        self.goals.append((upperleft, lowerright, onreturn, color))

    def add_paddle(self, p1, p2, padlen, padwid, hitret, acol=BLACK,
                   iacol=GREY, pthcol=None, elast=1.):
        """Add a paddle to this trial

        Args:
            TBD
        """
        self.paddle = (p1, p2, padlen, padwid, hitret,
                       acol, iacol, pthcol, elast)

    def add_occ(self, upperleft, lowerright, color=None):
        """Add an occluder to this trial

        Args:
            TBD
        """
        if color is None:
            color = self.doc
        self.occs.append((upperleft, lowerright, color))

    def make_table(self, soffset=None, paddleasgoal=False):
        """Make the trial into a SimpleTable

        Args:
            TBD
        """
        try:
            import pygame
            tb = SimpleTable(self.dims, self.ce, self.bkc, self.dbr, self.dbc,
                             self.dpl, self.dwc, self.doc, self.dpc, True,
                             soffset)
        except ImportError:
            tb = SimpleTable(self.dims, self.ce, self.dbr, self.dpl, True)
        if self.ball:
            tb.add_ball(self.ball[0], self.ball[1],
                       self.ball[2], self.ball[3], self.ball[4])
        if self.paddle:
            if paddleasgoal:
                p1 = self.paddle[0]
                p2 = self.paddle[1]
                if p1[0] == p2[0]:
                    if paddleasgoal == 'bottom':
                        tb.add_goal(p1, (p2[0], self.dims[1]),
                                   self.paddle[4], LIGHTGREY)
                    else:
                        tb.add_goal((p1[0], 0), p2, self.paddle[4], LIGHTGREY)
                elif p1[1] == p2[1]:
                    if paddleasgoal == 'right':
                        tb.add_goal(
                            p1, (self.dims[0], p2[1]), self.paddle[4],
                            LIGHTGREY)
                    else:
                        tb.add_goal((0, p1[1]), p2, self.paddle[4], LIGHTGREY)
                else:
                    raise Exception('Paddle must be vertical or horizontal')
            else:
                tb.add_paddle(self.paddle[0], self.paddle[1], self.paddle[2],
                             self.paddle[3], self.paddle[4], True,
                             self.paddle[5], self.paddle[6], self.paddle[7],
                             self.paddle[8], False)
        for w in self.normwalls:
            tb.add_wall(w[0], w[1], w[2], w[3])
        for w in self.abnormwalls:
            tb.add_abnorm_wall(w[0], w[1], w[2])
        for g in self.goals:
            tb.add_goal(g[0], g[1], g[2], g[3])
        for o in self.occs:
            tb.add_occ(o[0], o[1], o[2])
        return tb

    def normalize_vel(self):
        """Normalizes the ball's velocity to the default

        Args:
            TBD
        """
        v = self.ball[1]
        if v != (0, 0):
            vmag = sqrt(v[0] * v[0] + v[1] * v[1])
            vadj = self.dbv / vmag
            self.ball = (self.ball[0], (v[0] * vadj, v[1] * vadj),
                         self.ball[2], self.ball[3], self.ball[4])

    def check_consistency(self, maxsteps=50000, nochecktime=False):
        """Ensures this is a legal table with no overlaps

        Args:
            TBD
        """
        good = True

        ctb = self.make_table()

        if self.paddle:
            pbox = ctb.paddle.getbound()
        else:
            pbox = None

        if not self.ball:
            warnings.warn("Need to add a ball")
            good = False
        else:
            br = ctb.balls.getboundrect()
            for w in ctb.walls:
                if w.shapetype == SHAPE_RECT:
                    if br.colliderect(w.r):
                        warnings.warn("Ball overlaps with wall")
                        good = False
                else:
                    if br.colliderect(w.getBoundRect()):
                        if w.poly.point_query(ctb.balls.getpos()):
                            warnings.warn("Ball overlaps with abnormal wall")
                            good = False
                        else:
                            warnings.warn(
                                "POSSIBLE WARNING: Ball MAY overlap with" +
                                " abnormal wall")
                            good = -1
            if br.collidelist([g.r for g in ctb.goals]) != -1:
                warnings.warn("Ball overlaps with goal")
                good = False
            if pbox:
                if br.colliderect(pbox):
                    warnings.warn("Ball overlaps with paddle path")
                    good = False

        for g in ctb.goals:
            for w in ctb.walls:
                if w.shapetype == SHAPE_RECT:
                    if g.r.colliderect(w.r):
                        warnings.warn("Goal overlaps with wall")
                        good = False
                else:
                    if g.r.colliderect(w.getBoundRect()):
                        if (w.poly.segment_query(g.r.topleft, g.r.topright) or
                                w.poly.segment_query(g.r.topleft, g.r.bottomleft) or
                                w.poly.segment_query(g.r.topright, g.r.bottomright) or
                                w.poly.segment_query(g.r.bottomleft, g.r.bottomright)):
                            warnings.warn("Goal overlaps with abnormal wall")
                            good = False

            if pbox:
                if g.r.colliderect(pbox):
                    warnings.warn("Goal and paddle path intersect")
                    good = False

            if g.r.collidelist([o.r for o in ctb.occludes]) != -1:
                warnings.warn("Goal is at least partially occluded")
                good = False

        if len(ctb.goals) > 1:
            for i in range(1, len(ctb.goals)):
                g1 = ctb.goals[i - 1]
                g2 = ctb.goals[i]
                if g1.r.colliderect(g2.r):
                    warnings.warn("Two goals overlap")
                    good = False

        if pbox:
            for w in ctb.walls:
                if w.shapetype == SHAPE_RECT:
                    if pbox.colliderect(w.r):
                        warnings.warn("Paddle path intersects wall")
                        good = False
                else:
                    if pbox.colliderect(w.getBoundRect()):
                        ep = ctb.paddle.getendpts()
                        if w.poly.segment_query(ep[0], ep[1]):
                            warnings.warn(
                                "Paddle path intersects abnormal wall")
                            good = False

        if ctb.mostly_occ_all():
            good = False
            warnings.warn("Ball is mostly occluded at start")

        if not nochecktime:
            running = True
            stp = 0
            while running:
                stp += 1
                if stp > maxsteps:
                    print("Takes too long to end")
                    good = False
                    running = False
                e = ctb.step(TIMESTEP)
                if e:
                    running = False

            if ctb.mostly_occ_all():
                good = False
                warnings.warn("Ball is mostly occluded at end")

        return good

    def save_pickle(self, flnm=None, fldir=None, askoverwrite=True):
        if flnm is None:
            flnm = self.name + '.ptr'
        if fldir is not None:
            flnm = os.path.join(fldir, flnm)
        if os.path.exists(flnm) and askoverwrite:
            asking = True
            while asking:
                ans = input('File exists; overwrite? (y/n): ')
                if ans == 'n':
                    return None
                if ans == 'y':
                    asking = False

        pickle.dump(self, open(flnm, 'wb'))

    def save(self, flnm=None, fldir=None, askoverwrite=True, pretty=False):
        if flnm is None:
            flnm = self.name + '.json'
        if fldir is not None:
            flnm = os.path.join(fldir, flnm)
        if os.path.exists(flnm) and askoverwrite:
            asking = True
            while asking:
                ans = input('File exists; overwrite? (y/n): ')
                if ans == 'n':
                    return None
                if ans == 'y':
                    asking = False
        jdict = {'Name': self.name,
                 'Dims': self.dims,
                 'ClosedEnds': self.ce,
                 'BKColor': _unnumpy(self.bkc),
                 'Ball': _unnumpy(self.ball),
                 'Walls': _unnumpy(self.normwalls),
                 'AbnormWalls': _unnumpy(self.abnormwalls),
                 'Occluders': _unnumpy(self.occs),
                 'Paddle': _unnumpy(self.paddle),
                 'Goals': _unnumpy(self.goals)}

        if pretty:
            jfl = json.dumps(jdict, separators=(',', ': '),
                             sort_keys=True, indent=2,
                             cls=NumpyEncoder)
        else:
            jfl = json.dumps(jdict, cls=NumpyEncoder)
        ofl = open(flnm, 'w')
        ofl.write(jfl)
        ofl.close()


class PongTrial(SimpleTrial):

    def check_consistency(self, maxsteps=50000, nochecktime=False):
        good = True
        if len(self.goals) != 0:
            warnings.warn("No goals allowed on a PongTable")
            good = False
        if not super(PongTrial, self).check_consistency(maxsteps, nochecktime):
            good = False
        return good


class RedGreenTrial(SimpleTrial):

    def check_consistency(self, maxsteps=50000, nochecktime=False):
        good = True
        if len(self.goals) != 2:
            warnings.warn("Need two goals for a red/green trial")
            good = False

        if REDGOAL not in map(lambda x: x[2], self.goals): warnings.warn(
            "Need a REDGOAL return"); good = False
        if GREENGOAL not in map(lambda x: x[2], self.goals): warnings.warn(
            "Need a GREENGOAL return"); good = False
        if not super(RedGreenTrial, self).check_consistency(maxsteps, nochecktime):
            good = False
        return good

    def switch_red_green(self):
        self.goals = map(self.switch_goal_red_green, self.goals)

    @staticmethod
    def switch_goal_red_green(goal):
        if goal[2] == REDGOAL:
            return (goal[0], goal[1], GREENGOAL, GREEN)
        if goal[2] == GREENGOAL:
            return (goal[0], goal[1], REDGOAL, RED)


def load_json(j, trial_type=SimpleTrial):
    assert issubclass(trial_type, SimpleTrial), ("Loaded trial_type must "
                                                 "inherit from SimpleTrial")
    tr = trial_type(j['Name'], j['Dims'], j['ClosedEnds'],
                 background_cl=j['BKColor'])
    b = j['Ball']
    if b:
        tr.add_ball(b[0], b[1], b[2], b[3], b[4])
    for w in j['Walls']:
        tr.add_wall(w[0], w[1], w[2], w[3])
    for o in j['Occluders']:
        tr.add_occ(o[0], o[1], o[2])
    for g in j['Goals']:
        tr.add_goal(g[0], g[1], g[2], g[3])
    for a in j['AbnormWalls']:
        tr.add_abnorm_wall(a[0], a[1], a[2])
    p = j['Paddle']
    if p:
        tr.add_paddle(j[0], j[1], j[2], j[3], j[4], j[5], j[6], j[7], j[8])
    return tr

def load_trial(jsonfl, trialType=SimpleTrial):
    with open(jsonfl, 'rU') as jfl:
        j = json.load(jfl)
        tr = load_json(j, trialType)
    return tr

def load_pickle(flnm):
    return pickle.load(open(flnm, 'rb'))
