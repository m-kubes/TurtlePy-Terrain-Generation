import turtle
import random
import math
import time
from perlin_noise import PerlinNoise
from tile_colors import tiles
from tile_creator import *
from noise_generation import *

# execution time
start_time = time.time()

# terrain configuration
# very low width and height levels make terrain really bad
width, height = 50, 50
height_variance = 9
tree_chance = 0.45

# places this tile if GREATER THAN the float
# water always places below the lowest threshold
tile_thresholds = {
	'peak': 0.7,
	'mountain': 0.645,
	'plains': 0.44,
	'beach': 0.4
}

seed_value = random.randint(1, 1000000)
biome_noise = PerlinNoise(octaves=4, seed=seed_value)
forest_noise = PerlinNoise(octaves=3, seed=seed_value + 123)


# make visible edges fatter
def make_edge(x, z, fake_y, tile):
	if x == 0 or z == 0:
		for i in range(1, fake_y):
			scene_tiles.append((x,y-i,z,tile))



# create list of tiles
scene_tiles = []
for x in range (height):
	for z in range(width):
		# get noise values and make them between 0 and 1
		biome_noise_value = (biome_noise([x/height, z/width]) + 1) / 2
		forest_noise_value = (forest_noise([x/height, z/width]) + 1) / 2

		# get y value of tile from noise
		# this also centers the terrain on the screen
		fake_y = max(math.floor(biome_noise_value * height_variance), 3)
		y = fake_y - (height / 1.5)

		# get type of tile from noise values
		# also tweaks y values to make mountains a little taller
		tile = None
		if biome_noise_value > tile_thresholds['peak']:
			tile = tiles['dark_stone']
			y += 2
			scene_tiles.append((x,y-1,z,tile))
			scene_tiles.append((x,y-2,z,tile))

			make_edge(x,z,fake_y + 2,tiles['dark_stone'])

		elif biome_noise_value > tile_thresholds['mountain']:
			tile = tiles['stone']
			y += 1
			scene_tiles.append((x,y-1,z,tile))

			make_edge(x,z,fake_y + 1,tiles['stone'])

		elif biome_noise_value > tile_thresholds['plains']:
			tile = tiles['grass']

			# place trees in forests
			if forest_noise_value < 0.5 and random.random() < tree_chance:
				scene_tiles.append((x,y+1,z,tiles['tree']))

			# account for water gap when going from grass straight to water
			if biome_noise_value < 0.46:
				scene_tiles.append((x,y-1,z,tiles['dirt']))

			make_edge(x,z,fake_y,tiles['dirt'])

		elif biome_noise_value > tile_thresholds['beach']:
			tile = tiles['sand']
			make_edge(x,z,fake_y,tiles['sand'])
		else:
			tile = tiles['water']
			make_edge(x,z,fake_y,tiles['full_water'])

		scene_tiles.append((x,y,z,tile))


# makes sure sorting orders are correct
scene_tiles = sorted(scene_tiles, key=lambda tile: sort_order(tile))


# create drawer (tile_creator.py)
drawer = TileDrawer(1200/((width + height) / 2), 55/((width + height) / 2.0), False)
turtle.bgcolor('#add8e6')


for tile in scene_tiles:
	drawer.draw_tile(tile[0],tile[1],tile[2],tile[3])

print('\nRendered {} tiles in {} seconds'.format(len(scene_tiles), time.time() - start_time))

turtle.done()