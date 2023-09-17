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


class kinks:
    def __init__(self, beta, J, L):
        self.beta = beta
        self.J = J
        self.L = L
        lam = 1 / 4 * J
        self.points = []
        for _ in range(L):
            tauk, n = gen_uniformly_events(beta, lam)
            if n > 0:
                self.points.append(tauk)
            else:
                self.points.append([0])
        self.spins = [
            [random.choice([-1, 1]) for _ in range(len(self.points[i]))]
            for i in range(L)
        ]

    def get_tau(self, points_ix, itau):
        if itau == -1:
            return 0
        elif itau == len(points_ix):
            return self.beta
        else:
            return points_ix[itau]

    def get_wl(self):
        wl = []
        for ix in range(self.L):
            wl += [
                [
                    ix,
                    self.get_tau(self.points[ix], itau),
                    self.get_tau(self.points[ix], itau + 1),
                ]
                for itau in range(-1, len(self.points[ix]))
                if self.spins[ix][itau] == 1
            ]
        return np.array(wl)
