from collections import namedtuple
import numpy as np
import random


def gen_uniformly_events(beta, lam):
    n = 0
    d = np.exp(-beta * lam)
    p = d
    zeta = np.random.rand()
    while zeta > p:
        n += 1
        d *= beta * lam / n
        p += d
    tauk = [beta * random.random() for i in range(n)]
    tauk.sort()
    return (tauk, n)


class Conf:
    def __init__(self, beta, J, L):
        self.beta = beta
        self.J = J
        self.L = L
        self.lam = 1 / 4 * J
        self.kink = namedtuple("kink", ["ktau", "graph"])
        self.kinks = [[] for i in range(L)]
        self.b = namedtuple("b", ["kx", "ktau", "iktau", "LR"])
        # bs[bx][ibtau] = (kx, ktau, iktau, LR)
        self.bs = [[] for i in range(L)]
        # btilde = {(kx, iktau, LR): (bx, ibtau)}
        self.btilde = {}
        # c[x][itLR] = (bx, ibtau)
        self.cluster = [[] for i in range(self.L)]

    def root(self, x, t):
        r = self.cluster[x][t]
        while r != self.cluster[r[0]][r[1]]:
            r = self.cluster[r[0]][r[1]]
        return r

    def bond_cluster(self, x0, t0, x1, t1):
        r0 = self.root(x0, t0)
        r1 = self.root(x1, t1)
        if r0[0] < r1[0]:
            self.cluster[r1[0]][r1[1]] = r0
        elif r0[0] > r1[0]:
            self.cluster[r0[0]][r0[1]] = r1
        else:
            if r0[1] < r1[1]:
                self.cluster[r1[0]][r1[1]] = r0
            else:
                self.cluster[r0[0]][r0[1]] = r1

    def add_kinks(self, kx, ktau, graph):
        self.kinks[kx].append(self.kink(ktau, graph))

    def make_b(self):
        for kx in range(self.L):
            for iktau, kink in enumerate(self.kinks[kx]):
                self.bs[kx].append(self.b(kx, kink.ktau, iktau, 1))
            for itau, kink in enumerate(self.kinks[kx - 1]):
                self.bs[kx].append(self.b((kx - 1) % self.L, kink.ktau, itau, -1))
            self.bs[kx].sort(key=lambda b: b.ktau)

    def make_btilde(self):
        for bx in range(self.L):
            for ibtau in range(len(self.bs[bx])):
                self.btilde[
                    (
                        self.bs[bx][ibtau].kx,
                        self.bs[bx][ibtau].iktau,
                        self.bs[bx][ibtau].LR,
                    )
                ] = (bx, ibtau)

    def initial_cluster(self):
        for bx in range(self.L):
            for ibtau in range(len(self.bs[bx])):
                self.cluster[bx].append([bx, ibtau])

    def cluster_update(self):
        self.initial_cluster()
        print(self.cluster)
        for kx in range(self.L):
            for iktau in range(len(self.kinks[kx])):
                bx0, ibtau0 = self.btilde[(kx, iktau, 1)]
                bx1, ibtau1 = self.btilde[(kx, iktau, -1)]
                bx2 = bx0
                ibtau2 = ibtau0 - 1
                bx3 = bx1
                ibtau3 = ibtau1 - 1
                if self.kinks[kx][iktau].graph == "h":
                    self.bond_cluster(bx0, ibtau0, bx1, ibtau1)
                    self.bond_cluster(bx2, ibtau2, bx3, ibtau3)
                elif self.kinks[kx][iktau].graph == "d":
                    self.bond_cluster(bx0, ibtau0, bx3, ibtau3)
                    self.bond_cluster(bx1, ibtau1, bx2, ibtau2)
