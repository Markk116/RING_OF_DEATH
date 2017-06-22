# Houses all the Classes
import pygame as pg
import random as rnd
import math
import sys
from funct import *

PURPLE 	= ( 150	,     0	,  75)
FAB 	= (  75	,   255	, 255)
WHITE 	= ( 255	,   255	, 255)
LRED 	= ( 100	,     0	,   0)
DRED 	= ( 200	,     0	,   0)
BLACK 	= (   0	,     0	,   0)
GREEN   = (   0	,   255	,   0)
RED     = ( 255	,     0	,   0)


#All the classes from the game file
class Backround(object):
	"""A Class to handle the (scolling) backround"""
 	def __init__(self, img, x, screen):
 		self.img 		= img
 		self.x 			= x
 		self.x_anchor 	= x
 		self.screen 	= screen
 		self.rect 	= self.img.get_rect()
 	def move_render(self, vx=10, x_bound=1280):
 		self.x-=vx
 		if self.x<=-x_bound:
 			self.x = x_bound
 		self.screen.blit(self.img, (self.x, 0))
 	def still_render(self):
 		self.screen.blit(self.img, (self.x, 0))
 	def crop_render(self, x_min , x_max, vx = 10):
 		self.x +=vx
 		if self.x <=x_min: self.x += x_max-x_min
 		elif self.x >=x_max: self.x -= x_max-x_min
 		self.crop_img = self.img.subsurface(self.x - x_min ,0,x_max-x_min,self.rect[3])
 		self.screen.blit(self.crop_img, (self.x_anchor, 0))

class Ship(object):
	"""To handle the player ship"""
	def __init__(self, img, x, y, screen):
		self.x 			= x
		self.y 			= y
		self.screen		= screen
		self.img 		= img
		self.rect 		= self.img.get_rect()
		self.rect.left 	= self.x
		self.rect.top 	= self.y
		self.vx			= 0
		self.vy			= 0
		self.weapon		= "Pellet" #Either pellet or laser
		self.projectiles= [] #Format [x, y]
		self.cooldown	= 0
		self.score 		= 0



	def render(self):
		self.rect.left 	= self.x
		self.rect.top 	= self.y
		self.x += self.vx
		self.y += self.vy
		self.cooldown +=1
		self.screen.blit(self.img, (self.x, self.y))
		if self.x>= 640:  self.x, self.vx = 640, 0
		if self.y>= 688:  self.y, self.vy = 688, 0
		if self.x<= 5: 	  self.x, self.vx = 5, 0
		if self.y<= 5:    self.y, self.vy = 5, 0
		if len(self.projectiles)>0:
			for proj in self.projectiles:
				if proj.x>1280:
					self.projectiles.remove(proj)
				proj.render()
	def coll(self, other):
		return self.rect.colliderect(other.rect)

	def shoot(self):
		if self.weapon == "Pellet" and self.cooldown>(15-self.score):
			self.cooldown = 0
			self.projectiles.append(Projectile(self.x, self.y, "Pellet",self.screen))
		if self.weapon == "Laser" and self.cooldown>(45-self.score):
			self.cooldown = 0
			self.projectiles.append(Projectile(self.x, self.y, "Laser", self.screen))

class Projectile(object):
	"""A class to handle the projectiles"""
	def __init__(self, x, y, form, screen):
		self.x 		= x+95
		self.y 		= y+60
		self.screen = screen
		self.form 	= form
		self.rect 	= pg.Rect( (self.x, self.y), (8,8))
		self.Laser  = pg.Surface((600,10))
		if self.form == "Laser": self.rect = self.Laser.get_rect()
		fill_gradient(self.Laser, (0,255,255), (255,255,255))


	def render(self):
		self.x +=35.
		self.rect.left 	=self.x
		self.rect.top 	=self.y
		if self.form == "Pellet": pg.draw.circle(self.screen, RED, (int(self.x), int(self.y)), 8 )
		elif self.form == 'Laser': self.screen.blit(self.Laser, (self.x, self.y))

	def coll(self, other):
		return self.rect.colliderect(other.rect)


class Enemy(object):
	"""A class to handle the enemies"""
	def __init__(self,x,y, vx, vy,form, image,screen):
		self.x 			=x
		self.y 			=y
		self.vx 		=vx
		self.vy 		=vy
		self.theta		=0
		self.form 		=form
		self.img 		=image
		self.screen 	=screen
		self.rect 		=self.img.get_rect()
		self.rect.left 	=self.x
		self.rect.top 	=self.y
		self.imgT		=self.img

	def render(self, player = (0,0)):
		self.rect.left 	=self.x
		self.rect.top 	=self.y
		if self.y>= 688:  self.y, self.vy = 688, -self.vy
		if self.y<= 5:    self.y, self.vy = 5, -self.vy

		if self.form == "Spinner": 
			self.theta +=60
			self.imgT = pg.transform.rotate(self.img,self.theta)
			self.x += self.vx
			self.y += self.vy
			self.screen.blit(self.imgT, (self.x, self.y))
			
		if self.form == "BOSS":
			plr_r = [player[0]-self.x,player[1]-self.y]
			self.x -=10
			if plr_r[1]>0: self.y +=5
			elif plr_r[1]<0: self.y -=5
			self.screen.blit(self.img, (self.x, self.y))

def demon_spawn(difficulty,images ,form, screen):
	"""Calls demonspawn from the depth of the void"""
	if form !="BOSS":
		n=int(120 * math.exp(-300/difficulty))
		dn = rnd.randint(1,n) #this results in on average on enemy being spawned per four seconds
		if dn>=n: #but, difiiculty should step up every 10 seconds, by maybe 10%, so not every four but every 3.6s
			return Enemy(1280, rnd.randint(0,720), -rnd.randint(0,10),-rnd.randint(0,10), form,images[form], screen)
		else: return "BOOP"
	elif form == "BOSS":
		return Enemy(1280, 360, 0,0, "BOSS", images["BOSS"], screen)

# all the classes from the menu file

class MenuBackground(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image_file)
        self.image = pg.transform.scale(self.image, (1280, 720))
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
        self.BackGround = MenuBackground('./Images/ringoffire.jpg', [0, 0])
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