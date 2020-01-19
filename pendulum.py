
import pygame
import math
from decimal import Decimal

from glovars import GRAVITY, DRAG, ANGULAR_DRAG

class Pendulum:

    def __init__(self, x, y, ball):
        self.x = x
        self.y = y
        self.ball = ball
        self.color = pygame.Color('red')
        self.width = 3

        self.armlength = Pendulum.calc_armlength(self.coords, self.ball.center_coords)
        self.angle = Pendulum.calc_angle(self.coords, self.ball.center_coords)
        self.velocity = 0.5
        Pendulum.calc_enter_velocity(self, self.ball)

    @staticmethod
    def calc_armlength(pend_coords, ball_coords):
        distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(pend_coords, ball_coords)]))
        return distance

    @staticmethod
    def calc_angle(pend_coords, ball_coords):
        dx = pend_coords[0]-ball_coords[0]
        dy = pend_coords[1]-ball_coords[1]
        val = math.atan(dy/dx)
        if dx > 0:
            val += math.pi
        return val

    @staticmethod
    def calc_tangent_angle(pend_coords, ball_coords):
        return Pendulum.calc_angle(pend_coords, ball_coords) + math.pi/2

    @staticmethod
    def calc_enter_velocity(pendulum, ball):
        dx = pendulum.coords[0] - ball.center_coords[0]
        dy = pendulum.coords[1] - ball.center_coords[1]

        tangent_angle = Pendulum.calc_tangent_angle(pendulum.coords, ball.center_coords)

        velocity = ball.speed * math.sin(tangent_angle)
        pendulum.velocity = velocity / pendulum.armlength

    @staticmethod
    def calc_exit_velocities(pendulum, ball):
        tangent_angle = Pendulum.calc_tangent_angle(pendulum.coords, ball.center_coords)

        speed = pendulum.velocity * pendulum.armlength
        y = speed * math.sin(tangent_angle)
        x = speed * math.cos(tangent_angle)
        ball.velocity = [x,y]

    @property
    def coords(self):
        return (self.x, self.y)

    def display(self, screen):
        pygame.draw.line(screen, self.color, self.coords, self.ball.center_coords, self.width)

    def apply_gravity(self, dt):
        self.velocity += math.cos(self.angle) * GRAVITY * dt / 100

    def apply_drag(self, dt):
        self.velocity *= ANGULAR_DRAG**dt

    def move(self, dt):

        self.apply_gravity(dt)
        self.apply_drag(dt)
        self.angle += self.velocity*dt

        Pendulum.calc_exit_velocities(self, self.ball)
        self.ball.x = self.x + self.armlength*math.cos(self.angle) - self.ball.size/2
        self.ball.y = self.y + self.armlength*math.sin(self.angle) - self.ball.size/2

