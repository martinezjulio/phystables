from __future__ import division
from phystables import *
from phystables.constants import *
import pygame as pg
from pygame.constants import *
import pymunk as pm
import sys, os, random, time

if __name__ == '__main__':

    args = sys.argv
    if len(args) != 2:
        print ('test.py takes one argument; valid tests are BASIC, NOISY, GRAVITY, SPEED, PATHFILTER, LIMTIME')
        sys.exit(0)

    if not args[1] in ['BASIC','NOISY','GRAVITY','SPEED','PATHFILTER', 'LIMTIME','NOISYBOUNCE']:
        print ('test.py takes one argument; valid tests are BASIC, NOISY, GRAVITY, SPEED, PATHFILTER, LIMTIME, NOISYBOUNCE')
        sys.exit(0)


    pg.init()


    if args[1] == 'BASIC':
        screen = pg.display.set_mode((1000,600))
        clock = pg.time.Clock()
        running = True
        table = BasicTable((800,400),soffset = (100,100))
        table.add_ball((100,100),(300,-300))
        table.add_wall((600,100),(700,300))
        table.add_occ((100,50),(600,150))
        table.add_goal((0,300),(100,400),SUCCESS, RED)
        print (table.demonstrate())

    if args[1] == 'LIMTIME':
        screen = pg.display.set_mode((1000,600))
        clock = pg.time.Clock()
        running = True
        table = BasicTable((800,400),soffset = (100,100))
        table.add_ball((100,100),(300,-300))
        table.add_wall((600,100),(700,300))
        table.add_occ((100,50),(600,150))
        print (table.demonstrate(maxtime = 5))

    elif args[1] == 'SPEED':
        screen = pg.display.set_mode((1000,600))
        clock = pg.time.Clock()
        running = True
        table = BasicTable((800,400),soffset = (100,100))
        table.add_ball((100,100),(300,-300))
        table.add_wall((600,100),(700,300))
        table.add_occ((100,50),(600,150))
        table.add_goal((0,300),(100,400),SUCCESS, RED)
        print (table.demonstrate(timesteps = 1/200.))
    elif args[1] == 'NOISY':
        screen = pg.display.set_mode((1000,600))
        clock = pg.time.Clock()
        running = True
        table = SimpleTable((800,400))
        table.add_ball((100,100),(300,-300))
        table.add_wall((600,100),(700,300))
        table.add_occ((100,50),(600,150))
        table.add_abnorm_wall([(300,300),(300,400),(400,300),(400,200),(350,200)])
        table.add_goal((700,300),(800,400),SUCCESS,RED)
        table.add_goal((0,300),(100,400),SUCCESS, GREEN)
        while True:
            noise = make_noisy(table)
            noise.set_timestep(1/100.)
            noise.demonstrate()
            #pg.display.flip()

            running = True
            while running:
                for e in pg.event.get():
                    if e.type == QUIT: pg.quit(); sys.exit(0)
                    elif e.type == KEYDOWN and e.key == K_ESCAPE: pg.quit(); sys.exit(0)
                    elif e.type == MOUSEBUTTONDOWN: running = False


    elif args[1] == "NOISYBOUNCE":
        sc = pg.display.set_mode((600,400))
        tr = SimpleTrial('test', (600, 400))
        tr.add_wall((100,100), (600,400))
        tr.add_ball((50,300),(50,-280),10)
        tr.add_goal((550,0),(600,100),REDGOAL,RED)
        tr.add_wall((100,0),(200,20))
        tab = tr.make_table()
        ntab = make_noisy(tab, 10., 30., None, None, constrained_bounce=True, constrained_move=True)
        ntab.demonstrate()

    pg.quit()
    sys.exit(0)
