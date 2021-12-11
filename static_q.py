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
nx, ny = 64 * 25, 64 * 25
x = np.linspace(-50, 50, nx)
y = np.linspace(-50, 50, ny)
X, Y = np.meshgrid(x, y)


def init():
    # Create a multipole with nq charges of alternating sign, equally spaced
    # on the unit circle.
    # Создание мультиполя с nq зарядами переменного электрического тока, расположенных на
    # одинаковых расстояниях.
    # nq = 2**int(sys.argv[1])
    # nq = 3
    # charges = []
    # for i in range(nq):
    #     q = i % 2 * 2 - 1
    #     x = np.cos(2 * np.pi * i / nq)
    #     if x == np.cos(np.pi / 2) or x == np.cos(-np.pi / 2) or x == np.cos(-np.pi / 2 * 3):
    #         x = 0
    #     y = np.sin(2 * np.pi * i / nq)
    #     if y == np.sin(np.pi) or y == np.sin(0):
    #         y = 0
    #     charges.append([q, [x, y]])
    # return charges  # [[1, [1.0, 0]], [-1, [0.0, 1.0]], [1, [0.0, -1.0]]]

    return [[-1, [0.0, 3.0]], [-1, [0.0, 0.0]]]



def update_charges(charges):
    # [[xq1, yq1, q1, mq1, vxq1, vyq1, z]]
    up_charges = []
    for charge in charges:
        q = charge[0] * 10**(-9)
        xq, yq = charge[1]
        mq = 9.1 * 10**(-11)
        vxq = 0
        vyq = 0
        if q == 10**(-9):
            z = 1
        else:
            z = 0
        up_charges.append([xq, yq, q, mq, vxq, vyq, z])
    up_charges = np.array(up_charges)
    return up_charges


def initial_charges(up_charges):
    init_charges = []
    for up_charge in up_charges:
        r0 = []
        q = up_charge[2] * 10**9
        r0.extend([up_charge[0], up_charge[1]])
        init_charges.append([q, r0])
    return init_charges


def move_charges(up_charges):
    new_up_charges = np.copy(up_charges)
    for c in range(len(up_charges)):  # проход по зарядам и обновление их координат
        xs = up_charges[c][0]
        ys = up_charges[c][1]
        q = up_charges[c][2]
        m = up_charges[c][3]
        vx = up_charges[c][4]
        vy = up_charges[c][5]
        z = up_charges[c][6]
        Ex, Ey = E_values(up_charges, xs, ys, c)
        x = Ex
        y = Ey
        new_up_charges[c] = [x, y, q, m, vx, vy, z]
    return new_up_charges  # возвращение обновлённого массива характеристик зарядов


def vec_el(new_charges):
    # Electric field vector, E=(Ex, Ey), as separate components
    # Вектор электрического поля, E = (Ex, Ey), как отдельные компоненты
    Ex, Ey = np.zeros((ny, nx)), np.zeros((ny, nx))
    for charge in new_charges:
        ex, ey = E(*charge, x=X, y=Y)
        Ex += ex
        Ey += ey
    return Ex, Ey


def E_values(up_charges, xs, ys, nq):
    k = 9 * 10 ** 9
    i = 0
    for c in range(len(up_charges)):
        if c != nq:
            x = up_charges[c][0]
            y = up_charges[c][1]
            q = up_charges[c][2]
            r = ((xs - x) ** 2 + (ys - y) ** 2) ** 0.5
            module_E = (k * q) / r ** 2
            dx = (module_E * (x - xs) + r * xs) / r
            dy = (module_E * (y - ys) + r * ys) / r
            i += 1
            if i == 1:  # обрабатывается первый заряд
                result_Ex = dx
                result_Ey = dy
            else:  # сложение результирующих векторов
                result_Ex += result_Ex + dx - xs
                result_Ey += result_Ey + dy - ys
    return [result_Ex, result_Ey]


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
        ax.add_artist(Circle(pos, 1, color=charge_colors[q > 0]))


data_charges = []


def manager_charges(i):
    if data_charges:
        up_charges = update_charges(data_charges[i])
        new_up_charges = move_charges(up_charges)
        new_charges = initial_charges(new_up_charges)
        Ex, Ey = vec_el(new_charges)
        draw_line(Ex, Ey)
        draw_charges(new_charges)
        data_charges.append(new_charges)
    else:
        data_charges.append(init())
        Ex, Ey = vec_el(data_charges[0])
        draw_line(Ex, Ey)
        draw_charges(data_charges[0])
        data_charges.append(data_charges[0])


def animate(i):
    print(i)
    ax.clear()
    manager_charges(i)


sin_animation = animation.FuncAnimation(fig, animate, frames=5, interval=1, repeat=False)

sin_animation.save('anim1.gif', writer='imagemagick', fps=1)

# ax.set_xlabel('$x$')
# ax.set_ylabel('$y$')
# ax.set_xlim(-50, 50)
# ax.set_ylim(-50, 50)
# ax.set_aspect('equal')
# plt.show()
