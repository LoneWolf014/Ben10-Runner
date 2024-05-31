import pygame as pg
from dataclasses import dataclass
from random import randint

@dataclass(eq= False)
class Alien(pg.sprite.Sprite):
    alien_name: str
    omnitrix_sprites: dict
    sprite_index: int
    ground_level: int

    def __init__(self, type, groundlevel):
        super().__init__()

        self.alien_name = type
        self.ground_level = groundlevel
        self.sprite_index = 0

        self.omnitrix_sprites = {
            "Heatblast": self.load_sprites("Graphics/Omnitrix/Heatblast/", 2),
            "Diamondhead": self.load_sprites("Graphics/Omnitrix/Diamondhead/", 2)
        }

        if self.alien_name == "Heatblast":
            self.image = self.omnitrix_sprites["Heatblast"][self.sprite_index]
            self.rect = self.image.get_rect(midbottom = (randint(900, 1100), self.ground_level))
        elif self.alien_name == "Diamondhead":
            self.image = self.omnitrix_sprites["Diamondhead"][self.sprite_index]
            self.rect = self.image.get_rect(midbottom = (randint(900, 1100), self.ground_level))

    def load_sprites(self, path, size):
        sprite_list = []

        for x in range(1, size+1):
            sprite = pg.image.load(f"{path}{x}.png").convert_alpha()
            sprite_list.append(sprite)

        return sprite_list
    
    def animation_state(self):
        self.sprite_index += 0.1
        if self.sprite_index >= len(self.omnitrix_sprites[self.alien_name]): self.sprite_index = 0
        self.image = self.omnitrix_sprites[self.alien_name][int(self.sprite_index)]
        self.image = pg.transform.rotozoom(self.image, 0, 0.6)

    def update(self):
        self.rect.x -= 6
        self.animation_state()
        self.destroy()

    def destroy(self):
        if self.rect.x < -100:
            self.kill()