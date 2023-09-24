import matplotlib as mpl
import matplotlib.pyplot as plt


def spinplot(self, c):
    mins = []
    bxs = []
    for bx in range(c.L):
        if c.spins[bx][0].tau < 0:
            if c.spins[bx][0].spin == 1:
                mins.append(0)
                bxs.append(bx)
            continue
        if c.spins[bx][-1].spin == 1:
            mins.append(0)
            bxs.append(bx)
        for ibtau in range(len(c.spins[bx])):
            if c.spins[bx][ibtau].spin == 1:
                mins.append(c.spins[bx][ibtau].tau)
                bxs.append(bx)
    maxs = []
    for bx in range(c.L):
        if c.spins[bx][0].tau < 0:
            if c.spins[bx][0].spin == 1:
                maxs.append(c.beta)
            continue
        for ibtau in range(len(c.spins[bx])):
            if c.spins[bx][ibtau].spin == -1:
                maxs.append(c.spins[bx][ibtau].tau)
        if c.spins[bx][-1].spin == 1:
            maxs.append(c.beta)
    self.vlines(bxs, mins, maxs, colors="k", linewidths=5)
    self.vlines([bx for bx in range(c.L)], 0, c.beta, colors="k", linestyles="dotted")


def kinkplot(self, c, showgraph=False):
    graphsymbol = {"h": "=", "d": "X", "x": "None"}
    for kx in range(c.L):
        for ktau in range(len(c.kinks[kx])):
            self.hlines(c.kinks[kx][ktau].ktau, kx, kx + 1, colors="k", linewidths=5)
            if showgraph:
                self.text(
                    kx + 0.5,
                    c.kinks[kx][ktau].ktau,
                    graphsymbol[c.kinks[kx][ktau].graph],
                    ha="center",
                    va="top",
                    fontsize=20,
                )
    self.set_xlim(0, c.L - 0.5)
    self.set_ylim(0, c.beta)


mpl.axes.Axes.spinplot = spinplot
mpl.axes.Axes.kinkplot = kinkplot
