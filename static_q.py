import pygame
import numpy

pygame.init()

width, height = 1200, 800
white = (255, 255, 255)

sc = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Заряд с линиями напряженности")

clock = pygame.time.Clock()
FPS = 30

osxn = 0
osxk = width
osyn = 0
osyk = height

# pygame.draw.line(sc, white, (osxn, osyk), (osxk, osyk))
# pygame.draw.line(sc, white, (osxn, osyn), (osxn, osyk))

'''
Params:
q1 - величина заряда [нКл = 10^(-9) Кл]
x1 - координата x [см = 10^(-2)]
y1 - координата y [см = 10^(-2)]
'''
q1 = 1
x1 = 3
y1 = 3

# характеристики передаваемых зарядов
test_charges = [[q1, x1, y1]]
radius = 10


def draw_charges(charges: list):
    """
    Рисует заряды
    :param charges: test_charges
    """
    for i in range(len(charges)):
        index = 0
        for j in charges[i]:
            index += 1
            if index > 1:
                if index == 2:
                    x = j * 100
                else:
                    y = j * 100
        pygame.draw.circle(sc, white, (x, y), radius)


def value_E(charges, x, y):
    """
    Показывает направление напряженности в указанной точке
    :param charges: список зарядов
    :param x: начальная координата x
    :param y: начальная координата y
    :return: координаты конца вектора
    """
    dl = 10
    k = 9 * 10 ** 9
    Ex = []
    Ey = []
    for i in charges:
        if x / 100 == i[1] and y / 100 == i[2]:
            continue
        q = i[0] * 10 ** (-9)
        r = numpy.sqrt((i[1] - x / 100) ** 2 + (i[2] - y / 100) ** 2)
        E = (k * q) / (r ** 2)
        dx = (x * E) / r
        dy = (y * E) / r
        Ex.append(dx)
        Ey.append(dy)
    xv = sum(Ex) + x
    yv = sum(Ey) + y
    r = numpy.sqrt((xv - x) ** 2 + (yv - y) ** 2)
    a = numpy.arccos((xv - x) / r)
    dx = x + dl * numpy.cos(a)
    dy = y + dl * numpy.sin(a)
    return [dx, dy]


def draw_vec(charges):
    """
    Рисует линии напряженности
    :param charges: test_charges
    """
    kxv = width / 100
    kyv = height / 100
    xv = []
    yv = []

    for i in range(1, int(kxv)):
        xv.append(i * 100)
    for i in range(1, int(kyv)):
        yv.append(i * 100)

    for i in xv:
        for j in yv:
            pygame.draw.aaline(sc, white, [i, j], value_E(charges, i, j))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        draw_charges(test_charges)
        draw_vec(test_charges)

        pygame.display.update()

    clock.tick(FPS)
