import pygame as pg

class World():
    def __init__(self, data, map_image):
        self.image = map_image
        self.level_data = data
        self.tile_map = []

    def process_data(self):
        for layer in self.level_data["layers"]:
            if layer["name"] == "Tile Layer 1":
                self.tile_map = layer["data"]

    def draw(self, surface):
        surface.blit(self.image, (0,0))
