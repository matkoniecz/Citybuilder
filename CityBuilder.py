from numpy  import *
from copy import copy
import sys, pygame, time
pygame.init()

black = 0, 0, 0
red = 255, 0, 0

def makepainter(results):
   def painter(x, y, board):
		position = board.convert_position_on_screen_to_position_on_board(x, y)
		x = position[0]
		y = position[1]
		x_size = 20
		y_size = 20
		for i in range(x, x+x_size):
			for j in range(y, y+y_size):
				if not board.is_valid_tile(i, j):
					return
		for i in range(x, x+x_size):
			for j in range(y, y+y_size):
				board.play_area[i][j] = results[random.randint(0,len(results))]
   return painter
   
class Cursor:
	def __init__(self):
		self.data = makepainter([black])
	def press(self, x, y, board):
		self.data(x, y, board)

class PlayArea:
	def __init__(self, play_area_size, play_area_tile_size, usable_area, area_anchor):
		self.tiles = play_area_size #in tiles
		self.tile_size = play_area_tile_size #in pixels
		self.play_area = []
		self.usable_area = usable_area
		self.area_anchor = area_anchor
		for i in range(0, play_area_size):
			self.play_area.append([red] * self.tiles)
	def convert_position_on_screen_to_position_on_board(self, x, y):
		#may return invalid tile! Check with is_valid_tile
		x-=self.area_anchor[0]
		y-=self.area_anchor[1]
		x/=self.tile_size
		y/=self.tile_size
		return x, y
	def is_valid_tile(self, x, y):
		if x >= self.tiles:
			return False
		if y >= self.tiles:
			return False
		if x < 0 or y < 0:
			return False
		return True
	def is_free_tile(x, y):
		return self.is_valid_tile(x, y)
	def add_to_screen(self, screen):
		x_min = self.area_anchor[0]/self.tile_size
		y_min = self.area_anchor[1]/self.tile_size
		x_max = self.usable_area[0]/self.tile_size - x_min
		y_max = self.usable_area[1]/self.tile_size - y_min
		if x_max > self.tiles:
			x_max = self.tiles
		if y_max > self.tiles:
			y_max = self.tiles
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
		self.color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
		self.results = []
		for i in range(0, 20):
			self.results.append(copy(self.color))
		for color in self.results:
			color[0]=clip(color[0]+random.randint(-20, 20), 0, 255)
			color[1]=clip(color[1]+random.randint(-20, 20), 0, 255)
			color[2]=clip(color[2]+random.randint(-20, 20), 0, 255)
		c = self.color[0], self.color[1], self.color[2]
		self.surface.fill(c)
	def press(self, x, y, cursor):
		if (self.position[0]) <= x <= (self.position[0] + self.size[0]):
			if (self.position[1]) <= y <= (self.position[1] + self.size[1]):
				#touch = not touch
				cursor.data = makepainter(self.results)
		return cursor

class Menu:
	def __init__(self, button_width, button_height, count, location_x_start, location_y_start):
		self.menu = []
		for i in range(0, count):
			self.menu.append(Button(position=(location_x_start, location_y_start+button_height*i), size=(button_width, button_height)))
	def press(self, x, y, cursor):
		for thing in self.menu:
			cursor = thing.press(x, y, cursor)
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
		self.image = Button(position=(screen_width-button_width+(button_width-cursor_size)/2, (button_width-cursor_size)/2), size=(cursor_size, cursor_size))
		self.image.surface = pygame.image.load("rectangle.bmp")
		self.cursor = Cursor()
		#self.touch = False
	def press(self, event):
		# Set the x, y positions of the mouse click
		x, y = event.pos
		self.menu.press(x, y, self.cursor)
		self.cursor.press(x, y, self.board)
	
	def update_screen(self):
		#if touch:
		#	x, y = pygame.mouse.get_rel()
		#	self.image.position = (self.image.position[0]+x, self.image.position[1]+y)
		#else:
		#	pygame.mouse.get_rel()
		pygame.mouse.get_rel()
		#
		self.screen.fill(black)
		dummy = (1, 1)
		self.screen = self.menu.add_to_screen(self.screen)
		self.screen = self.board.add_to_screen(self.screen)
		self.screen.blit(pygame.transform.scale(self.image.surface, self.image.size), pygame.Rect(self.image.position, dummy))
		pygame.display.flip()

def init():
	global blob
	screen_width, screen_height = 600, 600
	button_width = 100
	button_height = 100
	play_area_tile_size = 5
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