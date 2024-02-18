import pygame as pg
from sys import exit
from Resources import *
from Environment import *
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
    P_Layers.append(Parallax(screen, image, i+1, 0, 0))

    # Ground
ground = pg.image.load("Graphics/BG/ground.png").convert_alpha()
ground_height = ground.get_height()
ground_layer = Ground(screen, ground, 4, 0, 0)
# .................................................................. #
def BG_update():
    screen.blit(BG_0, (0, 0))
    for index, layer in enumerate(P_Layers):
        layer.update()

    ground_layer.update()
# .................................................................. #
# ------------------------------------------------------------------ #
# -- Mechadroids --------------------------------------------------- #
mecha = pg.image.load("graphics/mechadroid/mech3.png").convert_alpha()
mecha_x = 700
mecha_y = (W_Height - ground_height) + 10
mech_rect = mecha.get_rect(midbottom = (mecha_x, mecha_y))
# ------------------------------------------------------------------ #
# -- Player -------------------------------------------------------- #
player_surf = pg.image.load("Graphics/Ben/Walk/1.png").convert_alpha()
player_x = 50
player_y = (W_Height - ground_height) + 10
player_rect = player_surf.get_rect(midbottom = (player_x, player_y))

player_gravity = 0
# ------------------------------------------------------------------ #
start_time = 0
score = 0

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

# Functions
def display_score():
    current_time = int(pg.time.get_ticks()/1000) - start_time
    score_surf = test_font.render(f"Score : {current_time}", True, "Red")
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)

    return current_time

# Main Loop
while(run):
    for event in pg.event.get():
        if ((event.type == pg.QUIT) or
             (event.type == pg.KEYDOWN and
               event.key == pg.K_ESCAPE)):
            run = False
            exit()

        if game_active:
            if event.type == pg.KEYDOWN and player_rect.bottom >= (W_Height-ground_height + 10):
                if event.key == pg.K_SPACE:
                    player_gravity = -30

            if event.type == pg.MOUSEBUTTONDOWN and player_rect.bottom >= (W_Height-ground_height + 10):
                if player_rect.collidepoint(event.pos):
                    player_gravity = -30
        else:
             if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                 start_time = int(pg.time.get_ticks()/1000)
                 game_active = True
                 mech_rect.left = 800

    if game_active:
        # BG
        screen.fill((0, 0, 0))
        BG_update()

        mech_rect.right -= 5
        if mech_rect.right < -200: mech_rect.right = 1000

        # Mechadroids
        screen.blit(mecha, mech_rect)
        pg.draw.rect(screen, "red", mech_rect, 2)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity

        if player_rect.bottom >= (W_Height-ground_height): player_rect.bottom = (W_Height-ground_height) + 10
        screen.blit(player_surf, player_rect)
        pg.draw.rect(screen, "GREEN", player_rect, 2)

        # Score
        score = display_score()

        if player_rect.colliderect(mech_rect):
            game_active = False
    else:
        screen.fill((0, 0, 0))
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