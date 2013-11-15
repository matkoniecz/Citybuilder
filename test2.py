from numpy  import *
import sys, pygame, time
pygame.init()

size = screen_width, screen_height = 600, 600
screen = pygame.display.set_mode(size)
button_width = 100
button_height = 100
play_area_size = 100
play_area_tile_size = 100
cursor_size = 25
touch = False

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
	def add_to_screen(self, screen):
		x_min = 0
		y_min = 0
		x_max = (screen_width-button_width)/self.play_area_tile_size
		y_max = screen_height/self.play_area_tile_size
		for x in range(x_min, x_max):
			for y in range(y_min, y_max):
				size = (self.play_area_tile_size, self.play_area_tile_size)
				position = (self.play_area_tile_size*(x-x_min), self.play_area_tile_size*(y-y_min))
				surface = pygame.Surface(size)
				color = self.play_area[x][y]
				surface.fill(color)
				screen.blit(surface, pygame.Rect(position, dummy))
		return screen

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

class Menu:
	def __init__(self, button_width, button_height):
		self.menu = []
		for i in range(0, screen_height/button_height):
			self.menu.append(Button(position=(screen_width-button_width, button_height*i), size=(button_width, button_height)))
	def press(self, x, y):
		for thing in self.menu:
			if thing.is_pressed(x, y):
				global touch, cursor_data
				touch = not touch
				cursor_data = thing.color
	def add_to_screen(self, screen):
		for thing in self.menu:
			screen.blit(pygame.transform.scale(thing.surface, thing.size), pygame.Rect(thing.position, dummy))
		return screen
		
board = PlayArea(play_area_size, play_area_tile_size)
menu = Menu(button_width, button_height)
cursor = Button(position=(screen_width-button_width+(button_width-cursor_size)/2, (button_width-cursor_size)/2), size=(cursor_size, cursor_size))
cursor.surface = pygame.image.load("rectangle.bmp")

#print pygame.mouse.get_rel()
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			# Set the x, y positions of the mouse click
			x, y = event.pos
			menu.press(x, y)
			board.press(x, y)
	if touch:
		x, y = pygame.mouse.get_rel()
		cursor.position = (cursor.position[0]+x, cursor.position[1]+y)
	else:
		pygame.mouse.get_rel()
	screen.fill(black)
	dummy = (1, 1)
	screen = menu.add_to_screen(screen)
	screen = board.add_to_screen(screen)
	screen.blit(pygame.transform.scale(cursor.surface, cursor.size), pygame.Rect(cursor.position, dummy))
	pygame.display.flip()
