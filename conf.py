from collections import namedtuple
from dataclasses import dataclass
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


@dataclass
class Kink:
    ktau: float
    graph: str


@dataclass
class Spin:
    tau: float
    spin: int


class Conf:
    def __init__(self, beta, J, L):
        self.beta = beta
        self.J = J
        self.L = L
        self.lam = 1 / 4 * J
        self.kinks = [[] for _ in range(L)]
        self.b = namedtuple("b", ["kx", "ktau", "iktau", "LR"])
        # bs[bx][ibtau] = (kx, ktau, iktau, LR)
        self.bs = [[] for i in range(L)]
        # btilde = {(kx, iktau, LR): (bx, ibtau)}
        self.btilde = {}
        # c[bx][ibtau] = (bx, ibtau)
        self.cluster = [[] for _ in range(self.L)]
        # spin[bx][ibtau] = (bx, ibtau)
        self.spins = [[Spin(-1, -1)] for _ in range(self.L)]

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

    def add_kinks(self, kinks, kx, ktau, graph):
        kinks[kx].append(Kink(ktau, graph))

    def make_b(self):
        """
        bar座標からkink座標への変換のためのリストを作成
        ibar, itau => (kx, ktau, iktau, LR)
        """
        self.bs = [[] for i in range(self.L)]
        for kx in range(self.L):
            for iktau, kink in enumerate(self.kinks[kx]):
                self.bs[kx].append(self.b(kx, kink.ktau, iktau, "L"))
            for itau, kink in enumerate(self.kinks[kx - 1]):
                self.bs[kx].append(self.b((kx - 1) % self.L, kink.ktau, itau, "R"))
            self.bs[kx].sort(key=lambda b: b.ktau)

    def make_btilde(self):
        """
        kink座標からbar座標への変換のための辞書を作成
        (kx, iktau, LR) => (bx, ibtau)
        """
        self.btilde = {}
        for bx in range(self.L):
            for ibtau in range(len(self.bs[bx])):
                self.btilde[
                    (
                        self.bs[bx][ibtau].kx,
                        self.bs[bx][ibtau].iktau,
                        self.bs[bx][ibtau].LR,
                    )
                ] = (bx, ibtau)

    def _initial_cluster(self):
        self.cluster = [[] for i in range(self.L)]
        for bx in range(self.L):
            for ibtau in range(len(self.bs[bx])):
                self.cluster[bx].append([bx, ibtau])

    def cluster_update(self):
        self._initial_cluster()
        for kx in range(self.L):
            for iktau in range(len(self.kinks[kx])):
                bx0, ibtau0 = self.btilde[(kx, iktau, "L")]
                bx1, ibtau1 = self.btilde[(kx, iktau, "R")]
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

    def insert_spin(self, kinks):
        last_spin = [self.spins[bx][-1].spin for bx in range(self.L)]
        for kx in range(self.L):
            for iktau in range(len(kinks[kx])):
                # bx0, ibtau0 = self.btilde[(kx, iktau, "L")]
                # bx1, ibtau1 = self.btilde[(kx, iktau, "R")]
                bx0 = kx
                bx1 = (kx + 1) % self.L
                tau = kinks[kx][iktau].ktau
                self.spins[bx0].append(Spin(tau, None))
                self.spins[bx1].append(Spin(tau, None))
        for bx in range(self.L):
            self.spins[bx].sort(key=lambda s: s.tau)
        for bx in range(self.L):
            # self.spins[bx].sort(key=lambda s: s.tau)
            for ibtau in range(len(self.spins[bx])):
                if self.spins[bx][ibtau].spin == None:
                    if ibtau == 0:
                        self.spins[bx][ibtau].spin = last_spin[bx]
                    else:
                        self.spins[bx][ibtau].spin = self.spins[bx][ibtau - 1].spin
            if len(self.spins[bx]) > 1 and self.spins[bx][0].tau < 0:
                self.spins[bx].pop(0)

    def spin_update(self):
        flip = [[] for i in range(self.L)]
        for kx in range(self.L):
            for itau in range(len(self.spins[kx])):
                flip[kx].append(random.choice([-1, 1]))
        for bx in range(self.L):
            for ibtau in range(len(self.spins[bx])):
                if len(self.cluster[bx]) > 0:
                    rbx, rbtau = self.root(bx, ibtau)
                else:
                    rbx, rbtau = bx, ibtau
                self.spins[bx][ibtau].spin *= flip[rbx][rbtau]

    def x2_hord(self):
        """
        kinkに対応するスピンに応じてkink.graphを更新
        スピンが平行(反平行)ならd(h)に更新
        """
        for kx in range(self.L):
            for iktau in range(len(self.kinks[kx])):
                if self.kinks[kx][iktau].graph != "x":
                    continue
                bx0, ibtau0 = self.btilde[(kx, iktau, "L")]
                bx1, ibtau1 = self.btilde[(kx, iktau, "R")]
                if self.spins[bx0][ibtau0].spin == self.spins[bx1][ibtau1].spin:
                    self.kinks[kx][iktau].graph = "d"
                else:
                    self.kinks[kx][iktau].graph = "h"

    def remove_kinks(self):
        """
        spinが前の時間と同じならkinkを削除
        """
        samewformer = [[] for i in range(self.L)]
        for kx in range(self.L):
            for iktau in range(len(self.kinks[kx])):
                bx0, ibtau0 = self.btilde[(kx, iktau, "L")]
                if self.spins[bx0][ibtau0].spin == self.spins[bx0][ibtau0 - 1].spin:
                    samewformer[kx].append(True)
                else:
                    samewformer[kx].append(False)
        for kx in range(self.L):
            self.kinks[kx] = [
                kink for kink, swf in zip(self.kinks[kx], samewformer[kx]) if not swf
            ]

    def remove_spins(self):
        """
        spinが前の時間と同じなら削除
        ただし、spinがすべて同じなら１つだけ残す
        """
        samewformer = [[] for i in range(self.L)]
        for bx in range(self.L):
            for ibtau in range(len(self.spins[bx])):
                if self.spins[bx][ibtau].spin == self.spins[bx][ibtau - 1].spin:
                    samewformer[bx].append(True)
                else:
                    samewformer[bx].append(False)
        new_spins = [[] for i in range(self.L)]
        for bx in range(self.L):
            if all(swf for swf in samewformer[bx]):
                new_spins[bx].append(Spin(-1, self.spins[bx][0].spin))
            else:
                for ibtau in range(len(self.spins[bx])):
                    if not samewformer[bx][ibtau]:
                        new_spins[bx].append(self.spins[bx][ibtau])
        self.spins = new_spins

    def assign_graph(self):
        """
        kinkにgraph"h"か"d"を割り当てる
        """
        for kx in range(self.L):
            for iktau in range(len(self.kinks[kx])):
                self.kinks[kx][iktau].graph = random.choice(["h", "d"])

    def insert_kink(self):
        """
        新しいkinkを挿入
        """
        new_kinks = [[] for _ in range(self.L)]
        for kx in range(self.L):
            tauk, n = gen_uniformly_events(self.beta, self.lam)
            for iktau in range(n):
                new_kinks[kx].append(Kink(tauk[iktau], "x"))
        for kx in range(self.L):
            for iktau in range(len(new_kinks[kx])):
                self.add_kinks(self.kinks, kx, new_kinks[kx][iktau].ktau, "x")
        return new_kinks

    def conf_update(self):
        self.assign_graph()
        new_kinks = self.insert_kink()
        self.make_b()
        self.make_btilde()
        self.insert_spin(new_kinks)
        self.x2_hord()
        self.cluster_update()
        self.spin_update()
        self.remove_kinks()
        self.remove_spins()
