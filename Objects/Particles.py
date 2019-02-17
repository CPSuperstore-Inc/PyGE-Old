from time import time
from random import uniform
from math import sin, cos, pi

from PyGE.Objects.SpriteSheet import SpriteSheet


RAD_TO_DEG = pi / 180


class ParticleGenerator:
    def __init__(self, screen, x, y, angle, velocity, min_life, max_life, spawn_per_s, spritesheet:SpriteSheet):
        self.velocity = velocity
        self.angle = angle
        self.spawn_delay = 1.0 / spawn_per_s
        self.spritesheet = spritesheet
        self.min_life = min_life
        self.max_life = max_life
        self.y = y
        self.x = x
        self.screen = screen

        self.last_spawn = time()
        self.particles = []

        self.delta_x = cos(self.angle * RAD_TO_DEG) * self.velocity
        self.delta_y = sin(self.angle * RAD_TO_DEG) * self.velocity

    def update(self):
        for p in self.particles:
            p.update()
            if p.time_left <= 0:
                self.particles.remove(p)
            p.x += self.delta_x
            p.y -= self.delta_y

        if time() - self.last_spawn >= self.spawn_delay:
            ttl = uniform(self.min_life, self.max_life)
            self.particles.append(Particle(self.screen, self.x, self.y, ttl, self.spritesheet))
            self.last_spawn = time()


class Particle:
    def __init__(self, screen, x, y, life, spritesheet:SpriteSheet):
        self.spritesheet = spritesheet
        self.life = life
        self.y = y
        self.x = x
        self.screen = screen

        self.creation = time()
        self.expiration = life + self.creation

    def update(self):

        image = self.spritesheet.current_image
        self.screen.blit(image, (self.x, self.y))

    @property
    def age(self):
        return time() - self.creation

    @property
    def time_left(self):
        return self.expiration - time()