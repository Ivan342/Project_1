import pygame
from pygame.draw import *
from random import randint

pygame.init()

FPS = 100  # Кадры в секунду
Screen_width = 1000  # Ширина окна
Screen_height = 700  # Высота окна
screen = pygame.display.set_mode((Screen_width, Screen_height))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


class Ball:
    """
    Класс шариков.
    x, y - коодринаты шарика
    r - радиус шарика
    lifetime - время от создания шарика до текущего момента
    color - цвет шарика
    vel_x, vel_y - скорость шарика по осям x и y соответственно
    Метод update() обновляет информацию о шарике с каждым вызовом (раз в кадр)
    Метод reflect_if_on_edge() реализует отражение шарика от стенок
    """
    lifetime = 0
    x = 0
    y = 0
    r = 0
    color = (255, 255, 255)
    vel_x = 0
    vel_y = 0

    def __init__(self, zero_time):
        self.lifetime = zero_time

        self.x = randint(100, Screen_width - 100)
        self.y = randint(100, Screen_height - 100)
        self.r = randint(40, 80)
        self.color = COLORS[randint(0, 5)]

        self.vel_x = randint(-500, 500) / 100
        self.vel_y = randint(-500, 500) / 100

        circle(screen, self.color, (self.x, self.y), self.r)

    def update(self):
        self.lifetime += 1
        self.x += self.vel_x
        self.y += self.vel_y
        circle(screen, self.color, (self.x, self.y), self.r)

    def reflect_if_on_edge(self):
        if (self.x - self.r < 0) or (self.x + self.r > Screen_width):
            self.vel_x = -self.vel_x
        if (self.y - self.r < 0) or (self.y + self.r > Screen_height):
            self.vel_y = -self.vel_y


def click(mouse_event, x_0, y_0, r_0):
    """
    Функция позволяет проверить, был ли произведен щелчок мыши в точке,
    удаленной от (x_0, y_0) не более чем на r_0 (На момент вызова функции).
    В случае, когда это так, функция возвращает True (Иначе - False)
    """
    if (mouse_event.pos[0] - x_0) ** 2 + (mouse_event.pos[1] - y_0) ** 2 <= r_0 ** 2:
        return True
    else:
        return False


pygame.display.update()
clock = pygame.time.Clock()
finished = False

score = 0  # Вводим счет
Balls = []  # Создаем множество, содержащее ссылки на объекты класса Ball (множество шариков)
for i in range(4):
    Balls.append(Ball(i * 100))  # Создаем начальные шарики

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ball in Balls:
                if click(event, ball.x, ball.y, ball.r):  # Проверка попадания по шарику
                    Balls.remove(ball)
                    Balls.append(Ball(0))  # Последовательное удаление и создание нового шарика (по которому попали)
                    score += 1
                    print("Your score is ", score)  # Увеличение счета

    for ball in Balls:  # Обновление параметров каждого шарика, проверка на истечение срока жизни
        ball.update()
        ball.reflect_if_on_edge()
        if ball.lifetime >= 400:  # При истечении срока жизни шарик заменяется на новый
            Balls.remove(ball)
            Balls.append(Ball(0))
    pygame.display.update()
    screen.fill(BLACK)

    if score >= 10:  # Завершение игры если счет больше или равен 10
        print("You won!")
        finished = True

pygame.quit()
