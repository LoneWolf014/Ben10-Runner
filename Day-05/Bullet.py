import pygame as pg
from Resources import *
from dataclasses import dataclass

@dataclass(eq=False)
class Bullet(pg.sprite.Sprite):
    bullet: dict
    speed: int
    name: str

    def __init__(self, x, y, name):
        super().__init__()

        self.name = name
        print(self.name)
        self.speed = 10
        self.bullet = {
            "heatblast" : pg.image.load("Graphics/Heatblast/fire.png").convert_alpha(),
            "diamondhead" : pg.image.load("Graphics/Diamondhead/fire.png").convert_alpha()
        }

        self.image = self.bullet[self.name]
        self.rect = self.image.get_rect(center= (x, y))
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        self.rect.x += 5
        self.destroy()

    def destroy(self):
        if self.rect.x >= (W_Width):
            self.kill()