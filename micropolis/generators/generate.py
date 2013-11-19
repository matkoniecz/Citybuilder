import pygame, time

to_process = ["res_zones.png", "com_zones.png", "ind_zones.png", "res_houses.png"]
for name in to_process:
	file = pygame.image.load(name)
	offset = 0
	count = 1
	while (file.get_height() - offset) >= file.get_width():
		size = (file.get_width(), file.get_width())
		surface = file.subsurface(pygame.Rect(0, offset, file.get_width(), file.get_width()))
		pygame.image.save(surface, name.replace(".png", "")+str(count)+".png")
		offset += file.get_width()
		count += 1
