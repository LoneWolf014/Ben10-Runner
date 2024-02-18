import math
from Resources import *

# Parallax Class
class Parallax:
    def __init__(self,screen, img, s_speed, x, y):
        self.img = img
        self.speed = s_speed
        self.screen = screen
        
        # utilities
        self.img_width = self.img.get_width()
        self.tile = math.ceil(W_Width/self.img_width) + 2
        # + 2 is like the padding or offset for smooth transition
        self.scroll = 0
        self.x = x
        self.y = y

    def update(self):
        self.scroll += self.speed
        if(abs(self.scroll) > self.img_width):
            self.scroll = 0
        
        self.draw()

    def draw(self):
        for i in range(self.tile):
            self.x = (i * self.img_width) - self.scroll
            self.screen.blit(self.img, (self.x, self.y))

class Ground:
    def __init__(self,screen, img, s_speed, x, y):
        self.img = img
        self.speed = s_speed
        self.screen = screen
        
        # utilities
        self.img_width = self.img.get_width()
        self.img_height = self.img.get_height()
        self.tile = math.ceil(W_Width/self.img_width) + 2
        # + 2 is like the padding or offset for smooth transition
        self.scroll = 0
        self.x = x
        self.y = (W_Height - self.img_height)

    def update(self):
        self.scroll += self.speed
        if(abs(self.scroll) > self.img_width * 5):
            self.scroll = 0
        
        self.draw()

    def draw(self):
        for i in range(self.tile * 5):
            self.x = (i * self.img_width) - self.scroll
            self.screen.blit(self.img, (self.x, self.y))