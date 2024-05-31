import pygame as pg
from sys import exit
from timer import Timer

pg.init()

display_surface = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
font = pg.font.Font(None, 50)

# In_Build Timers
# timer_event = pg.event.custom_type()
# pg.time.set_timer(timer_event, 2000)

show_text = False

def toggle_var():
    global show_text
    show_text = not show_text

simple_timer = Timer(1000, autostart= True)
repeat_timer = Timer(1500, autostart= True, repeat= True, func= toggle_var)

while True:
    dt = clock.tick() / 1000
    for event in pg.event.get():
        if ((event.type == pg.QUIT) or 
            (event.type == pg.KEYDOWN and 
             event.key == pg.K_ESCAPE)):
            
            pg.quit()
            exit()

        # if event.type == timer_event:
        #     print("Inbuild Timer")

    simple_timer.update()
    repeat_timer.update()
    
    display_surface.fill("black")
    if not (simple_timer.active):
        text_surf = font.render("1 Second has passed", False, "Green")
        display_surface.blit(text_surf, (0, 0))

    if show_text:
        text_surf = font.render("Timer is ON", False, "Red")
        text_rect = text_surf.get_rect(topleft = (0, 300))
        pg.draw.rect(display_surface, "Black", text_rect)
        display_surface.blit(text_surf, text_rect)
    else:
        text_surf = font.render("Timer is OFF", False, "Black")
        text_rect = text_surf.get_rect(topleft = (200, 300))
        pg.draw.rect(display_surface, "Red", text_rect)
        display_surface.blit(text_surf, text_rect)

    pg.display.update()