from perlin_noise import PerlinNoise
from scripts.utils import remap
from random import randint, random
from scripts.utils import get_curve
import pygame

BG_COLOR = (12, 5, 25)


class Line:
    def __init__(self, width, height, t_inc=0.01, alpha=2):
        self.width = width
        self.height = height
        self.t_inc = t_inc

        self.points = []
        self.render_points = []

        self.color = pygame.Color(246, 129, 254)
        self.hue = randint(0, 360)

        self.update_hue()

        self.noise = PerlinNoise(1, randint(20, 1000))

        self.display = pygame.Surface((self.width, self.height))
        # # not setting colorkey to get an effect
        self.display.set_colorkey((0, 0, 0))
        self.display.set_alpha(alpha)

        self.xoff = 10000

        self.index = 0

        self.xinc = random() / randint(30, 100)
        self.yinc = random() / randint(10, 30)

        self.anchors = [(20, self.height / 2), (self.width - 20, self.height / 2)]

        # print(self.xinc, self.yinc)
        pass

    def renderPoints(self):
        if self.index >= len(self.render_points):
            self.update()

        my_point = self.render_points[self.index]
        # self.display.fill(self.color, (my_point[0], my_point[1], 1, 1))
        pygame.draw.circle(self.display, self.color, (my_point[0], my_point[1]), 1)

        surf.blit(self.display, (0, 0))

        self.index += 1

    def render(self, surf, style=True):
        self.update_hue()
        if not style:
            # if false ,then RENDERING BY POINTS
            for my_point in self.render_points:
                pygame.draw.circle(
                    self.display, self.color, (my_point[0], my_point[1]), 1
                )
        else:
            # if true ,then RENDERING BY LINE
            for i in range(len(self.render_points) - 1):
                p1 = self.render_points[i]
                p2 = self.render_points[i + 1]
                pygame.draw.aaline(self.display, self.color, p1, p2)

                pass
        surf.blit(self.display, (0, 0))

    def update_hue(self, hue=False):
        if not (hue == False):
            k = list(self.color.hsla)

            k[0] = hue

            self.color.hsla = tuple(k)
        else:
            self.hue = (self.hue + 0.4) % 360
            k = list(self.color.hsla)

            k[0] = self.hue

            self.color.hsla = tuple(k)

    def get_points(self):
        self.points = [self.anchors[0]]
        self.index = 0
        self.yoff = 0
        for x in range(20, int(self.width - 25), 7):
            noise_y = self.noise((self.xoff, self.yoff))
            y_coords = remap(noise_y, -1, 1, 0, self.height)
            self.points.append((x, y_coords))
            self.yoff += self.yinc

        self.xoff += self.xinc
        self.points.append(self.anchors[1])

    def update(self):
        self.render_points = []

        self.get_points()
        self.render_points = get_curve(self.points, self.t_inc)


class AnimatedLine(Line):
    def __init__(self, width, height, t_inc=0.01, alpha=10):
        super().__init__(width, height, t_inc, alpha)
        self.display = pygame.Surface((self.width, self.height))
        # # not setting colorkey to get an effect
        # self.display.set_colorkey((0, 0, 0))
        self.display.set_alpha(alpha)

        self.xinc = random() / randint(30, 100)
        self.yinc = random() / randint(10, 30)

    def render(self, surf, style=True):
        self.display.fill(BG_COLOR)

        super().render(surf, style)


class FieldLine:
    def __init__(self, width, height, nLines=2, t_inc=0.01, alpha=10):
        self.width = width
        self.height = height

        self.nLines = nLines
        self.t_inc = t_inc

        # FOr anchor
        self.aoff = 5
        self.ainc = random() / 100
        # for different lines
        self.zoff = 5000
        self.zinc = 0.0003  # random() / randint(1, 10)
        print("Zinc: ", self.zinc, "Ainc: ", self.ainc)

        # for each line
        # 0.1 0.9 / 60

        self.xinc = random() / randint(25, 50)
        self.yinc = random() / randint(5, 25)

        self.noise = PerlinNoise(1, randint(20, 1000))

        self.color = pygame.Color(246, 129, 254)
        self.hue = randint(0, 360)
        self.update_hue()

        self.display = pygame.Surface((self.width, self.height))
        self.display.set_alpha(alpha)

        self.lines = []  # -->

        self.get_lines()
        print("Xinc: ", self.xinc, "Yinc: ", self.yinc)

    def update_hue(self, hue=False):
        if not (hue == False):
            k = list(self.color.hsla)

            k[0] = hue

            self.color.hsla = tuple(k)
        else:
            self.hue = (self.hue + 0.4) % 360
            k = list(self.color.hsla)

            k[0] = self.hue

            self.color.hsla = tuple(k)

    def get_lines(self):
        self.zoff += self.zinc
        for i in range(self.nLines):
            my_line = Line(self.width, self.height, self.t_inc)
            my_line.xinc = self.xinc
            my_line.yinc = self.yinc
            my_line.anchors = self.get_anchor()
            my_line.color = self.color
            self.lines.append(my_line)

    def get_anchor(self):
        noise_i = self.noise((self.aoff, self.zoff))
        noise_f = self.noise((self.zoff, self.aoff))
        yi = remap(noise_i, -1, 1, 0, self.height)
        yf = remap(noise_f, -1, 1, 0, self.height)
        self.aoff += self.ainc
        return [(20, yi), (self.width - 20, yf)]

    def update(self):
        for line in self.lines:
            line.update()

    def render(self, surf, style=True):
        self.display.fill(BG_COLOR)
        for line in self.lines:
            self.update_hue()
            line.update_hue(self.hue)
            if not style:
                for my_point in line.render_points:
                    pygame.draw.circle(
                        self.display, line.color, (my_point[0], my_point[1]), 1
                    )
            else:
                for i in range(len(line.render_points) - 1):
                    p1 = line.render_points[i]
                    p2 = line.render_points[i + 1]
                    pygame.draw.aaline(self.display, self.color, p1, p2)

        surf.blit(self.display, (0, 0))
