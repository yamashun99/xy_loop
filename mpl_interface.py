import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


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
    # lines1 = self.vlines(bxs, mins, maxs, colors="k", linewidths=5)
    # lines2 = self.vlines(
    #    [bx for bx in range(c.L)], 0, c.beta, colors="k", linestyles="dotted"
    # )
    segments1 = [((bx, min_), (bx, max_)) for bx, min_, max_ in zip(bxs, mins, maxs)]
    lines1 = LineCollection(segments1, colors="k", linewidths=5)
    self.add_collection(lines1)

    segments2 = [((bx, 0), (bx, c.beta)) for bx in range(c.L)]
    lines2 = LineCollection(segments2, colors="k", linestyles="dotted")
    self.add_collection(lines2)

    return [lines1, lines2]


def kinkplot(self, c, showgraph=False):
    graphsymbol = {"h": "=", "d": "X", "x": "None"}
    segments = []
    for kx in range(c.L):
        for ktau in range(len(c.kinks[kx])):
            # self.hlines(c.kinks[kx][ktau].ktau, kx, kx + 1, colors="k", linewidths=5)
            segments.append(
                ((kx, c.kinks[kx][ktau].ktau), (kx + 1, c.kinks[kx][ktau].ktau))
            )
            if showgraph:
                self.text(
                    kx + 0.5,
                    c.kinks[kx][ktau].ktau,
                    graphsymbol[c.kinks[kx][ktau].graph],
                    ha="center",
                    va="top",
                    fontsize=20,
                )
    lines = LineCollection(segments, colors="k", linewidths=5)
    self.add_collection(lines)
    self.set_xlim(0, c.L - 0.5)
    self.set_ylim(0, c.beta)
    return lines


mpl.axes.Axes.spinplot = spinplot
mpl.axes.Axes.kinkplot = kinkplot
