from math import *
from random import choice
from random import randint

import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


def draw_rectangle(x, y, width, height, color, rotation=0):
    """Draw a rotated rectangle, centered at x, y.

    Arguments:
      x (int/float):
        The x coordinate of the center of the shape.
      y (int/float):
        The y coordinate of the center of the shape.
      width (int/float):
        The width of the rectangle.
      height (int/float):
        The height of the rectangle.
      color (str):
        Name of the fill color, in HTML format.
      rotation (int/float):
        Rotation angle of the rectangle

    """
    points = []

    # The distance from the center of the rectangle to
    # one of the corners is the same for each corner.
    radius = sqrt((height / 2) ** 2 + (width / 2) ** 2)

    # Get the angle to one of the corners with respect
    # to the x-axis.
    angle = atan2(height / 2, width / 2)

    # Transform that angle to reach each corner of the rectangle.
    angles = [angle, -angle + pi, angle + pi, -angle]

    # Convert rotation from degrees to radians.
    rot_radians = (pi / 180) * rotation

    # Calculate the coordinates of each point.
    for angle in angles:
        y_offset = -1 * radius * sin(angle + rot_radians)
        x_offset = radius * cos(angle + rot_radians)
        points.append((x + x_offset, y + y_offset))

    pygame.draw.polygon(screen, color, points)


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 120

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy

        self.vy -= 1.6

        if self.y > HEIGHT - 50:
            self.vy = -0.5 * self.vy
            if abs(self.vy) > 2.7:
                self.y -= self.vy
                self.vx = 0.8 * self.vx
            else:
                self.vy = 0
                #self.vx = 0
        if (self.x < 10) or (self.x > WIDTH - 10):
            self.vx = -0.5 * self.vx
            self.x += self.vx

    def draw(self):
        """Отрисовка объекта"""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        """Конструктор класса Gun"""
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.length = 40

    def fire2_start(self, event):
        """Начинает накопление заряда выстрела"""
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * cos(self.an)
        new_ball.vy = - self.f2_power * sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if (event.pos[0] - 20) != 0:
                self.an = atan((event.pos[1] - 450) / (event.pos[0] - 20))
            else:
                self.an = -90
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        """Отрисовка объекта"""
        draw_rectangle(40 + self.length / 2 * cos(self.an),
                       450 + self.length / 2 * sin(self.an),
                       self.length, 15, self.color,
                       -(self.an / pi) * 180)

    def power_up(self):
        """Накопление заряда выстрела (при задержке кнопки мыши)"""
        if self.f2_on:
            if self.f2_power < 50:
                self.f2_power += 1
            self.color = YELLOW
            if self.length >= 80:
                self.color = GREEN
            if self.length < 80:
                self.length += 1 * (40 / 50)
        else:
            self.color = GREY
            self.length = 40


class Target:
    """Класс для мишени (цели)"""
    points = 1
    live = 1

    def __init__(self):
        """ Инициализация новой цели. """
        x = self.x = randint(450, 700)
        y = self.y = randint(300, 550)
        r = self.r = randint(20, 40)
        vx = self.vx = 0
        vy = self.vy = randint(-10, 10)
        freq = self.freq = randint(1000, 2000) / 1000
        amp = self.amp = randint(8, 20)
        time = self.time = 0
        color = self.color = RED

    def draw(self):
        """Отрисовка цели"""
        pygame.draw.circle(
            screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def move(self):
        """Переместить цель по прошествии единицы времени.

        Метод описывает перемещение цели за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy (размер окна 800х600).
        """
        self.y += self.vy
        self.x += self.amp * sin(self.freq * self.time / 10)
        self.time += 3

        if self.y > HEIGHT - 50:
            self.vy = -self.vy
        if self.y < 50:
            self.vy = -self.vy


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
targets = [Target(), Target()]
global score
score = 0

clock = pygame.time.Clock()
gun = Gun(screen)

finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    for t in targets:
        t.draw()
    for b in balls:
        b.draw()
        b.live -= 1
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
    for t in targets:
        t.move()
    for b in balls:
        b.move()
        for t in targets:
            if b.hittest(t) and t.live:
                score += 1
                print("Hit! Your score is now ", score)
                t.live = 0
                # target.new_target()
                targets.remove(t)
                balls.remove(b)
                targets.append(Target())
        if b.live < 0:
            balls.remove(b)
            # print("del")

    gun.power_up()

    if score == 5:
        print("You won!")
        finished = True

pygame.quit()
