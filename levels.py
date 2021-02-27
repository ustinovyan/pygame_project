from settings import *

level = [
    "                         ",
    "                         ",
    "                         ",
    "                         ",
    "                         ",
    "                         ",
    "                          ",
    "                  ####### ",
    "                         ",
    "                          ",
    "                         ",
    "                          ",
    "     c       c            ",
    "#########################",]


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = image.load("data/blocks/platform1.png")
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
