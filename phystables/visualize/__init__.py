from warnings import warn
import time


__all__ = ['screen_pause', 'WHITE', 'BLACK', 'BLUE', 'RED', 'GREEN', 'GREY', 'LIGHTGREY', 'YELLOW', 'GOLD', 'PURPLE',
           'Ball', 'Wall', 'Occlusion', 'AbnormWall', 'Goal', 'Paddle', 'ptRect', 'BasicTable', 'SimpleTable', "pgFig"]

try:
    import pygame as pg
    from pygame.locals import *

    def quitevent(quit_k=[K_LSHIFT, K_ESCAPE]):
        keys = pg.key.get_pressed()
        for k in quit_k:
            if keys[k] == 0:
                return False
        return True

    def screen_pause(t=0.5, keymove=True, clickmove=True):
        time.sleep(t)
        for e in pg.event.get():
            pass
        while True:
            for e in pg.event.get():
                if e.type == QUIT:
                    return True
                elif e.type == KEYDOWN:
                    if keymove and (e.key != K_ESCAPE and e.key != K_LSHIFT):
                        return False
                    if quitevent():
                        return True
                elif e.type == MOUSEBUTTONDOWN and clickmove:
                    return False

    from .vizobjects import Ball, Wall, Occlusion, AbnormWall, Goal, Paddle, ptRect
    from .viztables import BasicTable, SimpleTable
except ImportError:
    raise ImportError("pygame is required to import any visualizations")

try:
    from matpltPygame import pgFig
except ImportError:
    warn("Need matplotlib to import pgFig for graph plotting", ImportWarning)

    def pgFig(*kwds, **args): raise Exception('Need matplotlib for pgFig!s')

# Set color names
WHITE = pg.Color('White')
BLACK = pg.Color('Black')
BLUE = pg.Color('Blue')
RED = pg.Color('Red')
GREEN = pg.Color('Green')
GREY = pg.Color('Grey')
LIGHTGREY = pg.Color('lightgrey')
YELLOW = pg.Color('Yellow')
GOLD = pg.Color('Gold')
PURPLE = pg.Color('Purple')
