from perlin_noise import PerlinNoise
import random
import os


def write_noise(width, height, file_extension, seed=random.randint(1, 1000000)):
	noise = PerlinNoise(octaves=4, seed=seed)
	noise_values = [noise([x/height, z/width]) for x in range(width) for z in range(height)]

	file_path = 'templateNoise/{}x{}/noise{}'.format(width, height, file_extension)
	directory = os.path.dirname(file_path)

	if not os.path.exists(directory):
		os.mkdir('templateNoise/{}x{}'.format(width, height))

	with open(file_path, 'w') as file:
		for value in noise_values:
			file.write(str(value) + '\n')


def get_noise(width, height):
	directory = 'templateNoise/{}x{}'.format(width, height)
	entries = os.listdir(directory)

	files = [entry for entry in entries if os.path.isfile(os.path.join(directory, entry))]
	random_filename = random.choice(files)

	with open(os.path.join(directory, random_filename)) as file:
		noise = [float(value.strip()) for value in file.readlines()]

	print(noise)


