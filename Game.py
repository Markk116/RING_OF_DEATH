import pygame as pg
import random as rnd
import math
from funct import *
from Classes import *
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
	score = 0

	cont = True #The continue varable
	clock = pg.time.Clock()
	fnames = os.listdir("./Images/")

	images = {}
	for img in fnames:
		if img[len(img)-3:len(img)].lower() == "png":
	 		image = pg.image.load("./Images/%s"%img).convert_alpha()
			images[img.replace(".png", "")] = image


	

	bg1 = Backround(images["Space"], 0,screen)
	bg2 = Backround(images["Space"], -1280,screen)
	bg3 = Backround(images["Backround"], 0,screen)

	bg4 = Backround(images["Pillar_bg"], 450,screen)
	bg5 = Backround(images["Pillar_sc"], 450,screen)
	bg6  = Backround(images["Astro"], 0 , screen)

	Player = Ship(pg.transform.scale(images["Ship"], (142, 64)), 200, 100, screen)
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
	    em = demon_spawn(difficulty, images ,"Spinner", screen)
	    if em != "BOOP":
	    	Hellspawn.append(em)
	    
	    for item in Hellspawn:
	    	if item.x<0:
	    		Hellspawn.remove(item)
	    if difficulty == 700:
	  	Hellspawn.append(demon_spawn(difficulty, images, "BOSS", screen))    
	   	
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
	    			if proj.form == "Pellet":
		    			Player.projectiles.remove(proj)
		    			Player.score +=1
	    			if scum.form == "BOSS":
	    				Player.weapon = "Laser"
	    				Player.score +=12
	    			Hellspawn.remove(scum)

	    for scum in Hellspawn:
	    	if Player.coll(scum): cont = False

	    # --- Drawing Code ---
	    bg1.move_render() #These are the moving stars
	    bg2.move_render()

	    bg6.move_render()

	    bg4.still_render()#central pillar
	    bg5.crop_render(450,770, vx = 1)#scrollpillar

	    bg3.still_render()
	    Player.render()

	    for item in Hellspawn:
	    	item.render((Player.x, Player.y))

		# --- Update Screen
	    pg.display.flip()
	   
	    # --- Max FPS: 120
	    clock.tick(30)


	pg.quit() #RIP </3

