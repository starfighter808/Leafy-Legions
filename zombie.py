import pygame as pg
from pygame.math import Vector2
import math

class Zombie(pg.sprite.Sprite):
    def __init__(self, waypoints, image):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints

        self.pos = Vector2(self.waypoints[0])

        self.target_waypoint = 1
        self.speed = .5
        self.angle = 0


        self.original_image = image
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


    def update(self):
        self.move()


    def move(self):
        #define waypoiont
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movment = self.target - self.pos
        else:
            self.kill()

        #calculate distance to target
        dist = self.movment.length()

        # check if remaining distance is grreater tah nthe enemy speed
        if dist >= self.speed:
            self.pos += self.movment.normalize() * self.speed
        else:
            if dist !=0:
                self.pos += self.movment.normalize() * dist
            self.target_waypoint += 1

        self.rect.center = self.pos
