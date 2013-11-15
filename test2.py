from numpy  import *
import sys, pygame, time
pygame.init()

black = 0, 0, 0
red = 255, 0, 0
cursor_data = black

class PlayArea:
	def __init__(self, play_area_size, play_area_tile_size, usable_area, area_anchor):
		self.tiles = play_area_size #in tiles
		self.tile_size = play_area_tile_size #in pixels
		self.play_area = []
		self.usable_area = usable_area
		self.area_anchor = area_anchor
		for i in range(0, play_area_size):
			self.play_area.append([red] * self.tiles)
	def press(self, x, y):
		x/=self.tile_size
		y/=self.tile_size
		global cursor_data
		self.play_area[x][y] = cursor_data
	def add_to_screen(self, screen):
		x_min = self.area_anchor[0]/self.tile_size
		y_min = self.area_anchor[1]/self.tile_size
		x_max = self.usable_area[0]/self.tile_size - x_min
		y_max = self.usable_area[1]/self.tile_size - y_min
		dummy = (1, 1)
		for x in range(x_min, x_max):
			for y in range(y_min, y_max):
				size = (self.tile_size, self.tile_size)
				position = (self.tile_size*(x-x_min), self.tile_size*(y-y_min))
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
	def __init__(self, button_width, button_height, count, location_x_start, location_y_start):
		self.menu = []
		for i in range(0, count):
			self.menu.append(Button(position=(location_x_start, location_y_start+button_height*i), size=(button_width, button_height)))
	def press(self, x, y):
		for thing in self.menu:
			if thing.is_pressed(x, y):
				#touch = not touch
				global cursor_data
				cursor_data = thing.color
	def add_to_screen(self, screen):
		dummy = (1, 1)
		for thing in self.menu:
			screen.blit(pygame.transform.scale(thing.surface, thing.size), pygame.Rect(thing.position, dummy))
		return screen

class Game:
	def __init__(self, screen_width, screen_height, button_width, button_height, play_area_tile_size, cursor_size, play_area_size):
		size = screen_width, screen_height
		self.screen = pygame.display.set_mode(size)
		self.board = PlayArea(play_area_size, play_area_tile_size, (screen_width-button_width, screen_height), (0, 0))
		self.menu = Menu(button_width, button_height, count=screen_height/button_height, location_x_start=screen_width-button_width, location_y_start=0)
		self.cursor = Button(position=(screen_width-button_width+(button_width-cursor_size)/2, (button_width-cursor_size)/2), size=(cursor_size, cursor_size))
		self.cursor.surface = pygame.image.load("rectangle.bmp")
		#self.touch = False
	def press(self, event):
		# Set the x, y positions of the mouse click
		x, y = event.pos
		self.menu.press(x, y)
		self.board.press(x, y)
	
	def update_screen(self):
		#if touch:
		#	x, y = pygame.mouse.get_rel()
		#	self.cursor.position = (self.cursor.position[0]+x, self.cursor.position[1]+y)
		#else:
		#	pygame.mouse.get_rel()
		pygame.mouse.get_rel()
		#
		self.screen.fill(black)
		dummy = (1, 1)
		self.screen = self.menu.add_to_screen(self.screen)
		self.screen = self.board.add_to_screen(self.screen)
		self.screen.blit(pygame.transform.scale(self.cursor.surface, self.cursor.size), pygame.Rect(self.cursor.position, dummy))
		pygame.display.flip()

def init():
	global blob
	screen_width, screen_height = 600, 600
	button_width = 100
	button_height = 100
	play_area_tile_size = 100
	cursor_size = 25
	play_area_size = 100
	blob = Game(screen_width, screen_height, button_width, button_height, play_area_tile_size, cursor_size, play_area_size)

def main_loop():
	#print pygame.mouse.get_rel()
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				blob.press(event)
		blob.update_screen()

init()
main_loop()