from numpy  import *
import sys, pygame, time
pygame.init()

size = screen_width, screen_height = 700, 700
screen = pygame.display.set_mode(size)
black = 0, 0, 0
red = 255, 0, 0

class Button:
	def __init__(self, position, size):
		self.size = size
		self.position = position
		self.surface = pygame.Surface(self.size)
		color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
		self.surface.fill(color)
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
	if touch:
		x, y = pygame.mouse.get_rel()
		cursor.position = (cursor.position[0]+x, cursor.position[1]+y)
	else:
		pygame.mouse.get_rel()
	screen.fill(black)
	dummy = (1, 1)
	for thing in menu:
		screen.blit(pygame.transform.scale(thing.surface, thing.size), pygame.Rect(thing.position, dummy))
	screen.blit(pygame.transform.scale(cursor.surface, cursor.size), pygame.Rect(cursor.position, dummy))
	pygame.display.flip()
