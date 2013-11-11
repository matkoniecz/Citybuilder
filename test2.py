from numpy  import *
import sys, pygame, time
pygame.init()

size = width, height = 700, 700
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

menu = Button(position=(0,0), size=(100,100))


cursor = Button(position=(0,0), size=(100,100))
cursor.surface = pygame.image.load("rectangle.bmp")
cursorrect = cursor.surface.get_rect()

#print pygame.mouse.get_rel()
touch = False
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			# Set the x, y positions of the mouse click
			x, y = event.pos
			if menu.is_pressed(x, y):
				touch = not touch
	if touch:
		cursorrect = cursorrect.move(pygame.mouse.get_rel())
	else:
		pygame.mouse.get_rel()
	screen.fill(black)
	screen.blit(menu.surface, pygame.Rect(menu.position, menu.size))
	screen.blit(cursor.surface, cursorrect)
	pygame.display.flip()
