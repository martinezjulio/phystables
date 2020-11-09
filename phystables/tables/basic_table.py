"""The most basic table type

Allows for multiple balls, etc.

Examples:
    TBD

"""

from __future__ import division, print_function
import pymunk as pm
import random
import math
from ..constants import *
from ..objects import *
from ..utils import *
import numpy as np
from .rectangles import *
import subprocess
import os
import sys
import shutil
import shlex
import warnings
from weakref import ref


def _coll_func_ball_ball(arbiter, space, data):
    """Helper to deal with ball-ball collisions"""
    tableref = data['tableref']
    if tableref() is not None:
        tableref().coll_ball_ball(arbiter)


def _coll_func_ball_wall(arbiter, space, data):
    """Helper to deal with ball-wall collisions"""
    tableref = data['tableref']
    if tableref() is not None:
        tableref().coll_ball_wall(arbiter)


def _coll_func_ball_pad(arbiter, space, data):
    """Helper to deal with ball-paddle collisions"""
    tableref = data['tableref']
    if tableref() is not None:
        tableref().coll_ball_pad(arbiter)


def euclid_dist(p1, p2, maxdist=None):
    """Returns the euclidean distance or whether it is below a threshold

    Args:
        p1 ([float, float]): Point 1
        p2 ([float, float]): Point 2
        maxdist (float): The maximum distance between points

    Returns:
        The euclidean distance if maxdist is not set, boolean of whether the
        distance is below that max if it is
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    if maxdist is None:
        return math.sqrt(dx * dx + dy * dy)
    else:
        return (dx * dx + dy * dy) <= maxdist * maxdist


def ball_rect_collision(ball, rect):
    brect = ball.getboundrect()
    if rect.colliderect(brect):
        if rect.contains(brect):
            return True
        bcent = ball.getpos()
        rad = ball.getrad()
        if brect.bottom > rect.top or brect.top < rect.bottom:
            if bcent[0] > rect.left and bcent[0] < rect.right:
                return True
        if brect.right > rect.left or brect.left < rect.right:
            if bcent[1] > rect.top and bcent[1] < rect.bottom:
                return True

        return any(map(lambda pt: euclid_dist(pt, bcent, rad),
                       [rect.topleft, rect.topright,
                        rect.bottomleft, rect.bottomright]))
    else:
        return False



class BasicTable(object):
    """The most basic phystables table instantiation

    More description goes here
    """

    def __init__(self, dims, closed_ends=[LEFT, RIGHT, BOTTOM, TOP],
                 def_ball_rad=20, def_pad_len=100, active=True):
        """The BasicTable initializer

        Args:
            TBD
        """
        # Default characteristics
        self.dim = dims
        self.dballrad = def_ball_rad
        self.dpadlen = def_pad_len
        self.act = active

        # Make the pymunk space (& sink output)
        _stderr = sys.stderr
        _stdout = sys.stdout
        nullout = open(os.devnull, 'wb')
        sys.stderr = sys.stdout = nullout
        self.sp = pm.Space(10)
        sys.stderr = _stderr
        sys.stdout = _stdout
        self.sp.gravity = pm.Vec2d(0., 0.)
        stb = self.sp.static_body

        bbch = self.sp.add_collision_handler(COLLTYPE_BALL, COLLTYPE_BALL)
        bbch.data['tableref'] = ref(self)
        bbch.separate = _coll_func_ball_ball

        bwch = self.sp.add_collision_handler(COLLTYPE_BALL, COLLTYPE_WALL)
        bwch.data['tableref'] = ref(self)
        bwch.separate = _coll_func_ball_wall

        bpch = self.sp.add_collision_handler(COLLTYPE_BALL, COLLTYPE_PAD)
        bpch.data['tableref'] = ref(self)
        bpch.separate = _coll_func_ball_pad

        # Empty color info that gets replaced if pygame is there
        self.bk_c = None
        self.dballc = None
        self.dwallc = None
        self.doccc = None
        self.dpadc = None
        self.stored_soffset = None
        self.soff = None
        self.surface = None

        self.balls = []
        self.walls = []
        self.occludes = []
        self.goals = []
        self.goalrettypes = [TIMEUP]
        self.paddle = None
        self.padhit = False

        self.stored_closed_ends = closed_ends

        self.top = self.bottom = self.right = self.left = None

        def make_bounding_box_shape(left, top, right, bottom):
            verts = [(left, top), (left, bottom), (right, bottom), (right, top)]
            s = pm.Poly(stb, verts)
            s.elasticity = 1.
            s.collision_type = COLLTYPE_WALL
            return s
        for ce in closed_ends:
            if ce == TOP:
                self.top = make_bounding_box_shape(-1, -10, self.dim[0] + 1, 0)
                self.sp.add(self.top)
            elif ce == BOTTOM:
                self.bottom = make_bounding_box_shape(-1,
                                                      self.dim[1],
                                                      self.dim[0] + 1,
                                                      self.dim[1] + 10)
                self.sp.add(self.bottom)
            elif ce == RIGHT:
                self.right = make_bounding_box_shape(-10, -1, 0, self.dim[1])
                self.sp.add(self.right)
            elif ce == LEFT:
                self.left = make_bounding_box_shape(self.dim[0], -1,
                                                    self.dim[0] + 10,
                                                    self.dim[1] + 1)
                self.sp.add(self.left)
            else:
                print ("Warning: Inappropriate closed_ends:", ce)

        # Other characteristics
        self.tm = 0.
        self.basicts = TIMESTEP

    def __del__(self):
        """Destructor for cleaning pymunk"""
        # Clean up the pymunk space
        self.sp.remove(self.sp.bodies)
        self.sp.remove(self.sp.shapes)
        del self.sp

    def set_timestep(self, ts):
        self.basicts = ts

    def coll_ball_ball(self, arbiter):
        map(self.add_bounce, arbiter.shapes)
        self.on_ballhit([b for b in self.balls if b.circle in arbiter.shapes])

    def coll_ball_wall(self, arbiter):
        map(self.add_bounce, arbiter.shapes)
        if len(arbiter.shapes) > 2:
            print ("Shouldn't have multi-collision... may be errors")
        ss = [self.find_wall_by_shape(s) for s in arbiter.shapes]
        wl = [w for w in ss if w is not None][0]
        self.on_wallhit([b for b in self.balls if b.circle in arbiter.shapes][0], wl)

    def coll_ball_pad(self, arbiter):
        map(self.add_bounce, arbiter.shapes)
        if len(arbiter.shapes) > 2:
            print ("Shouldn't have multi-collision... may be errors")
        self.padhit = True
        self.on_paddlehit([b for b in self.balls if b.circle in arbiter.shapes][0], self.paddle)

    def on_step(self): pass

    def on_addball(self, ball): pass

    def on_ballhit(self, balllist): pass

    def on_wallhit(self, ball, wall): pass

    def on_paddlehit(self, ball, paddle): pass

    def on_goalhit(self, ball, goal): pass

    def activate(self): self.act = True

    def deactivate(self): self.act = False

    def mostly_occ(self, ball):
        bpos = ball.getpos()
        for o in self.occludes:
            if o.r.collidepoint(bpos):
                return True
        return False

    def mostly_occ_all(self):
        return [self.mostly_occ(b) for b in self.balls]

    def fully_occ(self, ball):
        brect = ball.getboundrect()
        orects = [o.r.inflate(1, 1) for o in self.occludes]
        testos = []
        for o in orects:
            if o.contains(brect):
                return True
            if o.colliderect(brect):
                testos.append(o)
        if len(break_rect(brect, testos)) == 0:
            return True
        return False

    def fully_occ_all(self):
        return [self.fully_occ(b) for b in self.balls]

    def add_ball(self, initpos, initvel=(0., 0.), rad=None, color=None,
                 elast=1., pmsp=None, layers=None):
        if pmsp is None:
            pmsp = self.sp
        if rad is None:
            rad = self.dballrad
        if color is None:
            color = self.dballc
        newball = Ball(initpos, initvel, rad, color, elast, pmsp, layers)
        self.sp.add(newball.body, newball.circle)
        self.on_addball(newball)
        self.balls.append(newball)
        return newball

    def add_wall(self, upperleft, lowerright, color=None, elast=1., pmsp=None):
        if pmsp is None:
            pmsp = self.sp
        if color is None:
            color = self.dwallc
        newwall = Wall(upperleft, lowerright, color, elast, self.sp.static_body, pmsp)
        self.sp.add(newwall.poly)
        self.walls.append(newwall)
        return newwall

    def add_abnorm_wall(self, vertexlist, color=None, elast=1., pmsp=None):
        if pmsp is None:
            pmsp = self.sp
        if not check_counterclockwise(vertexlist):
            print('In addAbnormWall, vertices must be counterclockwise and convex, no wall added:',
                  vertexlist)
            return None
        if color is None:
            color = self.dwallc
        newwall = AbnormWall(vertexlist, color, elast, self.sp.static_body, pmsp)
        self.sp.add(newwall.poly)
        self.walls.append(newwall)
        return newwall

    def add_occ(self, upperleft, lowerright, color=None):
        if color is None:
            color = self.doccc
        newocc = Occlusion(upperleft, lowerright, color)
        self.occludes.append(newocc)
        return newocc

    def add_goal(self, upperleft, lowerright, onreturn, color=None):
        try:
            dict([(onreturn, 0)])
        except RuntimeError:
            raise TypeError("'onreturn' argument is not hashable: " +
                            str(onreturn))
        newgoal = Goal(upperleft, lowerright, color, onreturn)
        self.goals.append(newgoal)
        if onreturn not in self.goalrettypes:
            self.goalrettypes.append(onreturn)
        return newgoal

    def add_paddle(self, p1, p2, padlen=None, padwid=3, hitret=None,
                   active=True, acol=None, iacol=None, pthcol=None, elast=1.,
                   suppressoverwrite=False, pmsp=None):
        if pmsp is None:
            pmsp = self.sp
        if active:
            sta = self.sp
        else:
            sta = None
        if p1 == p2:
            print("Paddle endpoints must not overlap:", p1, p2)
            return None
        if p1[0] != p2[0] and p1[1] != p2[1]:
            print("Paddle must be horizontal or vertical", p1, p2)
            return None
        if padlen is None:
            padlen = self.dpadlen
        if self.paddle is not None and not suppressoverwrite:
            print("Warning! Overwriting old paddle")
        self.paddle = Paddle(p1, p2, padlen, acol, iacol, pthcol, padwid,
                             hitret, sta, elast, self.sp.static_body, pmsp)
        return self.paddle

    def activate_paddle(self):
        if not self.paddle:
            print("Can't activate a missing paddle!")
            return None
        self.paddle.activate(self.sp, self.getRelativeMousePos())

    def deactivate_paddle(self):
        if not self.paddle:
            print("Can't deactivate a missing paddle!")
            return None
        self.paddle.deactivate(self.sp)

    def toggle_paddle(self):
        if not self.paddle:
            print("Can't toggle a missing paddle!")
            return None
        if self.paddle.act:
            self.paddle.deactivate(self.sp)
        else:
            self.paddle.activate(self.sp, self.getRelativeMousePos())

    # Default: does any ball overlap with any of the goals? Hit the paddle?
    def check_end(self):
        rets = []
        if self.padhit:
            return self.paddle.ret
        for g in self.goals:
            for b in self.balls:
                if ball_rect_collision(b, g.r):
                    self.on_goalhit(b, g)
                    if g.ret:
                        rets.append(g.ret)
        if len(rets) > 0:
            return rets
        return None

    def add_bounce(self, shapeobj):
        for b in self.balls:
            if b.circle == shapeobj:
                b.bounces += 1

    def find_wall_by_shape(self, shape):
        wls = [w for w in self.walls if w.poly == shape]
        if len(wls) == 1:
            return wls[0]
        elif self.top == shape:
            return TOP
        elif self.bottom == shape:
            return BOTTOM
        elif self.left == shape:
            return LEFT
        elif self.right == shape:
            return RIGHT
        else:
            return None

    def step(self, t=1 / 50., maxtime=None):
        substeps = t / self.basicts
        # Check for offsets in substeps, tolerant to rounding errors
        isubs = int(np.floor(substeps + 1e-7))
        if abs(substeps - isubs) > 1e-6:
            print("Warning: steps not evenly divisible - off by",
                  (substeps - isubs))
        if self.act:
            for i in range(int(substeps)):
                self.on_step()
                self.sp.step(self.basicts)
                self.tm += self.basicts
                e = self.check_end()
                if e is not None:
                    return e
                if maxtime and self.tm > maxtime:
                    return TIMEUP
            return e
        else:
            return None
