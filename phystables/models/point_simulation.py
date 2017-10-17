from __future__ import division
from ..tables import NoisyTable, make_noisy
from ..constants import *
from OptimTools import async_map
from multiprocessing import cpu_count
import numpy as np


class PointSimulation(object):

    def __init__(self, table, kapv=KAPV_DEF, kapb=KAPB_DEF, kapm=KAPM_DEF,
                 perr=PERR_DEF, ensure_end=False, nsims=200, maxtime=50.,
                 cpus=cpu_count(), timeres=0.05):
        self.tab = table
        self.kapv = kapv
        self.kapb = kapb
        # Correction for the fact that we're simulating fewer steps and thus
        # jitter must be noisier (by approx sqrt of number of steps)
        self.kapm = kapm / np.sqrt(timeres / 0.001)
        self.perr = perr
        self.maxtime = maxtime
        self.nsims = nsims
        self.ts = timeres

        self.outcomes = None
        self.endpts = None
        self.bounces = None
        self.run = False
        self.enend = ensure_end

        self.ucpus = cpus
        self.badsims = 0

    def single_sim(self, i):
        n = make_noisy(self.tab, self.kapv, self.kapb, self.kapm, self.perr)
        n.set_timestep(self.ts)
        r = n.simulate(self.maxtime)
        p = n.balls.getpos()
        nb = n.balls.bounces
        rp = (p[0], p[1])
        if self.enend:
            if r == TIMEUP:
                self.badsims += 1
                return(self.singleSim(i))
            if rp[0] < 0 or rp[0] > self.tab.dim[0] or rp[1] < 0 or rp[1] > self.tab.dim[1]:
                self.badsims += 1
                return(self.singleSim(i))
        return [r, rp, nb, n.tm]

    def run_simulation(self):

        if self.ucpus == 1:
            ret = map(self.singleSim, range(self.nsims))
        else:
            ret = async_map(self.singleSim, range(self.nsims), self.ucpus)

        self.outcomes = [r[0] for r in ret]
        self.endpts = [r[1] for r in ret]
        self.bounces = [r[2] for r in ret]
        self.tsims = [r[3] for r in ret]
        self.run = True

        return [self.outcomes, self.endpts, self.bounces, self.tsims]

    def get_outcomes(self):
        if not self.run:
            raise RuntimeError("Cannot get simulation outcome without "
                               "running simulations first")
        retdict = dict([(r, 0) for r in self.tab.goalrettypes])
        for o in self.outcomes:
            retdict[o] += 1

        return retdict

    def get_endpoints(self, xonly=False, yonly=False):
        if not self.run:
            raise RuntimeError("Cannot get simulation endpoints without "
                               "running simulations first")
        if xonly and not yonly:
            return [p[0] for p in self.endpts]
        if yonly and not xonly:
            return [p[1] for p in self.endpts]
        return self.endpts

    def get_bounces(self):
        if not self.run:
            raise RuntimeError("Cannot get simulation bounces without "
                               "running simulations first")
        return self.bounces

    def get_times(self):
        if not self.run:
            raise RuntimeError("Cannot get simulation times without "
                               "running simulations first")
        return self.tsims

    def replace_outcomes(self, badoutcomes=[TIMEUP, OUTOFBOUNDS], printout=False):
        # Find the indices of all places where the outcomes are bad
        idxs = [x[0] for x in enumerate(self.outcomes) if badoutcomes.count(x[1]) > 0]
        if len(idxs) == 0:
            return None

        if printout:
            print "Resimulating", len(idxs), "times"

        ret = async_map(self.single_sim, range(len(idxs)), self.ucpus)
        for i in range(len(idxs)):
            idx = idxs[i]
            self.outcomes[idx] = ret[i][0]
            self.endpts[idx] = ret[i][1]
            self.bounces[idx] = ret[i][2]
            self.tsims[idx] = ret[i][3]
        self.replace_outcomes(badoutcomes, printout)
