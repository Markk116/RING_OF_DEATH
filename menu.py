# -*- coding: latin-1 -*-

import sys
import pygame as pg
import Ringofdeath as rd
pg.init()

PURPLE = (150, 0, 75)
FAB = (55, 255, 255)
WHITE = (255, 255, 255)
LRED = (100, 0, 0)
DRED = (200, 0, 0)
BLACK = (0, 0, 0)

class Background(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class MenuPoint(pg.font.Font):
    def __init__(self, text, font=None, schrift_size=60,
                 schrift_color=LRED, (pos_x, pos_y)=(0, 0)):
        pg.font.Font.__init__(self, font, schrift_size)
        self.text = text
        self.schrift_size = schrift_size
        self.schrift_color = schrift_color
        self.label = self.render(self.text, 1, self.schrift_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.dimensions = (self.width, self.height)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = pos_x, pos_y

    def is_mouse_selection(self, (posx, posy)):
        if (posx >= self.pos_x and posx <= self.pos_x + self.width) and \
                (posy >= self.pos_y and posy <= self.pos_y + self.height):
            return True
        return False

    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y

    def set_schrift_color(self, rgb_code):
        self.schrift_color = rgb_code
        self.label = self.render(self.text, 1, self.schrift_color)


class GameMenu():
    def __init__(self, screen, items, funcs, background_color=PURPLE, font=None, schrift_size=60,
                 schrift_color=LRED):
        self.BackGround = Background('ringoffire.jpg', [0, 0])
        #self.bg_color = background_color
        self.clock = pg.time.Clock()
        self.screen = screen
        self.width = self.screen.get_rect().width
        self.height = self.screen.get_rect().height
        self.funcs = funcs
        self.items = []
        for index, item in enumerate(items):
            this_item = MenuPoint(item, font, schrift_size, schrift_color)

            # t_h: block height
            h = len(items) * this_item.height
            pos_x = (self.width / 2) - (this_item.width / 2)
            pos_y = (self.height / 2) - (h / 2) + ((index * 2) + index * this_item.height)

            this_item.set_position(pos_x, pos_y)
            self.items.append(this_item)

        self.mouse_is_visible = True
        self.select_item = None

    def set_mouse_visibility(self):
        if self.mouse_is_visible:
            pg.mouse.set_visible(True)
        else:
            pg.mouse.set_visible(False)

    def set_keyboard_selection(self, key):
        """
        Marks the MenuPoint chosen via up and down keys.
        """
        for item in self.items:
            # Return all to neutral
            item.set_italic(False)
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

        self.items[self.select_item].set_italic(True)
        self.items[self.select_item].set_schrift_color(DRED)

        # Finally check if Enter or Space is pressed
        if key == pg.K_SPACE or key == pg.K_RETURN:
            text = self.items[self.select_item].text
            self.funcs[text]()

    def set_mouse_selection(self, item, mpos):
        """Marks the MenuPoint the mouse cursor hovers on."""
        if item.is_mouse_selection(mpos):
            item.set_schrift_color(DRED)
            item.set_italic(True)
        else:
            item.set_schrift_color(LRED)
            item.set_italic(False)

    def run(self):
        mainloop = True
        while mainloop:
            # refresh rate
            self.clock.tick(50)

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.BackGround.image, self.BackGround.rect)

            mpos = pg.mouse.get_pos()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    mainloop = False
                if event.type == pg.KEYDOWN:
                    self.mouse_is_visible = False
                    self.set_keyboard_selection(event.key)
                if event.type == pg.MOUSEBUTTONDOWN:
                    for item in self.items:
                        if item.is_mouse_selection(mpos):
                            self.funcs[item.text]()

            if pg.mouse.get_rel() != (0, 0):
                self.mouse_is_visible = True
                self.select_item = None

            self.set_mouse_visibility()

            #self.screen.fill(self.bg_color)

            for item in self.items:
                if self.mouse_is_visible:
                    self.set_mouse_selection(item, mpos)
                self.screen.blit(item.label, item.position)

            pg.display.flip()


if __name__ == "__main__":
    # Creating the screen
    screen = pg.display.set_mode((760, 406), 0, 32)

    points = ("Start", "Quit")
    #Ringofdeath.main()
    funcs = {"Hold my Beer aka Start": rd.main,
             "Gimme my beer back! aka quit": sys.exit}

    pg.display.set_caption("Best Game Menu 4 eva! <3")
    menu = GameMenu(screen, funcs.keys(), funcs)
    menu.run()