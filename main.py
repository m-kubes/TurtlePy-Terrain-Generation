import turtle
import random
import math
from perlin_noise import PerlinNoise
from tile_colors import tiles
from tile_creator import *
from noise_generation import *


# terrain configuration
width, height = 40, 40
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


# create list of tiles
scene_tiles = []
for x in range (height):
	for z in range(width):
		# get noise values and make them between 0 and 1
		biome_noise_value = (biome_noise([x/height, z/width]) + 1) / 2
		forest_noise_value = (forest_noise([x/height, z/width]) + 1) / 2

		# get y value of tile from noise
		# this also centers the terrain on the screen
		y = max(math.floor(biome_noise_value * height_variance), 3) - (height / 2)

		# get type of tile from noise values
		# also tweaks y values to make mountains taller
		tile = None
		if biome_noise_value > tile_thresholds['peak']:
			tile = tiles['dark_stone']
			y += 2
			scene_tiles.append((x,y-1,z,tile))
			scene_tiles.append((x,y-2,z,tile))

		elif biome_noise_value > tile_thresholds['mountain']:
			tile = tiles['stone']
			y += 1
			scene_tiles.append((x,y-1,z,tile))

		elif biome_noise_value > tile_thresholds['plains']:
			tile = tiles['grass']

			if forest_noise_value < 0.5 and random.random() < tree_chance:
				scene_tiles.append((x,y+1,z,tiles['tree']))

		elif biome_noise_value > tile_thresholds['beach']:
			tile = tiles['sand']
		else:
			tile = tiles['water']

		scene_tiles.append((x,y,z,tile))

# makes sure sorting orders are correct
scene_tiles = sort_to_render(scene_tiles)
drawer = TileDrawer(20, 0.5, False)

for tile in scene_tiles:
	drawer.draw_tile(tile[0],tile[1],tile[2],tile[3])

turtle.done()