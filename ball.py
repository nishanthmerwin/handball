
from glovars import GRAVITY, DRAG, CANVAS
import math
import pygame


class Ball:

    def __init__(self):
        self.mass = 1
        self.velocity = [15, 0]
        self.x = 350
        self.y = 50
        self.size = 20
        self.jump_cooldown = True
        self.last_jump = None

    @property
    def color(self):
        return (0, 0, 255) if self.jump_cooldown else (0, 255, 0)

    @property
    def thickness(self):
        return 8 if self.jump_cooldown else 2

    @property
    def angle(self):
        vel_x = self.velocity[0]
        vel_y = self.velocity[1]
        return math.atan2(vel_y, vel_x)
    
    def jump(self):
        if self.jump_cooldown:
            self.velocity[1] -= 80
            self.jump_cooldown = False
            self.last_jump = pygame.time.get_ticks()

    @property
    def speed(self):
        return math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)

    @property
    def center_coords(self):
        return (self.x + self.size/2, self.y + self.size/2)

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def display(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect, self.thickness)
        new_pos = self.center_coords
        new_pos = (new_pos[0] + self.velocity[0]*3, new_pos[1] + self.velocity[1]*3)


        pygame.draw.line(screen, (255, 0, 0), self.center_coords, new_pos, int(self.speed/10))

    def apply_drag(self, dt):
        self.velocity[0] *= DRAG**dt
        self.velocity[1] *= DRAG**dt

    def apply_gravity(self, dt):
        self.velocity[1] = self.velocity[1] + GRAVITY*dt

    def reset_jump(self):
        if self.jump_cooldown is False:
            if (pygame.time.get_ticks() - self.last_jump) > 3000:
                self.jump_cooldown = True

    def move(self, dt):
        self.reset_jump()
        self.apply_drag(dt)
        self.apply_gravity(dt)

        dx = dt * self.velocity[0]
        dy = dt * self.velocity[1]
        self.x += dx
        self.y += dy

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.size

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.size

