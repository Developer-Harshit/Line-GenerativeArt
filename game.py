import pygame
import sys
from random import random, randint
from scripts.line import Line, AnimatedLine, FieldLine
from scripts.utils import alpha_screen

# Setup
RENDER_SCALE = 2
WIDTH, HEIGHT = 360 * RENDER_SCALE, 360 * RENDER_SCALE
BG_COLOR = (15, 10, 32)
MODES = ["normal", "animate", "field"]

print("Starting Game")


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Test Project")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # display is half of screen size
        self.display = pygame.Surface((WIDTH / 2, HEIGHT / 2))
        self.alpha_screen = alpha_screen(WIDTH / 2, HEIGHT / 2, 5, BG_COLOR)
        self.clock = pygame.time.Clock()
        self.x = 20
        self.y = 0
        self.mode = 1

        self.line_style = True
        self.resetLine()

    def run(self):
        running = True
        self.display.fill(BG_COLOR)
        frame = 0
        while running:
            self.line.update()

            # Checking Events -----------------------------------------------------|
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        self.mode = (self.mode + 1) % len(MODES)
                        self.resetLine()
                    if event.key == pygame.K_r:
                        self.resetLine()
                    if event.key == pygame.K_e:
                        self.line_style = not self.line_style

            # Rendering Screen ----------------------------------------------------|

            self.line.render(self.display, self.line_style)

            if MODES[self.mode] == "normal":
                self.line.display.blit(self.alpha_screen, (0, 0))

            self.display.fill((255, 255, 255), (5 + (self.mode * 10), 5, 5, 5))
            pygame.display.update()

            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            frame += 1
            # self.clock.tick(40 + self.mode * 10)
            self.clock.tick(60)

        # Quit --------------------------------------------------------------------|
        pygame.quit()
        sys.exit()

    def resetLine(self):
        self.display.fill(BG_COLOR)
        if MODES[self.mode] == "normal":
            self.line = Line(WIDTH / RENDER_SCALE, HEIGHT / RENDER_SCALE, 0.01, 3)
        elif MODES[self.mode] == "animate":
            self.line = AnimatedLine(
                WIDTH / RENDER_SCALE, HEIGHT / RENDER_SCALE, 0.01, 10
            )
        elif MODES[self.mode] == "field":
            self.line = FieldLine(
                WIDTH / RENDER_SCALE, HEIGHT / RENDER_SCALE, randint(1, 4), 0.01, 10
            )


if __name__ == "__main__":
    Game().run()
print("Game Over")
