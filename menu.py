# -*- coding: latin-1 -*-

import sys
import pygame as pg
import Ringofdeath as rd

pg.init()

PURPLE = (150, 0, 75)
FAB = (55, 255, 255)
WHITE = (255, 255, 255)
LRED = (150, 0, 0)
DRED = (200, 0, 0)
BLACK = (0, 0, 0)


class Backround(object):
    """A Class to handle the (scolling) backround"""
    def __init__(self, img, x):
        self.img = img
        self.x = x

    def move_render(self):
        self.x -= 10
        if self.x <= -1280:
            self.x = +1280
        screen.blit(self.img, (self.x, 0))

    def still_render(self):
        screen.blit(self.img, (self.x, 0))


class Background(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class MenuPoint(pg.font.Font):
    def __init__(self, text, font=None, schrift_size=60,
                 schrift_color=LRED, (xpos, ypos)=(0, 0)):
        pg.font.Font.__init__(self, font, schrift_size)
        self.text = text
        self.schrift_size = schrift_size
        self.schrift_color = schrift_color
        self.label = self.render(self.text, 1, self.schrift_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.dimensions = (self.width, self.height)
        self.xpos = xpos
        self.ypos = ypos
        self.position = xpos, ypos

    def set_schrift_color(self, rgb):
        self.schrift_color = rgb
        self.label = self.render(self.text, 1, self.schrift_color)

    def mouse_point(self, (posx, posy)):
        if (posx <= self.xpos + self.width and posx >= self.xpos) and \
                (posy <= self.ypos + self.height and posy >= self.ypos):
            return True
        return False

    def set_pos(self, x, y):
        self.position = (x, y)
        self.xpos = x
        self.ypos = y


class GameMenu():
    def __init__(self, screen, items, funcs, font=None, schrift_size=60,
                 schrift_color=LRED):
        self.BackGround = Background('ringoffire.jpg', [0, 0])
        # self.bg_color = background_color
        self.clock = pg.time.Clock()
        self.screen = screen
        self.width = self.screen.get_rect().width
        self.height = self.screen.get_rect().height
        self.funcs = funcs
        self.items = []
        for index, item in enumerate(items):
            this_item = MenuPoint(item, font, schrift_size, schrift_color)
            h = len(items) * this_item.height
            xpos = (self.width / 2) - (this_item.width / 2)
            ypos = (self.height / 2) - (h / 2) + ((index * 2) + index * this_item.height)

            this_item.set_pos(xpos, ypos)
            self.items.append(this_item)

        self.mouse_vis = True
        self.select_item = None

    def run(self):
        mainloop = True
        while mainloop:
            # refresh rate
            self.clock.tick(30)

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.BackGround.image, self.BackGround.rect)

            mpos = pg.mouse.get_pos()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    mainloop = False
                if event.type == pg.KEYDOWN:
                    self.mouse_vis = False
                    self.tast_auswahl(event.key)
                if event.type == pg.MOUSEBUTTONDOWN:
                    for item in self.items:
                        if item.mouse_point(mpos):
                            self.funcs[item.text]()

            if pg.mouse.get_rel() != (0, 0):
                self.mouse_vis = True
                self.select_item = None

            self.set_mouse_vis()

            # self.screen.fill(self.bg_color)

            for item in self.items:
                if self.mouse_vis:
                    self.mouse_select(item, mpos)
                self.screen.blit(item.label, item.position)

            # movingships???




            pg.display.flip()

    def mouse_select(self, item, mpos):
        if item.mouse_point(mpos):
            item.set_schrift_color(DRED)
            item.set_bold(True)
        else:
            item.set_schrift_color(LRED)
            item.set_bold(False)

    def tast_auswahl(self, key):
        """
        Marks the MenuPoint chosen via up and down keys.
        """
        for item in self.items:
            # Return all to neutral
            item.set_bold(False)
            item.set_schrift_color(LRED)

        if self.select_item is None:
            self.select_item = 0
        else:
            # Find the chosen item
            if key == pg.K_UP and \
                            self.select_item > 0:
                self.select_item -= 1
            elif key == pg.K_UP and \
                            self.select_item == 0:
                self.select_item = len(self.items) - 1
            elif key == pg.K_DOWN and \
                            self.select_item < len(self.items) - 1:
                self.select_item += 1
            elif key == pg.K_DOWN and \
                            self.select_item == len(self.items) - 1:
                self.select_item = 0

        self.items[self.select_item].set_bold(True)
        self.items[self.select_item].set_schrift_color(DRED)

        # Finally check if Enter or Space is pressed
        if key == pg.K_SPACE or key == pg.K_RETURN:
            text = self.items[self.select_item].text
            self.funcs[text]()

    def set_mouse_vis(self):
        if self.mouse_vis:
            pg.mouse.set_visible(True)
        else:
            pg.mouse.set_visible(False)



screen = pg.display.set_mode((1280, 720), 0, 32)
points = ("Quit", "Dark Souls I is for Casuals", "Easymode")
# Ringofdeath.main()
funcs = {"Dark Souls I is for Casuals": rd.main,
         "Easymode": rd.main,
         "Quit": sys.exit}
pg.display.set_caption("Ring Of Death")
menu = GameMenu(screen, funcs.keys(), funcs)
menu.run()
