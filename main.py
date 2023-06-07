import pygame
import button
# import menus

import match
#create display window
SCREEN_HEIGHT = 820
SCREEN_WIDTH = 820

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Start Go game')

#load button images
start_img = pygame.image.load('start_btn.png').convert_alpha()
exit_img = pygame.image.load('exit_btn.png').convert_alpha()

#create button instances
start_button = button.Button(100, 200, start_img, 0.8)
exit_button = button.Button(500, 200, exit_img, 0.8 )

#game loop
run = True
while run:
     
	screen.fill((181, 101, 29))
	

	if start_button.draw(screen):
		match.main()	
	
	
	if exit_button.draw(screen):
		pygame.quit()
		

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()
