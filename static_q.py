import pygame

pygame.init()

width, height = 1200, 800
white = (255, 255, 255)
osxn = width * 1/4
osxk = width * 3/4
osyn = height * 1/6
osyk = height * 3/4

sc = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Заряд с линиями напряженности")

clock = pygame.time.Clock()
FPS = 30

# pygame.draw.line(sc, white, (osxn, osyk), (osxk, osyk))
# pygame.draw.line(sc, white, (osxn, osyn), (osxn, osyk))
'''
Params:
q1 - величина заряда;
x1 - координата x;
y1 - координата y;
'''
q1 = 1
x1 = 300
y1 = 300

# характеристики передаваемых зарядов
charges = [[q1, x1, y1]]


def draw_q(prob_q: list):
    """
    Рисует заряды.
    :param prob_q: charges
    """
    for i in range(len(prob_q)):
        index = 0
        for j in prob_q[i]:
            index += 1
            if index > 1:
                if index == 2:
                    x = j
                else:
                    y = j
        pygame.draw.circle(sc, white, (osxn + x, osyk - y), 50)


def draw_vec(prob_q):
    """
    Рисует векторы напряженности.
    :param prob_q: charges
    """
    return None


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        draw_q(charges)

        pygame.display.update()

    clock.tick(FPS)
