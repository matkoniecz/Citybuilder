from numpy  import *
import sys, pygame, time
pygame.init()

size = screen_width, screen_height = 600, 600
screen = pygame.display.set_mode(size)

black = 0, 0, 0
red = 255, 0, 0
cursor_data = black

class PlayArea:
	def __init__(self, play_area_size, play_area_tile_size):
		self.play_area_size = play_area_size #in tiles
		self.play_area_tile_size = play_area_tile_size #in pixels
		self.play_area = []
		for i in range(0, play_area_size):
			self.play_area.append([red] * play_area_size)
	def press(self, x, y):
		x/=self.play_area_tile_size
		y/=self.play_area_tile_size
		self.play_area[x][y] = cursor_data
board = PlayArea(play_area_size=100, play_area_tile_size=100)

class Button:
	def __init__(self, position, size):
		self.size = size
		self.position = position
		self.surface = pygame.Surface(self.size)
		self.color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
		self.surface.fill(self.color)
	def is_pressed(self, x, y):
		if (self.position[0]) <= x <= (self.position[0] + self.size[0]):
			if (self.position[1]) <= y <= (self.position[1] + self.size[1]):
				return True
		return False

button_width = 100
button_height = 100
menu = []
for i in range(0, screen_height/button_height):
	menu.append(Button(position=(screen_width-button_width, button_height*i), size=(button_width, button_height)))


cursor_size = 25
cursor = Button(position=(screen_width-button_width+(button_width-cursor_size)/2, (button_width-cursor_size)/2), size=(cursor_size, cursor_size))
cursor.surface = pygame.image.load("rectangle.bmp")

#print pygame.mouse.get_rel()
touch = False
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			# Set the x, y positions of the mouse click
			x, y = event.pos
			for thing in menu:
				if thing.is_pressed(x, y):
					touch = not touch
					cursor_data = thing.color
			board.press(x, y)
	if touch:
		x, y = pygame.mouse.get_rel()
		cursor.position = (cursor.position[0]+x, cursor.position[1]+y)
	else:
		pygame.mouse.get_rel()
	screen.fill(black)
	dummy = (1, 1)
	for thing in menu:
		screen.blit(pygame.transform.scale(thing.surface, thing.size), pygame.Rect(thing.position, dummy))
	x_min = 0
	y_min = 0
	x_max = (screen_width-button_width)/board.play_area_tile_size
	y_max = screen_height/board.play_area_tile_size
	for x in range(x_min, x_max):
		for y in range(y_min, y_max):
			size = (board.play_area_tile_size, board.play_area_tile_size)
			position = (board.play_area_tile_size*(x-x_min), board.play_area_tile_size*(y-y_min))
			surface = pygame.Surface(size)
			color = board.play_area[x][y]
			surface.fill(color)
			screen.blit(surface, pygame.Rect(position, dummy))
	screen.blit(pygame.transform.scale(cursor.surface, cursor.size), pygame.Rect(cursor.position, dummy))
	pygame.display.flip()
