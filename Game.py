import pygame as pg
import random as rnd
import math
from funct import *
import os

def main():
	# Define some colours
	BLACK    = (   0,   0,   0)
	WHITE    = ( 255, 255, 255)
	GREEN    = (   0, 255,   0)
	RED      = ( 255,   0,   0)

	pg.init()

	#Basic setup 
	size = (1280,720)
	screen = pg.display.set_mode(size)
	pg.display.set_caption("Welcome to the ring of death!")
	Laser = pg.Surface((600,10))
	fill_gradient(Laser, (0,255,255), (255,255,255))
	score = 0

	cont = True #The continue varable
	clock = pg.time.Clock()
	fnames = os.listdir("./Images/")

	images = {}
	for img in fnames:
		if img[len(img)-3:len(img)].lower() == "png":
	 		image = pg.image.load("./Images/%s"%img).convert_alpha()
			images[img.replace(".png", "")] = image


	class Backround(object):
		"""A Class to handle the (scolling) backround"""
	 	def __init__(self, img, x):
	 		self.img = img
	 		self.x = x
	 	def move_render(self):
	 		self.x-=10
	 		if self.x<=-1280:
	 			self.x = +1280
	 		screen.blit(self.img, (self.x, 0))
	 	def still_render(self):
	 		screen.blit(self.img, (self.x, 0))

	class Ship(object):
		"""To handle the player ship"""
		def __init__(self, img, x, y ):
			self.x 			= x
			self.y 			= y
			self.img 		= img
			self.rect 		= self.img.get_rect()
			self.rect.left 	= self.x
			self.rect.top 	= self.y
			self.vx			= 0
			self.vy			= 0
			self.weapon		= "Pellet" #Either pellet or laser
			self.projectiles= [] #Format [x, y]
			self.cooldown	= 0


		def render(self):
			self.rect.left 	= self.x
			self.rect.top 	= self.y
			self.x += self.vx
			self.y += self.vy
			self.cooldown +=1
			screen.blit(self.img, (self.x, self.y))
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
			if self.weapon == "Pellet" and self.cooldown>15:
				self.cooldown = 0
				self.projectiles.append(Projectile(self.x, self.y, "Pellet"))
			if self.weapon == "Laser" and self.cooldown>45:
				self.cooldown = 0
				self.projectiles.append(Projectile(self.x, self.y, "Laser"))

	class Projectile(object):
		"""A class to handle the projectiles"""
		def __init__(self, x, y, form):
			self.x = x+95
			self.y = y+60
			self.form = form
			self.rect = pg.Rect( (self.x, self.y), (8,8))
			if self.form == "Laser": self.rect = Laser.get_rect()

		def render(self):
			self.x +=35
			self.rect.left 	=self.x
			self.rect.top 	=self.y
			if self.form == "Pellet": pg.draw.circle(screen, RED, (self.x, self.y), 8 )
			elif self.form == 'Laser': screen.blit(Laser, (self.x, self.y))

		def coll(self, other):
			return self.rect.colliderect(other.rect)


	class Enemy(object):
		"""A class to handle the enemies"""
		def __init__(self,x,y, vx, vy,form, image):
			self.x 			=x
			self.y 			=y
			self.vx 		=vx
			self.vy 		=vy
			self.theta		=0
			self.form 		=form
			self.img 		=image
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
				screen.blit(self.imgT, (self.x, self.y))
				
			if self.form == "BOSS":
				plr_r = [player[0]-self.x,player[1]-self.y]
				self.x -=10
				if plr_r[1]>0: self.y +=5
				elif plr_r[1]<0: self.y -=5
				screen.blit(self.img, (self.x, self.y))

	def demon_spawn(difficulty, form):
		"""Calls demonspawn from the depth of the void"""
		if form !="BOSS":
			n=int(120 * math.exp(-300/difficulty))
			dn = rnd.randint(1,n) #this results in on average on enemy being spawned per four seconds
			if dn>=n: #but, difiiculty should step up every 10 seconds, by maybe 10%, so not every four but every 3.6s
				return Enemy(1280, rnd.randint(0,720), -rnd.randint(0,10),-rnd.randint(0,10), form, images[form])
			else: return "BOOP"
		elif form == "BOSS":
			return Enemy(1280, 360, 0,0, "BOSS", images["BOSS"])

	bg1 = Backround(images["Space"], 0)
	bg2 = Backround(images["Space"], -1280)
	bg3 = Backround(images["Backround"], 0)

	Player = Ship(pg.transform.scale(images["Ship"], (142, 64)), 200, 100)
	difficulty = 250
	Hellspawn = []
	Running = False

	while cont:
		# --- Main Event Loop ---
	    for event in pg.event.get():
	        if event.type ==  pg.QUIT:
	            cont = False

	    # --- Game Logic ---
	    difficulty +=1
	    em = demon_spawn(difficulty, "Spinner")
	    if em != "BOOP":
	    	Hellspawn.append(em)
	    
	    for item in Hellspawn:
	    	if item.x<0:
	    		Hellspawn.remove(item)
	    if difficulty == 700:
	  	Hellspawn.append(demon_spawn(difficulty, "BOSS"))    
	   	
	    if event.type == pg.KEYDOWN:
	    	if event.key == pg.K_LEFT and Player.vx>=-20:
	            Player.vx -=7
	        if event.key == pg.K_RIGHT and Player.vx<=20:
	            Player.vx +=7
	        if event.key == pg.K_UP and Player.vy >=-20:
	        	Player.vy -= 7
	        if event.key == pg.K_DOWN and Player.vy <=20:
	        	Player.vy += 7
	        if event.key == pg.K_SPACE:
	        	Player.shoot()
	    
	    #Now, collision dececton:
	    #Detect collision for player with hellspawn, and player.projectiles with hellspawn
	    for proj in Player.projectiles:
	    	for scum in Hellspawn:
	    		if proj.coll(scum): 
	    			Player.projectiles.remove(proj)
	    			if scum.form == "BOSS":
	    				Player.weapon = "Laser"
	    			Hellspawn.remove(scum)

	    for scum in Hellspawn:
	    	if Player.coll(scum): cont = False

	    # --- Drawing Code ---
	    bg1.move_render()
	    bg2.move_render()
	    bg3.still_render()
	    Player.render()

	    for item in Hellspawn:
	    	item.render((Player.x, Player.y))

		# --- Update Screen
	    pg.display.flip()
	   
	    # --- Max FPS: 120
	    clock.tick(30)


	pg.quit() #RIP </3

