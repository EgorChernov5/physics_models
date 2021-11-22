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


def positive_charges(charges: list):
    """
    Удаляет отрицательные заряды
    :param charges: test_charges
    :return: positive_charges
    """
    for i in charges:
        if i[0] <= 0:
            charges.remove(i)
    positive_charges = charges
    return positive_charges


def draw_start_coordinates(positive_ch):
    """
    Рисует начальные координаты вокруг заряда и возвращает их в виде списка
    :param positive_ch: positive_charges
    :return: charges_w_st_coord
    """
    charge_w_st_coord = []
    charges_w_st_coord = []
    for i in positive_ch:
        a = numpy.pi / 4
        charge_w_st_coord.append(i[0])
        while a != 9 * numpy.pi / 4:
            x = i[1] * 100 + 1 + radius * numpy.cos(a)
            y = i[2] * 100 + 1 + radius * numpy.sin(a)
            pygame.draw.circle(sc, white, [x, y], 1)
            charge_w_st_coord.append([x, y])
            a += numpy.pi / 4
        charges_w_st_coord.append(charge_w_st_coord)
        charge_w_st_coord = []
    return charges_w_st_coord


def value_E(charges, x, y):
    """
    Показывает направление напряженности в указанной точке
    :param charges: список зарядов
    :param x: начальная координата x
    :param y: начальная координата y
    :return: координаты конца вектора в виде списка
    """
    k = 9 * 10 ** 9
    Ex = 0
    Ey = 0
    for i in charges:
        if x / 100 == i[1] and y / 100 == i[2]:
            continue
        q = i[0] * 10 ** (-9)
        r = (((i[1] - x / 100) ** 2 + (i[2] - y / 100) ** 2) ** (1 / 2))
        E = (k * q) / (r ** 2)
        dx = (x / 100) * E / r
        dy = (y / 100) * E / r
        Ex += dx
        Ey += dy
    return [Ex * 100, Ey * 100]


def draw_lines(ch_w_st_coord):
    """
    Рисует линии напряженности
    :param ch_w_st_coord: charges_w_st_coord
    """
    dl = 50
    for i in ch_w_st_coord:
        for j in i:
            if j == i[0]:
                continue
            x1, y1 = j
            while 0 <= x1 <= width or 0 <= y1 <= height:
                x2, y2 = value_E(test_charges, x1, y1)
                r = numpy.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                a = numpy.arccos((x2 - x1)/r)
                dx = x1 + dl * numpy.cos(a)
                dy = y1 + dl * numpy.sin(a)
                pygame.draw.aaline(sc, white, [x1, y1], [dx, dy])
                x1 += dx
                y1 += dy
    return None


# def draw_vec(charges):
#     """
#     Рисует линии напряженности
#     :param charges: test_charges
#     """
#     kxv = width / 100
#     kyv = height / 100
#     xv = []
#     yv = []
#
#     for i in range(1, int(kxv)):
#         xv.append(i * 100)
#     for i in range(1, int(kyv)):
#         yv.append(i * 100)
#
#     for i in xv:
#         for j in yv:
#             pygame.draw.aaline(sc, white, [i, j], value_E(charges, i, j))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        draw_charges(test_charges)
        draw_lines(draw_start_coordinates(positive_charges(test_charges)))

        pygame.display.update()

    clock.tick(FPS)
