"""A SimpleTable that includes uncertainty in simulation

For details of parameters, see Smith & Vul (2013)

Examples:

    TBD

"""

from __future__ import division, print_function
import sys
import os
from .simple_table import *
from .basic_table import *
from ..objects import *
from ..utils import *
import random
import numpy as np
import pymunk as pm


def vel_angle(vx, vy):
    ang = np.arctan2(vy, vx) % (np.pi * 2)
    mag = np.sqrt(vx * vx + vy * vy)
    return (ang, mag)


class NoisyTable(SimpleTable):

    def __init__(self, dims, kapv=KAPV_DEF, kapb=KAPB_DEF, kapm=KAPM_DEF,
                 perr=PERR_DEF, constrained_bounce=False,
                 constrained_move=False, *args, **kwds):

        self.kapv = kapv
        self.kapb = kapb
        self.kapm = kapm
        self.perr = perr
        self.cons_bounce = constrained_bounce
        self.cons_move = constrained_move
        super().__init__(dims, *args, **kwds)

    def __del__(self):
        super().__del__()

    def jitter_ball(self, ball, kappa=None, posjitter=None):
        if posjitter:
            initpos = ball.getpos()
            rad = ball.getrad()
            xdim, ydim = self.dim
            setting = True
            while setting:
                px = random.normalvariate(initpos[0], posjitter)
                py = random.normalvariate(initpos[1], posjitter)
                ball.setpos((px, py))
                setting = False
                # Check that the ball isn't outside the screen
                if not (px > rad and py > rad and px < (xdim - rad) and py < (ydim - rad)):
                    setting = True

                # Check that the ball isn't stuck in walls or on a goal
                brect = ball.getboundrect()
                for w in self.walls:
                    if brect.colliderect(w.get_bound_rect()):
                        setting = True
                for g in self.goals:
                    if brect.colliderect(g.r):
                        setting = True

        if kappa:
            v = ball.getvel()
            vang, vmag = vel_angle(v[0], v[1])
            newang = np.random.vonmises(vang, kappa) % (2 * np.pi)
            if self.cons_move:
                if 0 < vang < np.pi / 2.:
                    bounds = (0, np.pi / 2.)
                elif np.pi / 2. < vang < np.pi:
                    bounds = (np.pi / 2., np.pi)
                elif np.pi < vang < np.pi * 1.5:
                    bounds = (np.pi, np.pi * 1.5)
                elif np.pi * 1.5 < vang < np.pi * 2.:
                    bounds = (np.pi * 1.5, np.pi * 2.)
                else:
                    raise RuntimeError("Angle outside of 0, 2pi")
                while not (bounds[0] < newang < bounds[1]):
                    newang = np.random.vonmises(vang, kappa) % (2 * np.pi)
            ball.setvel((vmag * np.cos(newang), vmag * np.sin(newang)))

    # Special case of wall collision -- doesn't allow ball to reverse course
    def wall_collide(self, ball, wall, kappa=None):
        if type(wall) == AbnormWall:
            print ("Cannot do special collision with abnormal walls (yet) - doing normal jitter")
            self.jitter_ball(ball, kappa)
        elif kappa:
            v = ball.getvel()
            vang, vmag = vel_angle(v[0], v[1])
            # Find the bounding angles
            if 0 < vang < np.pi / 2.:
                bounds = (0, np.pi / 2.)
            elif np.pi / 2. < vang < np.pi:
                bounds = (np.pi / 2., np.pi)
            elif np.pi < vang < np.pi * 1.5:
                bounds = (np.pi, np.pi * 1.5)
            elif np.pi * 1.5 < vang < np.pi * 2.:
                bounds = (np.pi * 1.5, np.pi * 2.)
            else:
                raise RuntimeError("Angle outside of 0, 2pi")
            newang = np.random.vonmises(vang, kappa) % (2 * np.pi)
            while not (bounds[0] < newang < bounds[1]):
                newang = np.random.vonmises(vang, kappa) % (2 * np.pi)
            ball.setvel((vmag * np.cos(newang), vmag * np.sin(newang)))

    def on_wallhit(self, ball, wall):
        if self.cons_bounce:
            self.wall_collide(ball, wall, self.kapb)
        else:
            self.jitter_ball(ball, self.kapb)

    def on_addball(self, ball):
        self.jitter_ball(ball, self.kapv, self.perr)

    def on_step(self):
        if self.balls is not None:
            self.jitter_ball(self.balls, self.kapm)


class NoisyMultiTable(BasicTable):

    def __init__(self, dims, kapv=KAPV_DEF, kapb=KAPB_DEF, kapm=KAPM_DEF,
                 perr=PERR_DEF, constrained_bounce=False,
                 constrained_move=False, *args, **kwds):

        self.kapv = kapv
        self.kapb = kapb
        self.kapm = kapm
        self.perr = perr
        self.cons_bounce = constrained_bounce
        self.cons_move = constrained_move
        super().__init__(dims, *args, **kwds)

    def __del__(self):
        super().__del__()

    def jitter_ball(self, ball, kappa=None, posjitter=None):
        if posjitter:
            initpos = ball.getpos()
            rad = ball.getrad()
            xdim, ydim = self.dim
            setting = True
            while setting:
                px = random.normalvariate(initpos[0], posjitter)
                py = random.normalvariate(initpos[1], posjitter)
                ball.setpos((px, py))
                setting = False
                # Check that the ball isn't outside the screen
                if not (px > rad and py > rad and px < (xdim - rad) and py < (ydim - rad)):
                    setting = True

                # Check that the ball isn't stuck in walls or on a goal
                brect = ball.getboundrect()
                for w in self.walls:
                    if brect.colliderect(w.get_bound_rect()):
                        setting = True

                for g in self.goals:
                    if brect.colliderect(g.r):
                        setting = True

        if kappa:
            v = ball.getvel()
            vang, vmag = vel_angle(v[0], v[1])
            newang = np.random.vonmises(vang, kappa)
            ball.setvel((vmag * np.cos(newang), vmag * np.sin(newang)))

    def on_wallhit(self, ball, wall):
        if self.cons_bounce:
            self.wall_collide(ball, wall, self.kapb)
        else:
            self.jitter_ball(ball, self.kapb)

    def on_ballhit(self, ballist):
        for b in ballist:
            self.jitter_ball(b, self.kapb)

    def on_addball(self, ball):
        self.jitter_ball(ball, self.kapv, self.perr)

    def on_step(self):
        if self.balls is not None:
            for b in self.balls:
                self.jitter_ball(b, self.kapm)


def make_noisy(table, kapv=KAPV_DEF, kapb=KAPB_DEF, kapm=KAPM_DEF,
               perr=PERR_DEF, paddlereturn=SUCCESS, straddlepaddle=True,
               constrained_bounce=False, constrained_move=False):

    sttype = type(table) == SimpleTable

    try:
        import pygame
        if sttype:
            ntab = NoisyTable(table.dim, kapv, kapb, kapm, perr, constrained_bounce, constrained_move,
                              table.stored_closed_ends, table.bk_c, table.dballrad, table.dballc, table.dpadlen,
                              table.dwallc, table.doccc, table.dpadc, table.act, table.stored_soffset)
        else:
            ntab = NoisyMultiTable(table.dim, kapv, kapb, kapm, perr, constrained_bounce, constrained_move,
                                   table.stored_closed_ends, table.bk_c, table.dballrad, table.dballc, table.dpadlen,
                                   table.dwallc, table.doccc, table.dpadc, table.act, table.stored_soffset)
    except:
        if sttype:
            ntab = NoisyTable(table.dim, kapv, kapb, kapm, perr, constrained_bounce, constrained_move,
                              table.stored_closed_ends, table.dballrad, table.dpadlen, table.act)
        else:
            ntab = NoisyMultiTable(table.dim, kapv, kapb, kapm, perr, constrained_bounce, constrained_move,
                                   table.stored_closed_ends, table.dballrad, table.dpadlen, table.act)
    ntab.set_timestep(table.basicts)
    for w in table.walls:
        if isinstance(w, AbnormWall):
            ntab.add_abnorm_wall(safe_winding_vertices(w.poly.get_vertices()),
                                 w.col, w.poly.elasticity)
        elif isinstance(w, Wall):
            ntab.add_wall(w.r.topleft, w.r.bottomright, w.col, w.poly.elasticity)

    for o in table.occludes:
        ntab.add_occ(o.r.topleft, o.r.bottomright, o.col)
    for g in table.goals:
        ntab.add_goal(g.r.topleft, g.r.bottomright, g.ret, g.col)
    # Turn paddle into a special goal that returns paddlereturn (SUCCESS by default)
    if table.paddle and paddlereturn:
        if straddlepaddle:
            op = table.paddle.otherpos
            if table.paddle.dir == HORIZONTAL:
                ul = (0, op - table.paddle.wid)
                lr = (table.dim[0], op + table.paddle.wid)
            else:
                ul = (op - table.paddle.wid, 0)
                lr = (op + table.paddle.wid, table.dim[1])
        else:
            e1, e2 = table.paddle.getendpts()
            if table.paddle.dir == HORIZONTAL:
                ul = (e1[0], e1[1] - table.paddle.wid)
                lr = (e2[0], e2[1] + table.paddle.wid)
            else:
                ul = (e1[0] - table.paddle.wid, e1[1])
                lr = (e2[0] + table.paddle.wid, e2[1])
        ntab.add_goal(ul, lr, paddlereturn, LIGHTGREY)

    if sttype:
        if table.balls:
            ntab.add_ball(table.balls.getpos(), table.balls.getvel(),
                         table.balls.getrad(), color=table.balls.col)
    else:
        for b in table.balls:
            ntab.add_ball(b.getpos(), b.getvel(), b.getrad(), color=b.col)

    ntab.tm = table.tm

    return ntab
