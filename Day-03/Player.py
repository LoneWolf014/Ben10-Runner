import pygame as pg
from Resources import *

class Player(pg.sprite.Sprite):
    def __init__(self, ground_level):
        super().__init__()
        # -- Player -------------------------------------------------------- #
        player_walk_1 = pg.image.load("Graphics/Ben/Walk/1.png").convert_alpha()
        player_walk_2 = pg.image.load("Graphics/Ben/Walk/2.png").convert_alpha()
        player_walk_3 = pg.image.load("Graphics/Ben/Walk/3.png").convert_alpha()
        player_walk_4 = pg.image.load("Graphics/Ben/Walk/4.png").convert_alpha()
        
        self.player_walk = [player_walk_1, player_walk_2, player_walk_3, player_walk_4]
        self.player_index = 0

        player_jump_1 = pg.image.load("Graphics/Ben/Jump/1.png").convert_alpha()
        player_jump_2 = pg.image.load("Graphics/Ben/Jump/2.png").convert_alpha()
        player_jump_3 = pg.image.load("Graphics/Ben/Jump/3.png").convert_alpha()
        player_jump_4 = pg.image.load("Graphics/Ben/Jump/4.png").convert_alpha()
        
        self.player_jump = [player_jump_1, player_jump_2, player_jump_3, player_jump_4]

        self.ground_level = ground_level
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, self.ground_level))

        self.mask = pg.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()

        self.gravity = 0

    def player_input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_SPACE] and self.rect.bottom >= self.ground_level:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= self.ground_level : self.rect.bottom = self.ground_level

    def animation_state(self):
        if self.rect.bottom < self.ground_level:
            self.player_index += 0.25
            if self.player_index >= len(self.player_jump):
                self.player_index = 0

            self.image = self.player_jump[int(self.player_index)]

            self.mask = pg.mask.from_surface(self.image)
            # self.mask_image = self.mask.to_surface()
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0

            self.image = self.player_walk[int(self.player_index)]

            self.mask = pg.mask.from_surface(self.image)
            self.mask_image = self.mask.to_surface()

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        # screen.blit(self.mask_image, self.rect)
        # pg.draw.rect(screen, "green", self.rect, 2)