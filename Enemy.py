
import pygame as pg
from pygame.math import Vector2

class Zombie(pg.sprite.Sprite):
    
    def __init__(self, waypoints, image):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.tile = Vector2(self.waypoints[0])
        self.target_tile = 1
        self.speed = .5
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = self.tile

    def update(self):
        self.move()

    
    def move(self):
        if self.target_tile < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_tile])
            self.movement = self.target - self.tile
        else:
            #Enemy has reached the end
            self.kill()
        
        #Calculate distance to target
        SpceLeft = self.movement.length()
        #Check if remaining distance is greater than the enemy speed
        if SpceLeft >= self.speed:
            self.tile += self.movement.normalize() * self.speed
        else:
            if SpceLeft != 0:
                self.tile += self.movement.normalize() * SpceLeft
            self.target_tile += 1

        
        self.rect.center = self.tile