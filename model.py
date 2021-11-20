import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import animation
import numpy as np
from math import sin , cos, pi
from tqdm import tqdm
import numba as nb
from numba import jit
import tkinter

m = 9.1 * 10 ** (-11)
q = 1.6 * 10 ** (-10)

r_q = np.sqrt(5)
size = 150  # size of plot
n = 0  # n lines
N = 1  # n frames
dt = 1
qual = size // 6
Cell = [-1, -10, -q, m, 0, 0]
q_prop = np.array([[-1, -10, -q, m, 0, 0, 1], [30, 0, q, m, 0, 0, 0], [-30, 0, q, m, 0, 0, 1]]).astype(
    np.float32)  # [[xq1, yq1, q1, mq1, vxq1, vyq1], [xq2, yq2, q2, mq2, vxq2, vyq2] ... ]
# nn=200
# q_prop=np.empty((nn,6))
# for i in range(nn):
# q_prop[i]=[size-np.random.rand()*2*size, size-np.random.rand()*2*size, q*(1-np.random.rand()*2), m*np.random.rand(), 0,0]

gr = np.mgrid[-size:(size + 1):qual, -size:(size + 1):qual]
xg, yg = np.array(gr[0]).reshape(-1), np.array(gr[1]).reshape(-1)


# print(len(xg), len(yg))
# print(gr)

@nb.jit()
def E(q_prop, xs, ys, nq):
    l = 1
    k = 9 * 10 ** 9
    Ex = 0
    Ey = 0
    c = 0
    if nq == None:
        for c in range(len(q_prop)):
            q = q_prop[c]
            r = ((xs - q[0]) ** 2 + (ys - q[1]) ** 2) ** 0.5
            dEv = (k * q[2]) / r ** 2
            dEx = (xs - q[0]) * (dEv / r) * l
            dEy = (ys - q[1]) * (dEv / r) * l

            Ex += dEx
            Ey += dEy
        return Ex, Ey
    else:
        for c in range(len(q_prop)):
            if c != nq:
                q = q_prop[c]

                r = ((xs - q[0]) ** 2 + (ys - q[1]) ** 2) ** 0.5
                dEv = (k * q[2]) / r ** 2
                dEx = (xs - q[0]) * (dEv / r) * l
                dEy = (ys - q[1]) * (dEv / r) * l

                Ex += dEx
                Ey += dEy
        return Ex, Ey


# k=0.0000000004
# dt=(((size*q_prop[0][3])/(q_prop[0][2]*E(q_prop,q_prop[0][0],q_prop[0][1],0 )[0]))**2)/N*k
@nb.jit()
def Draw_feld(q_prop):
    arrows = np.ones((len(yg) * len(xg), 2, 2))

    for c, z in enumerate(zip(xg, yg)):
        xs, ys = z
        # print(c)
        dx, dy = E(q_prop, xs, ys, None)
        l = ((dx) ** 2 + (dy) ** 2) ** 0.5

        # print(dx, dy)
        arrows[c] = np.array([[xs, xs + dx / l * 10], [ys, ys + dy / l * 10]])
    return arrows


@nb.jit()
def Update_all(q_prop):
    vx = 0
    vy = 0
    x = 0
    y = 0
    q_prop_1 = np.copy(q_prop)
    for c in range(len(q_prop)):
        if q_prop[c][6] == 1:
            xs = q_prop[c][0]
            ys = q_prop[c][1]
            q = q_prop[c][2]
            m = q_prop[c][3]
            vx = q_prop[c][4]
            vy = q_prop[c][5]
            Ex, Ey = E(q_prop, xs, ys, c)

            x = (((Ex * q) / m) * dt ** 2) / 2 + vx * dt + xs
            y = (((Ey * q) / m) * dt ** 2) / 2 + vy * dt + ys
            vx += ((Ex * q) / m) * dt
            vy += ((Ey * q) / m) * dt
            # print(q_prop[c]-[x,y,q,m,vx,vy])
            q_prop_1[c] = [x, y, q, m, vx, vy, 1]

    return q_prop_1


@nb.jit()
def Make_data(size, q_prop, r_q, n):
    # global q_prop
    q_prop = Update_all(q_prop)
    arrows = Draw_feld(q_prop)
    linen = np.empty((np.count_nonzero(q_prop[:, 2] > 0), n, 6000000), dtype=np.float64)

    linen[:] = np.nan
    theta = np.linspace(0, 2 * np.pi, n)
    # mask=q_prop[ q_prop[:,2]>0 ]
    mask = q_prop[q_prop[:, 2] > 0]  # [ q_prop[q_prop[:,2]>0][:,6]==1 ]

    for cq in range(len(mask)):

        qmask = mask[cq]
        xr = r_q * np.cos(theta) + qmask[0]
        yr = r_q * np.sin(theta) + qmask[1]

        for c in range(len(xr)):

            xs = xr[c]
            ys = xr[c]

            lines = np.empty((2, 3000000), dtype=np.float64)
            lines[:] = np.nan
            stop = 0
            nnn = 0
            lines[0][nnn] = xs
            lines[1][nnn] = ys
            while abs(xs) < size + 2 and abs(ys) < size + 2:

                nnn += 1
                for cq1 in range(len(q_prop)):
                    q = q_prop[cq1]
                    if ((ys - q[1]) ** 2 + (xs - q[0]) ** 2) ** 0.5 < r_q * 0.5:
                        stop = 1
                        break
                if stop == 1:
                    break
                dx, dy = E(q_prop, xs, ys, None)

                xs += dx
                ys += dy
                lines[0][nnn] = xs
                lines[1][nnn] = ys

            linen[cq, c, :] = lines.reshape(-1)
    return arrows, linen, q_prop


fig = plt.figure(dpi=100)
ax = plt.axes()
ax.set_axis_off()
plt.xlim(-(size + 1), (size + 1))
plt.ylim(-(size + 1), (size + 1))
plt.gca().set_aspect('equal', adjustable='box')
a_lines = []
points = []
a_arrows = []
arrows, lines, q_prop = Make_data(size, q_prop, r_q, n)

for _ in range(lines.shape[0] * lines.shape[1]):
    a_lines.append(plt.plot([], [], ls="-", lw=0.8, c="r")[0])
for _ in range(len(yg) * len(xg)):
    a_arrows.append(plt.plot([], [], ls="-", lw=0.8, c="r")[0])
points.append(plt.plot([], [], "bo", lw=500, c="black")[0])


def Plot_im(size, r_q, n):
    global q_prop
    arrows, lines, q_prop = Make_data(size, q_prop, r_q, n)
    c = 0
    for qq in lines:
        for l in qq:
            l = l[l != np.nan].reshape(2, -1)
            a_lines[c].set_data(l[0][::20], l[1][::20])
            c += 1
    c = 0
    # print(arrows.shape)
    for a in arrows:
        a_arrows[c].set_data(a[0], a[1])
        c += 1

    points[0].set_data(q_prop[:, 0], q_prop[:, 1])
    return a_lines + points


def animate(x):
    global q_prop
    print(x)

    return Plot_im(size, r_q, n)


def init():
    lobj = plt.plot([], [], lw=0.8, c="r")[0]
    return lobj,


anim = animation.FuncAnimation(fig, animate, frames=N, interval=200, blit=True)
anim.save('Mit der Wirkung.gif', writer='imagemagick', fps=30)
plt.show()
print(0.2 / dt)