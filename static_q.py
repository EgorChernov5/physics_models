# import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.animation as animation


def E(q, r0, x, y):
    """Return the electric field vector E=(Ex,Ey) due to charge q at r0."""
    den = np.hypot(x - r0[0], y - r0[1]) ** 3
    return q * (x - r0[0]) / den, q * (y - r0[1]) / den


# Grid of x, y points
# Матрица x, y
nx, ny = 64, 64
x = np.linspace(-2, 2, nx)
y = np.linspace(-2, 2, ny)
X, Y = np.meshgrid(x, y)


def init():
    # Create a multipole with nq charges of alternating sign, equally spaced
    # on the unit circle.
    # Создание мультиполя с nq зарядами переменного электрического тока, расположенных на
    # одинаковых расстояниях.
    # nq = 2**int(sys.argv[1])
    nq = 4
    charges = []
    for i in range(nq):
        q = i % 2 * 2 - 1
        charges.append([q, [np.cos(2 * np.pi * i / nq), np.sin(2 * np.pi * i / nq)]])
    return charges


def move_charges(charges, i):
    for j in range(len(charges)):
        charges[j] = list(charges[j])
        charges[j][1] = list(charges[j][1])
        charges[j][1][0] += i * 0.1
        charges[j][1][1] += i * 0.1
        charges[j][1] = tuple(charges[j][1])
        charges[j] = tuple(charges[j])
    new_charges = charges
    return new_charges


def vec_el(new_charges):
    # Electric field vector, E=(Ex, Ey), as separate components
    # Вектор электрического поля, E = (Ex, Ey), как отдельные компоненты
    Ex, Ey = np.zeros((ny, nx)), np.zeros((ny, nx))
    for charge in new_charges:
        ex, ey = E(*charge, x=X, y=Y)
        Ex += ex
        Ey += ey
    return Ex, Ey


fig = plt.figure()
ax = fig.add_subplot(111)


def draw_line(Ex, Ey):
    # Plot the streamlines with an appropriate colormap and arrow style
    # Нанести линии обтекания с соответствующей цветовой картой и стилем стрелки
    color = 2 * np.log(np.hypot(Ex, Ey))
    ax.streamplot(x, y, Ex, Ey, color=color, linewidth=1, cmap=plt.cm.inferno,
                  density=2, arrowstyle='->', arrowsize=1.5)


def draw_charges(new_charges):
    # Add filled circles for the charges themselves
    # Добавление закрашенных кружков для самих зарядов
    charge_colors = {True: '#aa0000', False: '#0000aa'}
    for q, pos in new_charges:
        ax.add_artist(Circle(pos, 0.05, color=charge_colors[q > 0]))


def animate(i):
    ax.clear()
    charges = init()
    new_charges = move_charges(charges, i)
    Ex, Ey = vec_el(new_charges)
    draw_line(Ex, Ey)
    draw_charges(new_charges)


sin_animation = animation.FuncAnimation(fig, animate, frames=10, interval=5, repeat=False)

sin_animation.save('anim1.gif', writer='imagemagick', fps=5)

# ax.set_xlabel('$x$')
# ax.set_ylabel('$y$')
# ax.set_xlim(-2, 2)
# ax.set_ylim(-2, 2)
# ax.set_aspect('equal')
# plt.show()
