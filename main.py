import pygame
import math
import spritesheet
import random
import sys
import re

pygame.init()
clock = pygame.time.Clock()
FPS = 60

window_width = 800
window_height = 500
screen = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('BASSDRUM-HEAVEN')
icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)

sprite_sheet_image = pygame.image.load('img/spritesheet.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

hit_image = pygame.image.load("img/hit.png").convert_alpha()
miss_image = pygame.image.load("img/miss.png").convert_alpha()
note_image = pygame.image.load("img/note.png").convert_alpha()
notes = []

logo = pygame.image.load("img/logo_image.png")
logo_rect = logo.get_rect()
logo_x = (window_width - logo_rect.width)//2
logo_y = (window_height- logo_rect.height)//2

bass_drum_hit_sound = "sfx/hitsound.mp3"
hit_sound = pygame.mixer.Sound(bass_drum_hit_sound)
miss_sound = "sfx/misssound.mp3"
miss_hit = pygame.mixer.Sound(miss_sound)
background_music = "sfx/bgmusic.wav"
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)

background = pygame.image.load("img/background.png").convert()
background_width = background.get_width()
menu_background = pygame.image.load("img/background_menu.png").convert()

transparent = (0, 0, 0, 0)
BLACK = (0,0,0)

font_color = (8,4,44)
font = pygame.font.Font("img/Rocket.ttf", 36)
graphics = pygame.image.load("img/graphic.png").convert_alpha()

def make_text(text,font,text_color,x,y):
        global text_input
        text_input = font.render(text, True, text_color)

        global screen
        screen.blit(text_input, (x,y))
def menu(): 
    global user_text
    user_text = ""

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                if event.key == pygame.K_RETURN:
                    if re.match(r'^[1-9][0-9]?$', user_text):
                        number = int(user_text)
                        if number <= 20:
                            game()
                if event.unicode.isdigit():
                    user_text += event.unicode
                if event.key == pygame.K_TAB:
                    keybind_menu()

        screen.blit(menu_background,(0,0))
        
        make_text("Please type a number between 1 and 20", font, font_color, 125, 100 + 130)
        make_text("This is your note speed", font, font_color, 230, 135 + 130)
        make_text("Press TAB to view keybinds", font, font_color, 230, 135 + 300)

        
        screen.blit(graphics, (115,225 + 115))

        user_input = font.render(user_text, True, font_color)
        screen.blit(user_input, (375,250 + 115))
        
        displacement = 20 * math.sin(pygame.time.get_ticks() * 0.004)
        logo_y = (window_height - 270 - logo_rect.height) // 2 + displacement
        screen.blit(logo, (logo_x, logo_y))

        clock.tick(60)

        pygame.display.update()
    pygame.quit()
def game():
    score = 0
    miss_count = 0

    scroll = 0
    tiles = math.ceil(window_width / background_width) + 1

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
                    # Check if any notes are currently visible and intersecting the key press
                    for note in notes:
                        if note["visible"] and note["rect"].colliderect(pygame.Rect(400, 550, 300, 300)):  # Adjust position as needed
                            note["visible"] = False
                            screen.blit(hit_image,(background_width/2,0))
                            hit_sound.play()
                            score += 10
                if event.key == pygame.K_ESCAPE:
                    escape_menu()
                action = 1
                frame = 0
                play_animation = True
            # Create a new note with random position and add it to the list
        if random.random() < 0.01:  # Adjust this value to control note spawning frequency
            note_rect = note_image.get_rect(center=(random.randint(500, 750), 0))
            notes.append({"rect": note_rect, "visible": True})
        # Move and draw the notes
        for note in notes:
            if note["visible"]:
                screen.blit(note_image, note["rect"])
                note["rect"].move_ip(0, int(user_text))  # Move the note down
                # If note is off-screen, make it invisible
                if note["rect"].bottom > 700:
                    note["visible"] = False
                    screen.blit(miss_image,(background_width/2,0))
                    miss_count += 1
                    miss_hit.play()
        
        if pygame.get_init():
            score_on_screen = font.render("Score: " + str(score),True, font_color)
            miss_counter_screen = font.render("Misses: " + str(miss_count),True, font_color)

        screen.blit(score_on_screen, (window_width/2 + window_height/2 ,10))
        screen.blit(miss_counter_screen, (window_width/2 + window_height/2 ,50))

        pygame.display.update()
    pygame.quit()

def escape_menu():
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game()
                if event.key == pygame.K_x:
                    sys.exit()
                if event.key == pygame.K_TAB:
                    menu()
        
        screen.blit(menu_background,(0,0))
        
        make_text("OPTION MENU",font,font_color,325,100)
        make_text("Press X to quit the game",font,font_color,225,200)
        make_text("Press ENTER to return to/restart the game",font,font_color,125,250)
        make_text("Press TAB to return to menu",font,font_color,200,300)
        

        pygame.display.update()
    pygame.quit()

def keybind_menu():
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    sys.exit()
                if event.key == pygame.K_TAB:
                    menu()
        
        screen.blit(menu_background,(0,0))
        
        make_text("KEYBINDS",font,font_color,340,100)
        make_text("Press X to quit the game",font,font_color,225,200)
        make_text("Press TAB to return to the menu",font,font_color,175,250)
        make_text("Press the SPACE BAR to hit notes!",font,font_color,175,300)
        make_text("Press the ESC to view more options in game",font,font_color,115,350)
        pygame.display.update()
    pygame.quit()

menu()