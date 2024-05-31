import pygame as pg
from random import randint

class Obstacle(pg.sprite.Sprite):
    def __init__(self, type, ground_level):
        super().__init__()
        
        if type == "drone":
            drone_frame_1 =pg.image.load("graphics/drones/1.png").convert_alpha()
            drone_frame_2 =pg.image.load("graphics/drones/2.png").convert_alpha()
            drone_frame_3 =pg.image.load("graphics/drones/3.png").convert_alpha()
            
            self.frames = [drone_frame_1, drone_frame_2, drone_frame_3]
            self.y_pos = 150

        else:
            mecha_frame_1 = pg.image.load("graphics/mechadroid/mech1.png").convert_alpha()
            mecha_frame_2 = pg.image.load("graphics/mechadroid/mech2.png").convert_alpha()
            mecha_frame_3 = pg.image.load("graphics/mechadroid/mech3.png").convert_alpha()

            self.frames = [mecha_frame_1, mecha_frame_2, mecha_frame_3]
            self.y_pos = ground_level

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.surf = self.frames[2]
        self.rect = self.surf.get_rect(midbottom = (randint(900, 1100), self.y_pos))

        self.mask = pg.mask.from_surface(self.image)
        # self.mask_image = self.mask.to_surface()

    def animation_state(self):
        # self.animation_index += 0.1
        # if self.animation_index >= len(self.frames): self.animation_index = 0
        # self.image = self.frames[int(self.animation_index)]
        if self.rect.x >= 700:
            self.animation_index = 0
        elif self.rect.x < 700 and self.rect.x >= 600:
            self.animation_index = 1
        else:
            self.animation_index = 2

        self.image = self.frames[self.animation_index]
        self.mask = pg.mask.from_surface(self.image)
        # self.mask_image = self.mask.to_surface()

    def update(self):
        self.rect.x -= 6
        self.animation_state()
        # screen.blit(self.mask_image, self.rect)
        # pg.draw.rect(screen, "red", self.rect, 2)
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()