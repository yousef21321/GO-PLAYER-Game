import pygame
import button2
import main
pygame.init()

SCREEN_WIDTH = 820
SCREEN_HEIGHT = 820

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GO GAME")

game_paused = False
menu_state = "main"

font = pygame.font.SysFont("arialblack", 40)

TEXT_COL = (255, 255, 255)

resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
options_img = pygame.image.load("images/button_options.png").convert_alpha()
quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
video_img = pygame.image.load('images/button_video.png').convert_alpha()
audio_img = pygame.image.load('images/button_audio.png').convert_alpha()
keys_img = pygame.image.load('images/button_keys.png').convert_alpha()
back_img = pygame.image.load('images/button_back.png').convert_alpha()

resume_button = button2.Button(304, 125, resume_img, 1)
options_button = button2.Button(297, 250, options_img, 1)
quit_button = button2.Button(336, 375, quit_img, 1)
video_button = button2.Button(226, 75, video_img, 1)
audio_button = button2.Button(225, 200, audio_img, 1)
keys_button = button2.Button(246, 325, keys_img, 1)
back_button = button2.Button(332, 450, back_img, 1)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


run = True
while run:
    background_image = pygame.image.load("111111.jpg").convert()
    screen.blit(background_image, [0, 0])

    if game_paused == True:
        if menu_state == "main":
            if resume_button.draw(screen):
                run = False
            if options_button.draw(screen):
                menu_state = "options"
            if quit_button.draw(screen):
                pygame.display.update()

        if menu_state == "options":
            if video_button.draw(screen):
                print("Video Settings")
            if audio_button.draw(screen):
                print("Audio Settings")
            if keys_button.draw(screen):
                print("Change Key Bindings")
            if back_button.draw(screen):
                menu_state = "main"
    else:
        draw_text("Press SPACE to pause", font, TEXT_COL, 160, 250)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_paused = True
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
