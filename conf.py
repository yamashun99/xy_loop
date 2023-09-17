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


class Kink:
    def __init__(self, beta, J, L):
        self.beta = beta
        self.J = J
        self.L = L
        lam = 1 / 4 * J


class Wolrdline:
    def __init__(self, beta, J, L):
        self.beta = beta
        self.J = J
        self.L = L
        lam = 1 / 4 * J
        self.kinks = [[] for i in range(L)]
        self.kink = namedtuple("kink", ["tau", "spin"])
        self.initial_spin = [-1 for i in range(L)]

    def add_kinks(self, x, tau, spin):
        self.kinks[x].append(self.kink(tau, spin))

    def initial_spin_update(self, spin):
        for x in range(self.L):
            if len(self.kinks[x]) != 0 and len(self.kinks[x - 1]) == 0:
                spin[x] = self.kinks[x][0].spin[0]
            elif len(self.kinks[x]) == 0 and len(self.kinks[x]) != 0:
                spin[x] = self.kinks[x][0].spin[0]
            elif len(self.kinks[x]) != 0 and len(self.kinks[x]) != 0:
                if self.kinks[x][0].tau < self.kinks[x - 1][0].tau:
                    spin[x] = self.kinks[x][0].spin[0]
                else:
                    spin[x] = self.kinks[x - 1][0].spin[-1]

    def get_up(self, x):
        tau_spin = namedtuple("tau_spin", ["tau", "spin"])
        tau_right = []
        for i in range(len(self.kinks[x])):
            tau_right.append(tau_spin(self.kinks[x][i].tau, self.kinks[x][i].spin[0]))
        tau_left = []
        for i in range(len(self.kinks[x - 1])):
            tau_left.append(
                tau_spin(self.kinks[x - 1][i].tau, self.kinks[x - 1][i].spin[-1])
            )
        tau = tau_left + tau_right
        tau.sort()
        up = []
        for i in range(len(tau)):
            if tau[i - 1].spin == 1:
                up.append([tau[i - 1].tau, tau[i].tau, x])
        if up[0][0] > up[0][1]:
            up.append([0, up[0][1], x])
            up.append([up[0][0], self.beta, x])
            up.pop(0)
        return up

    def get_ups(
        self,
    ):
        ups = []
        for x in range(self.L):
            if len(self.kinks[x]) == len(self.kinks[x - 1]) == 0:
                if self.initial_spin[x] == 1:
                    ups += [[0, self.beta, x]]
            else:
                ups += self.get_up(x)
        ups = np.array(ups)
        return ups
