import pygame as pg
import Constants as c


class Plant(pg.sprite.Sprite):
    def __init__(self, img, Tx, Ty):
        pg.sprite.Sprite.__init__(self)
        self.image = img
        self.tile_X = Tx
        self.tile_Y = Ty
        #Calc Center Cordinate
        self.x = (self.tile_X - 0.5) *c.TILE_SIZE
        self.y = (self.tile_Y - 0.5) *c.TILE_SIZE
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
