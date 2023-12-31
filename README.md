# 1次元 XY modelにおけるループアルゴリズム

$$
\def\bra#1{\mathinner{\left\langle{#1}\right|}}
\def\ket#1{\mathinner{\left|{#1}\right\rangle}}
\def\braket#1#2{\mathinner{\left\langle{#1}\middle|#2\right\rangle}}
$$

１ 次元XY模型のハミルトニアンは、
$$
\mathcal{H} =  -J\sum_i(S_i^xS_{i+1}^x + S_i^yS_{i+1}^y)\notag\\
= -\frac{J}{2}\sum_i(S_i^+S_{i+1}^- + S_i^-S_{i+1}^+)
$$
である。分配関数は、
$$
Z = \mathrm{Tr}\bra{C_0}e^{-\beta\mathcal{H}}\ket{C_0}
$$
であり、経路積分表示すると、
$$
Z = \sum_{C_0,...C_M}\bra{C_0}e^{-\Delta\tau\mathcal{H}}\ket{C_M}\bra{C_M}e^{-\Delta\tau\mathcal{H}}\ket{C_{M-1}}...\bra{C_2}e^{-\Delta\tau\mathcal{H}}\ket{C_{1}}\bra{C_1}e^{-\Delta\tau\mathcal{H}}\ket{C_{0}}
$$
ただし、$M$は$\beta$の分割数であり、$\Delta\tau = \beta/M$は微小虚時間間隔である。
ボルツマン因子は、
$$
W = \bra{C_0}e^{-\Delta\tau\mathcal{H}}\ket{C_M}\bra{C_M}e^{-\Delta\tau\mathcal{H}}\ket{C_{M-1}}...\bra{C_2}e^{-\Delta\tau\mathcal{H}}\ket{C_{1}}\bra{C_1}e^{-\Delta\tau\mathcal{H}}\ket{C_{0}}\notag\\
= \Pi_{i,k}w_i^k
$$
となる。$w_i^k$は局所ボルツマン因子であり、$S_i^z$の固有状態$s$を基底とすると、
$$
w_i^k= \bra{s_i^{k+1},s_{i+1}^{k+1}}e^{\frac{J\Delta\tau}{2}(S_i^+S_{i+1}^- + S_i^-S_{i+1}^+)}\ket{s_i^k,s_{i+1}^k}
$$
となる。
ハミルトニアンに定数$J\Delta\tau/4$を加え、$\Delta\tau$の１次まで展開すると、
$$
w_i = \bra{s_i',s_j'}1 + \frac{J\Delta\tau}{2}(S_i^+S_j^- + S_i^-S_j^+ + \frac{1}{2})\ket{s_i,s_j}\\
= \delta_{s_i', s_i}\delta_{s_j',s_j} + \frac{J\Delta\tau}{4}(\delta_{s_i',s_j}\delta_{s_j',s_i} + \delta_{s_i,-s_j}\delta_{s_i',-s_j'})
$$
（略）
