from Utilities import *
from Bullet import Bullet

@dataclass(eq=False)
class Ben(pg.sprite.Sprite):
    # Attributes
    name: str
    playerstate: str
    gravity: int
    sprite_index: int
    sprites: dict
    ground_level: int
    jump_height: dict
    
    # Methods
    def __init__(self, name, ground_level, display_screen):
        super().__init__()
        self.name = name
        self.playerstate = "gamestate"
        self.gravity = 0
        self.ground_level = ground_level
        self.sprite_index = 0
        self.screen = display_screen

        self.bullet_group = pg.sprite.Group()

        # Load_images
        self.sprites= {
            "ben": {
                "walk" : self.load_images("Graphics/Ben/Walk/", 4),
                "jump" : self.load_images("Graphics/Ben/jump/", 4),
                "transform" : self.load_images("Graphics/Ben/transform/", 5)
            },
            "heatblast": {
                "walk" : self.load_images("Graphics/Heatblast/run/", 6),
                "jump" : self.load_images("Graphics/Heatblast/jump/", 1),
                "transform" : self.load_images("Graphics/Ben/transform/", 5),
                "attack" : self.load_images("Graphics/Heatblast/attack/", 5)
            },
            "diamondhead": {
                "walk" : self.load_images("Graphics/Diamondhead/walk/", 4),
                "jump" : self.load_images("Graphics/Diamondhead/jump/", 1),
                "transform" : self.load_images("Graphics/Ben/transform/", 5),
                "attack" : self.load_images("Graphics/Diamondhead/attack/", 3)
            }
        }

        self.jump_height= {
            "ben" : -20,
            "heatblast" : -22,
            "diamondhead" : -23
        }

        self.image = self.sprites[self.name]["walk"][self.sprite_index]
        self.rect = self.image.get_rect(midbottom = (80, self.ground_level))

    def load_images(self, path, size):
        sprite_list = []
        for x in range(1, size+1):
            image = pg.image.load(f"{path}{x}.png").convert_alpha()
            sprite_list.append(image)

        return sprite_list
    
    def player_input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_SPACE] and self.rect.bottom >= self.ground_level:
            self.gravity = self.jump_height[self.name]

        # if not self.name == "ben" and keys[pg.K_x]:
        #     if not self.playerstate == "attackstate":
        #         self.playerstate = "attackstate"

        #     if self.playerstate == "attackstate":
        #         self.create_bullet()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= self.ground_level : self.rect.bottom = self.ground_level

    def animation_state(self):
        if self.rect.bottom < self.ground_level and self.playerstate == "gamestate":
            self.sprite_index += 0.25
            if self.sprite_index >= len(self.sprites[self.name]["jump"]):
                self.sprite_index = 0
                self.playerstate = "gamestate"

            self.image = self.sprites[self.name]["jump"][int(self.sprite_index)]

            self.mask = pg.mask.from_surface(self.image)
            # self.mask_image = self.mask.to_surface()

        elif not self.name == "ben" and self.playerstate == "attackstate":
            self.sprite_index += 0.2
            if self.sprite_index >= 4.8:
                self.bullet_group.add(self.create_bullet(self.name))
            if self.sprite_index >= len(self.sprites[self.name]["attack"]):
                self.sprite_index = 0
                self.playerstate = "gamestate"


            self.image = self.sprites[self.name]["attack"][int(self.sprite_index)]

        else:
            self.sprite_index += 0.1
            if self.sprite_index >= len(self.sprites[self.name]["walk"]):
                self.sprite_index = 0

            self.image = self.sprites[self.name]["walk"][int(self.sprite_index)]

            self.mask = pg.mask.from_surface(self.image)
            self.mask_image = self.mask.to_surface()

    def transform(self, screen, alien_name):
        if alien_name == "Heatblast":
            pg.draw.circle(screen, "green", self.rect.center, 100)
            self.name = "heatblast"
        elif alien_name == "Diamondhead":
            pg.draw.circle(screen, "green", self.rect.center, 100)
            self.name = "diamondhead"
        else:
            pg.draw.circle(screen, "red", self.rect.center, 100)
            self.name = "ben"
            self.playerstate = "gamestate"

    def create_bullet(self, name):
        return Bullet(self.rect.centerx+25, self.rect.centery-23, name)

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        
        self.bullet_group.update()
        self.bullet_group.draw(self.screen)
        # self.screen.blit(self.mask_image, self.rect)
        # pg.draw.rect(self.screen, "green", self.rect, 2)