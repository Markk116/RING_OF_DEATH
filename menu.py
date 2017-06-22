# -*- coding: latin-1 -*-
import sys
import pygame as pg
import Game as rd
from Classes import GameMenu

pg.init()

screen = pg.display.set_mode((1280,720), 0, 32)
points = ("Start", "Quit")
#Ringofdeath.main()
funcs = {"Hold my Beer aka Start": rd.main,

         "Gimme my beer back! aka quit": sys.exit}
pg.display.set_caption("Best Game Menu 4 eva! <3")
menu = GameMenu(screen, funcs.keys(), funcs)
menu.run()