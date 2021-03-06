from numpy  import *
from copy import copy
import sys, pygame, time
import os.path
import ConfigParser
from lxml import etree
pygame.init()

black = 0, 0, 0
red = 255, 0, 0

def makepainter(possibilities):
	def painter(x, y, board):
		selected = possibilities[random.randint(0,len(possibilities))]
		size = selected['size']
		position = board.convert_position_on_screen_to_position_on_board(x-board.tile_size*(size-1)/2, y-board.tile_size*(size-1)/2)
		x = position[0]
		y = position[1]
		x_size = size
		y_size = size
		for i in range(x, x+x_size):
			for j in range(y, y+y_size):
				if not board.is_free_tile(i, j):
					return
		for i in range(x, x+x_size):
			for j in range(y, y+y_size):
				board.play_area[i][j] = {'surface': None, 'size': 0, 'ground': False, 'parent': (x, y)}
		board.play_area[x][y] = {'surface': pygame.image.load(selected['image']), 'size': size, 'ground': False, 'parent': (x, y)}
	return painter
   
def makeremover(possibilities):
	def remover(x, y, board):
		selected = possibilities[random.randint(0,len(possibilities))]
		size = selected['size']
		position = board.convert_position_on_screen_to_position_on_board(x-board.tile_size*(size-1)/2, y-board.tile_size*(size-1)/2)
		position = board.convert_position_on_screen_to_position_on_board(x-board.tile_size*(size-1)/2, y-board.tile_size*(size-1)/2)
		x = position[0]
		y = position[1]
		try:
			root = board.play_area[x][y]['parent']
		except KeyError:
			return
		x = root[0]
		y = root[1]
		size = board.play_area[x][y]['size']
		x_size = size
		y_size = size
		for i in range(x, x+x_size):
			for j in range(y, y+y_size):
				board.play_area[i][j] = {'surface': pygame.image.load(selected['image']), 'size': size, 'ground': True, 'parent': (x, y)}
	return remover

class Cursor:
	def __init__(self):
		self.data = None
	def press(self, x, y, board):
		if self.data != None:
			self.data(x, y, board)

class PlayArea:
	def get_ground_tile(self, selected, x, y):
		if selected['size'] != 1:
			raise "unimplemented handling of large ground tiles!"
		return {'surface': selected['surface'], 'size': selected['size'], 'ground': True, 'parent': (x, y)}
	def __init__(self, play_area_size, play_area_tile_size, usable_area, area_anchor, xml_file_with_definitions):
		data = etree.parse(xml_file_with_definitions)
		for elt in data.getiterator("special"):
			for e in elt:
				ground_tile_possibilities = []
				if e.tag == "delete":
					for sprite in e:
						ground_tile_possibilities.append({'image': sprite.attrib['image'], 'surface': pygame.image.load(sprite.attrib['image']), 'size': int(sprite.attrib['size'])})
		if len(ground_tile_possibilities) == 0:
			raise "ground tile must be included!"
		if len(ground_tile_possibilities) != 1:
			raise "unimplemented handling of multiple ground tiles!"
		selected = ground_tile_possibilities[random.randint(0,len(ground_tile_possibilities))]
		size = selected['size']

		self.tiles = play_area_size #in tiles
		self.tile_size = play_area_tile_size #in pixels
		self.play_area = []
		self.usable_area = usable_area
		self.area_anchor = area_anchor
		for x in range(0, play_area_size):
			column = []
			for y in range(0, play_area_size):
				column.append(self.get_ground_tile(selected, x, y))
			self.play_area.append(column)
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
	def is_ground_tile(self, x, y):
		return self.play_area[x][y]['ground']
	def is_free_tile(self, x, y):
		if not self.is_valid_tile(x, y):
			return False
		if self.is_ground_tile(x, y):
			return True
	def add_to_screen(self, screen):
		x_min = self.area_anchor[0]/self.tile_size
		y_min = self.area_anchor[1]/self.tile_size
		x_max = self.usable_area[0]/self.tile_size - x_min + 1
		y_max = self.usable_area[1]/self.tile_size - y_min + 1
		if x_max > self.tiles:
			x_max = self.tiles
		if y_max > self.tiles:
			y_max = self.tiles
		dummy = (1, 1)
		for x in range(x_min, x_max):
			for y in range(y_min, y_max):
				if self.play_area[x][y]['surface'] != None:
					size = (self.tile_size*self.play_area[x][y]['size'], self.tile_size*self.play_area[x][y]['size'])
					position = (self.tile_size*(x-x_min), self.tile_size*(y-y_min))
					screen.blit(pygame.transform.scale(self.play_area[x][y]['surface'], size), pygame.Rect(position, dummy))
		return screen

class Button:
	def __init__(self, function, image, position, size):
		self.size = size
		self.position = position
		self.function = function
		self.image = image
		self.surface = pygame.image.load(image)
	def press(self, x, y, cursor):
		if (self.position[0]) <= x <= (self.position[0] + self.size[0]):
			if (self.position[1]) <= y <= (self.position[1] + self.size[1]):
				cursor.data = self.function
				return cursor, True
		return cursor, False
	def add_to_screen(self, screen):
		dummy = (1, 1)
		screen.blit(pygame.transform.scale(self.surface, self.size), pygame.Rect(self.position, dummy))
		return screen
class Menu:
	def __init__(self, button_width, button_height, location_x_start, location_y_start, xml_file_with_definitions):
		self.menu = []
		count = 0
		data = etree.parse(xml_file_with_definitions)
		for elt in data.getiterator("buildings"):
			for e in elt:
				possibilities = []
				for sprite in e:
					possibilities.append({'image': sprite.attrib['image'], 'size': int(sprite.attrib['size'])})
				self.menu.append(Button(function=makepainter(possibilities), image=e.attrib['image'], position=(location_x_start, location_y_start+button_height*count), size=(button_width, button_height)))
				count+=1
		for elt in data.getiterator("linear"):
			for e in elt:
				possibilities = []
				for sprite in e:
					possibilities.append({'image': sprite.attrib['image'], 'size': int(sprite.attrib['size'])})
				self.menu.append(Button(function=makepainter(possibilities), image=e.attrib['image'], position=(location_x_start, location_y_start+button_height*count), size=(button_width, button_height)))
				count+=1
		for elt in data.getiterator("special"):
			for e in elt:
				possibilities = []
				for sprite in e:
					possibilities.append({'image': sprite.attrib['image'], 'size': int(sprite.attrib['size'])})
				if e.tag == "delete":
					self.menu.append(Button(function=makeremover(possibilities), image=e.attrib['image'], position=(location_x_start, location_y_start+button_height*count), size=(button_width, button_height)))
					count+=1
				else:
					raise "Unhandled special button"
	def press(self, x, y, cursor):
		for thing in self.menu:
			cursor, pressed = thing.press(x, y, cursor)
			if pressed:
				return cursor, True
		return cursor, False
	def add_to_screen(self, screen):
		for thing in self.menu:
			screen = thing.add_to_screen(screen)
		return screen

class Game:
	def __init__(self):
		default_settings = [
			{'section_name': 'display', 
			'dictionary_of_settings': {
			'screen_width': 900,
			'screen_height': 710,
			'button_width': 80,
			'button_height': 80,
			'play_area_tile_size': 25,
			}}, 
			{'section_name': 'play_area',
			'dictionary_of_settings': {
			'play_area_size': 100,
			}},
			{'section_name': 'data',
			'dictionary_of_settings': {
			'xml_file_with_data': 'structure.xml',
			}},
		]
		settings = self.load_settings_from_file(default_settings)
		size = settings['screen_width'], settings['screen_height']
		self.screen_width = settings['screen_width']
		self.screen_height = settings['screen_height']
		self.button_width = settings['button_width']
		self.button_height = settings['button_height']
		self.xml_file_with_data = settings['xml_file_with_data']
		print settings['xml_file_with_data']
		self.screen = pygame.display.set_mode(size)
		self.board = PlayArea(play_area_size = settings['play_area_size'], play_area_tile_size = settings['play_area_tile_size'], usable_area = (settings['screen_width'], self.screen_height), area_anchor = (0, 0), xml_file_with_definitions=self.xml_file_with_data)
		self.menu = Menu(settings['button_width'], self.button_height, location_x_start=settings['screen_width']-self.button_width, location_y_start=0, xml_file_with_definitions=self.xml_file_with_data)
		self.cursor = Cursor()
	def press(self, event):
		# Set the x, y positions of the mouse click
		x, y = event.pos
		cursor, pressed = self.menu.press(x, y, self.cursor)
		if pressed:
			return
		self.cursor.press(x, y, self.board)
	
	def update_screen(self):
		self.screen.fill(black)
		dummy = (1, 1)
		self.screen = self.board.add_to_screen(self.screen)
		self.screen = self.menu.add_to_screen(self.screen)
		pygame.display.flip()

	def get_settings_filename(self):
		return "settings.cfg"

	def load_settings_from_file(self, default_settings):
		loaded_settings = {}
		unified_defaults = {}
		for set in default_settings:
			unified_defaults.update(set['dictionary_of_settings'])
		config = ConfigParser.SafeConfigParser()
		config.read(self.get_settings_filename())
		for set in default_settings:
			section = set['section_name']
			for name in set['dictionary_of_settings']:
				try:
					if isinstance(unified_defaults[name], (int, long)):
						loaded_settings[name] = config.getint(section, name)
					elif isinstance(unified_defaults[name], (str)):
						loaded_settings[name] = config.get(section, name)
					else:
						raise "That should be impossible!"
				except ConfigParser.NoSectionError, ConfigParser.NoOptionError:
					loaded_settings[name] = unified_defaults[name]
		return loaded_settings
	def save_settings_to_file(self):
		config = ConfigParser.RawConfigParser()
		# When adding sections or items, add them in the reverse order of
		# how you want them to be displayed in the actual file.
		# In addition, please note that using RawConfigParser's and the raw
		# mode of ConfigParser's respective set functions, you can assign
		# non-string values to keys internally, but will receive an error
		# when attempting to write to a file or when you get it in non-raw
		# mode. SafeConfigParser does not allow such assignments to take place.
		config.add_section('display')
		config.set('display', 'screen_width', str(self.screen_width))
		config.set('display', 'screen_height', str(self.screen_height))
		config.set('display', 'button_width', str(self.button_width))
		config.set('display', 'button_height', str(self.button_height))
		config.set('display', 'play_area_tile_size', str(self.board.tile_size))
		config.add_section('play_area')
		config.set('play_area', 'play_area_size', str(self.board.tiles))
		config.add_section('data')
		config.set('data', 'xml_file_with_data', str(self.xml_file_with_data))
		# Writing our configuration file
		with open(self.get_settings_filename(), 'wb') as configfile:
			config.write(configfile)	

def init():
	global blob
	blob = Game()
	blob.save_settings_to_file()

def main_loop():
	#print pygame.mouse.get_rel()
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				blob.press(event)
		blob.update_screen()
		time.sleep(0.01)

init()
main_loop()