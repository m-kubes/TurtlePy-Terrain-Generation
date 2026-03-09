import turtle
from tile_creator import *
from tile_colors import tiles


drawer = TileDrawer(100, 2, True, 2)
drawer.draw_tile(1,0,0,tiles['sand'])
drawer.draw_tile(0,0,1,tiles['stone'])
drawer.draw_tile(0,0,0,tiles['grass'])
drawer.draw_tile(0,1,0,tiles['tree'])
turtle.done()