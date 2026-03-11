import turtle
from tile_creator import *
from tile_colors import tiles


drawer = TileDrawer(100, 2, True, 5)
drawer.draw_tile(1,0,0,tiles['sand'])
drawer.draw_tile(0,0,2,tiles['stone'])
drawer.draw_tile(0,1,2,tiles['dark_stone'])
drawer.draw_tile(0,-1,1,tiles['full_water'])
drawer.draw_tile(0,0,1,tiles['water'])
drawer.draw_tile(0,-1,0,tiles['dirt'])
drawer.draw_tile(0,0,0,tiles['grass'])
drawer.draw_tile(0,1,0,tiles['tree'])
turtle.done()