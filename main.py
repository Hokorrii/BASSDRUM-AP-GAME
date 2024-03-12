import pygame
import math
import spritesheet

pygame.init()

clock = pygame.time.Clock()
FPS = 60

window_width = 800
window_height = 490

screen = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('sprite sheet test')

sprite_sheet_image = pygame.image.load('spritesheet.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

background = pygame.image.load("background.png").convert()
background_width = background.get_width()

scroll = 0
tiles = math.ceil(window_width / background_width) + 1

BLACK = (0,0,0)

#animation list
animation_list = []
animation_steps = [4,7]
action = 0
last_update = pygame.time.get_ticks()
animation_cooldown = 100
frame = 0
step_counter = 0

#loops through the sprite sheet by grabbing an number from the list(number of sprite per animation action)
for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
            temp_img_list.append(sprite_sheet.get_image(step_counter, 686, 758,1.5, BLACK))
            step_counter += 1
    animation_list.append(temp_img_list)

play_animation = False

run = True
while run:
    clock.tick(FPS)
    for i in range(0, tiles):
        screen.blit(background, (i * background_width + scroll, 0))
    scroll -= 2

    if abs(scroll) > background_width:
        scroll = 0
    
    if  play_animation:
    #update animation
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            frame += 1
            last_update = current_time
            if frame >= len(animation_list[action]):
                frame = 0
                play_animation = False
        screen.blit(animation_list[action][frame], (0,0))
    
    else:
        
        screen.blit(animation_list[action][frame], (0,0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not play_animation or frame >= len(animation_list[action])-1:
                    action = 1
                    frame = 0
                    play_animation = True
                    pygame.time.wait(1)
    pygame.display.update()
pygame.quit()