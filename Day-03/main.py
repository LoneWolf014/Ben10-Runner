import pygame as pg
from sys import exit
from random import randint, choice

from Resources import *
from Environment import *
from Player import Player

# <Target> -- Add Better Enemy Spawn Logic and Object Oriented the Game #

# Variables
Display_Width = W_Width
Display_Height = W_Height
run = True

pg.init()
screen = pg.display.set_mode((Display_Width, Display_Height))
pg.display.set_caption("BEN_10 RUN")
clock = pg.time.Clock()

test_font = pg.font.Font("Font/Technology.ttf", 50)
msg_font = pg.font.SysFont("OCR A Extended", 50)

# Game States
game_active = False

# Classes 
class Obstacle(pg.sprite.Sprite):
    def __init__(self, type):
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

class Alien(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pg.Surface((60, 60))
        self.image.fill("red")
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), ground_level))

    def update(self):
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x < 20:
            self.kill()
# Functions
def display_score():
    current_time = int(pg.time.get_ticks()/1000) - start_time
    score_surf = test_font.render(f"Score : {current_time}", True, "Red")
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)

    return current_time

def collision_sprites():
    if pg.sprite.spritecollide(player.sprite, obstacle_group, False):
        print("rectangles collided")
        if pg.sprite.spritecollide(player.sprite, obstacle_group, False, collided=pg.sprite.collide_mask):
            print("Masks Collided")
            pg.time.delay(1400)
            obstacle_group.empty()
            return False
    return True

def collision_objects():
    if pg.sprite.groupcollide(obstacle_group, alien_power, False, True):
        print("A Power Up has Spawned on Enemy... the Powerup has been Killed")

    if pg.sprite.spritecollide(player.sprite, alien_power, True):
        print("Player got the Power Up")
# ------------------------------------------------------------------ #
# Creating Background
    # Loading Background
BG_0 = pg.image.load(f"Graphics/BG/bg.png").convert_alpha()

    # Parallax Layers
BgLayers = []
for i in range(1, 5):
    image = pg.image.load(f"Graphics/BG/{i}.png").convert_alpha()
    BgLayers.append(image)

    # Loading Parallax
P_Layers = []
for i, image in enumerate(BgLayers):
    layer_speed = i+1
    P_Layers.append(Parallax(screen, image, layer_speed, 0, 0))

    # Ground
ground = pg.image.load("Graphics/BG/ground.png").convert_alpha()
ground_height = ground.get_height()
ground_level = (W_Height - ground_height) + 10
ground_speed = 4
ground_layer = Ground(screen, ground, ground_speed, 0, 0)
# .................................................................. #
def BG_update():
    screen.blit(BG_0, (0, 0))
    for index, layer in enumerate(P_Layers):
        layer.update()

    ground_layer.update()
# .................................................................. #
# ------------------------------------------------------------------ #
start_time = 0
score = 0

player = pg.sprite.GroupSingle()
player.add(Player(ground_level))

obstacle_group = pg.sprite.Group()

alien_power = pg.sprite.Group()

# GameOver State
Game_Over = pg.image.load("Graphics/GameOver.jpg").convert_alpha()
Game_Over = pg.transform.scale(Game_Over, (W_Width, W_Height))
Game_Over_rect = Game_Over.get_rect(topleft = (0, 0))

# Game Start State
BG = pg.image.load("Graphics/bg.jpg").convert_alpha()
BG = pg.transform.scale(BG, (W_Width, W_Height))
BG_rect = BG.get_rect(center = (W_Width/2, W_Height/2))

Ben_surf = pg.image.load("Graphics/stand.png").convert_alpha()
Ben_rect = Ben_surf.get_rect(center = (Display_Width/2, Display_Height/2))

game_message = msg_font.render("Press Space to Run", False, (0, 255, 0))
game_message_rect = game_message.get_rect(center = (400, 350))


# Timer
obstacle_timer = pg.USEREVENT + 1
pg.time.set_timer(obstacle_timer, 1500)

alien_timer = pg.USEREVENT + 2
pg.time.set_timer(alien_timer, 2000)

# Main Loop
while(run):
    for event in pg.event.get():
        if ((event.type == pg.QUIT) or
             (event.type == pg.KEYDOWN and
               event.key == pg.K_ESCAPE)):
            run = False
            exit()
        if not game_active:
             if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                start_time = int(pg.time.get_ticks()/1000)
                game_active = True

        # Update Timers
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["mechadroid", "mechadroid", "mechadroid", "drone"])))

            if event.type == alien_timer:
                print("Alien - Heat Blast")
                alien_power.add(Alien())

    if game_active:
        # BG
        screen.fill((0, 0, 0))
        BG_update()

        # Group
        game_active = collision_sprites()
        collision_objects()

        obstacle_group.update()
        alien_power.update()
        player.update()
        
        obstacle_group.draw(screen)
        alien_power.draw(screen)
        player.draw(screen)

        # Score
        score = display_score()

    else:
        screen.fill((0, 0, 0))
        player_gravity = 0

        if score == 0:
            title_surf = test_font.render("Run Ben Run !!", False, "Red")
            title_surf = pg.transform.scale2x(title_surf)
            title_rect = title_surf.get_rect(center = (400, 60))
        else:
            title_surf = test_font.render("You Lose", False, "Red")
            title_surf = pg.transform.rotozoom(title_surf, 0, 0.8)
            title_rect = title_surf.get_rect(midtop = (600, 10))

        score_message = test_font.render(f"Your Score : {score}", False, "red")
        score_message = pg.transform.rotozoom(score_message, 0, 0.8)
        score_message_rect = score_message.get_rect(center = (600, 90))

        if score == 0:
            screen.blit(BG, BG_rect)
            screen.blit(title_surf, title_rect)
            screen.blit(Ben_surf, Ben_rect)
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(Game_Over, Game_Over_rect)
            screen.blit(title_surf, title_rect)
            screen.blit(score_message, score_message_rect)

    pg.display.update()
    clock.tick(FPS)
pg.quit()