
import pygame
import math
from decimal import Decimal

from ball import Ball
from pendulum import Pendulum
from glovars import GRAVITY, DRAG, CANVAS


class App:
    def __init__(self):
        self._running = True
        self._display_suf = None
        self.size = CANVAS
        self.width = self.size[0]
        self.height = self.size[1]
        self.bg_color = (255, 255, 255)
        self.pendulum = None
        self.clock = None
        self.fps = 30

    def on_init(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size)
        self._running = True
        self.ball = Ball()

    def reset(self):
        self.on_init()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            self.pendulum = Pendulum(x, y, self.ball)

        if event.type == pygame.MOUSEBUTTONUP:
            Pendulum.calc_exit_velocities(self.pendulum, self.ball)
            self.pendulum = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.reset()


            if event.key == pygame.K_UP:
                if self.pendulum is None:
                    self.ball.jump()

    def apply_movement(self, dt):
        keymap = pygame.key.get_pressed()
        force = dt * 5
        if keymap[pygame.K_LEFT]:
            self.ball.velocity[0] -= force
        if keymap[pygame.K_RIGHT]:
            self.ball.velocity[0] += force

    def check_collisions(self):
        if self.ball.top < 0:
            self.ball.y = 0
            self.ball.velocity[1] *= -1

        if self.ball.bottom > self.height:
            self.ball.y = self.height - self.ball.size
            self.ball.velocity[1] *= -1

        if self.ball.left < 0:
            self.ball.x = 0
            self.ball.velocity[0] *= -1

        if self.ball.right > self.width:
            self.ball.x = self.width - self.ball.size
            self.ball.velocity[0] *= -1

    def on_loop(self, dt):
        self.check_collisions()
        self.apply_movement(dt)

        if self.pendulum is not None:
            self.pendulum.move(dt)
        else:
            self.ball.move(dt)

    def on_render(self):
        self.screen.fill(self.bg_color)
        self.ball.display(self.screen)
        if self.pendulum is not None:
            self.pendulum.display(self.screen)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            dt = self.clock.tick(self.fps)
            dt = dt / 100.
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop(dt)
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    app = App()
    app.on_execute()
