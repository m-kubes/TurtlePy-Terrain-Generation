import turtle

# get sort order
# things with higher sort orders are rendered last (on top of everything else)
def sort_order(tile, ignoreType=False):
	if not ignoreType:
		match tile[3]['type']:
			case 'tree':
				return (sort_order(tile, True) + sort_order((tile[0],tile[1]+1,tile[2],tile[3]), True)) / 2

	return ((tile[0] + tile[2]) * -1) + tile[1]
		

# merge sort that fixes the sorting order for rendering
def sort_to_render(arr):
    if len(arr) <= 1:
        return arr
    
    # Divide
    mid = len(arr) // 2
    left = sort_to_render(arr[:mid])
    right = sort_to_render(arr[mid:])
    
    # Merge
    return merge(left, right)

# for sort_to_render
def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if sort_order(left[i]) < sort_order(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


class TileDrawer():
	def __init__(self, tile_size, outline_width=2, is_animated=True, speed=0):
		self.tile_size = tile_size
		self.t = turtle.Turtle()
		self.t.speed(speed)
		self.t.width(outline_width)	
		screen = turtle.Screen()
		screen.tracer(1 if is_animated else 0)

	# moves turtle without drawing a line
	def setpos_noline(self, x,y):
		t = self.t
		t.up()
		t.setpos(x,y)
		t.down()

	# rectange
	def draw_rect(self, size_x, size_y):
		t = self.t
		x, y = t.pos()
		self.setpos_noline(x - 0.5 * size_x, y + 0.5 * size_y)
		t.begin_fill()
		t.goto(x - 0.5 * size_x, y - 0.5 * size_y)
		t.goto(x + 0.5 * size_x, y - 0.5 * size_y)
		t.goto(x + 0.5 * size_x, y + 0.5 * size_y)
		t.goto(x - 0.5 * size_x, y + 0.5 * size_y)
		t.end_fill()

	# converts x,y coordinates to an isometric grid
	def to_isometric(self, x, y, z, tile_size):
		iso_x = x * (0.5 * tile_size) + z * (-0.5 * tile_size)
		iso_y = x * (0.25 * tile_size) + z * (0.25 * tile_size) + y * (0.5 * tile_size)
		return iso_x, iso_y

	# draws the top of a tile
	def draw_top_tile_face(self, size):
		t = self.t
		t.begin_fill()
		t.goto(t.pos()[0] + (0.5 * size), t.pos()[1] + (0.25 * size))
		t.goto(t.pos()[0] + (-0.5 * size), t.pos()[1] + (0.25 * size))
		t.goto(t.pos()[0] + (-0.5 * size), t.pos()[1] + (-0.25 * size))
		t.goto(t.pos()[0] + (0.5 * size), t.pos()[1] + (-0.25 * size))
		t.end_fill()

	# draws the right or left side of a tile
	def draw_side_tile_face(self, size_x, size_y, side):
		t = self.t
		t.begin_fill()
		t.goto(t.pos()[0], t.pos()[1] + (-0.5 * size_y))
		t.goto(t.pos()[0] + (-side * 0.5 * size_x), t.pos()[1] + (0.25 * size_x))
		t.goto(t.pos()[0], t.pos()[1] + (0.5 * size_y))
		t.goto(t.pos()[0] + (side * 0.5 * size_x), t.pos()[1] + (-0.25 * size_x))
		t.end_fill()

	# tree leaves bro
	def draw_tree_leaves(self, size):
		t = self.t
		x, y = t.pos()
		t.begin_fill()
		self.setpos_noline(x - 0.4 * size, y)
		t.goto(x + 0.4 * size, y)
		t.goto(x + 0.2 * size, y + 0.5 * size)
		t.goto(x + 0.325 * size, y + 0.5 * size)
		t.goto(x, y + 1.25 * size)
		t.goto(x - 0.325 * size, y + 0.5 * size)
		t.goto(x - 0.2 * size, y + 0.5 * size)
		t.goto(x - 0.4 * size, y)
		t.end_fill()


	# all the math and color stuff needed to draw a tile
	# currently only accounts for tile types 'basic', 'grasstop', and 'tree'
	# this does fortunatly allow for modular tile colors so you can go into tile_colors.py and make whatever tile u want
	def draw_tile(self,x,y,z,tile):
		t = self.t
		t.seth(0)
		x, y = self.to_isometric(x,y,z,self.tile_size)
		self.setpos_noline(x,y)

		match tile['type']:
			case 'basic':
				# draw top face
				t.color(tile['outline_color'])
				t.fillcolor(tile['top_face_color'])
				self.draw_top_tile_face(self.tile_size)

				# draw left side face
				t.fillcolor(tile['left_face_color'])
				self.draw_side_tile_face(self.tile_size, self.tile_size, 1)

				# draw right side face
				t.fillcolor(tile['outline_color'])
				self.draw_side_tile_face(self.tile_size, self.tile_size, -1)
			case 'grasstop':
				# draw top face
				t.color(tile['top_outline_color'])
				t.fillcolor(tile['top_face_color'])
				self.draw_top_tile_face(self.tile_size)

				# draw top left side face
				t.fillcolor(tile['top_face_color'])
				self.draw_side_tile_face(self.tile_size, self.tile_size * 0.3, 1)

				# draw top right side face
				t.fillcolor(tile['top_outline_color'])
				self.draw_side_tile_face(self.tile_size, self.tile_size * 0.3, -1)

				# move cursor down to draw bottom part
				self.setpos_noline(x,y - 0.15 * self.tile_size)

				# draw bottom left face
				t.color(tile['bottom_outline_color'])
				t.fillcolor(tile['bottom_side_color'])
				self.draw_side_tile_face(self.tile_size, self.tile_size * 0.7, 1)

				# draw bottom right face
				t.fillcolor(tile['bottom_outline_color'])
				self.draw_side_tile_face(self.tile_size, self.tile_size * 0.7, -1)
			case 'tree':
				# trunk
				t.color(tile['trunk_outline_color'])
				t.fillcolor(tile['trunk_color'])
				self.setpos_noline(x, y - 0.125 * self.tile_size)
				self.draw_rect(0.25 * self.tile_size, 0.25 * self.tile_size)

				# part of trunk in shadow from the leaves
				t.color(tile['trunk_shaded_outline_color'])
				t.fillcolor(tile['trunk_shaded_color'])
				self.setpos_noline(x, y + 0.125 * self.tile_size)
				self.draw_rect(0.25 * self.tile_size, 0.25 * self.tile_size)

				# leaves
				t.color(tile['leaves_outline_color'])
				t.fillcolor(tile['leaves_color'])
				self.setpos_noline(x,y + 0.125 * self.tile_size)
				self.draw_tree_leaves(self.tile_size)
