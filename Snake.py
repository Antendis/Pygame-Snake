import tkinter
import random
import time
import pygame
import os

#COLOURS
white = 255, 255, 255
black = 0, 0, 0
light_blue = 42, 145, 173
dark_blue = 0, 5, 41
light_green = 22, 219, 55
dark_green = 4, 74, 28
light_red = 255, 13, 33
dark_red = 140, 7, 11
yellow = 211, 214, 34
dark_grey = 14, 15, 15

#VARIABLES THAT CAN BE CHANGED
Background_colour = dark_blue
Screen_width, Screen_height = 625, 500
fps = 100
snake_size = 8
snake_colour = white
movement_amount = 2
gameover_font_size = 110
instruction_font_size = 25
apple_size = 18
volume = 0.15
Title_width = 450
Title_height = 120

#INITIALISE + SOUND
pygame.init()
pygame.font.init()
pygame.mixer.init()

#VARIABLES TO NOT CHANGE
clock = pygame.time.Clock()
centre = (Screen_width/2, Screen_height/2)
gameover_font = pygame.font.SysFont(None, gameover_font_size)
instruction_font = pygame.font.SysFont(None, instruction_font_size)

#IMPORT APPLE PNG
APPLE_IMAGE = pygame.image.load(os.path.join("ASSETS", 'Apple.png'))
apple = pygame.transform.scale(APPLE_IMAGE, (apple_size, apple_size))

#TOP WRITING AND WINDOW SIZE + UPDATE
pygame.display.set_caption('Rohail\'s Snake Game?!')
display = pygame.display.set_mode((Screen_width, Screen_height))
pygame.display.update()

#IMPORT TITLE PNG
TITLE_IMAGE = pygame.image.load(os.path.join("ASSETS", 'Title.png'))
title = pygame.transform.scale(TITLE_IMAGE, (Title_width, Title_height))

#MAKING CENTRED TEXT ACCESSABLE
def points_text(msg, colour):
    mesg = instruction_font.render(msg, True, colour)
    #POINTS TEXT LOCATION
    display.blit(mesg, mesg.get_rect(center = [Screen_width*1/6, Screen_height*1/10]))

#GAMEOVER TEXT
def gameover_text(msg, colour):
    mesg = gameover_font.render(msg, True, colour)
    #TAKES TEXT RECT AND GETS CENTRE AND ALIGNS WITH SCREEN CENTRE ???
    display.blit(mesg, mesg.get_rect(center = [display.get_rect().center[0], Screen_height*5/14]))

#INSTRUCTION TEXT
def instruction_text(msg, colour):
    mesg = instruction_font.render(msg, True, colour)
    #TAKES TEXT RECT AND MOVES TEXT TO CENTRY AND 4/6 FROM THE TOP
    display.blit(mesg, mesg.get_rect(center = [display.get_rect().center[0], Screen_height*4/6]))

#HIGHSCORE TEXT
def highscore_text(msg, colour):
    mesg = instruction_font.render(msg, True, colour)
    #TAKES TEXT RECT AND MOVES TEXT 
    display.blit(mesg, mesg.get_rect(center = [display.get_rect().center[0], Screen_height*7/9]))

#FLASHY SCREEN (one flash)
def gameover_flash():
        display.fill(black)
        gameover_text('GAME OVER', dark_red)
        pygame.display.update()
        time.sleep(0.1)
        display.fill(dark_red)
        gameover_text('GAME OVER', black)
        pygame.display.update()
        time.sleep(0.1)

#GAMEOVER SCREEN
def gameover_screen():
    #READ HIGHSCORE .TXT
    highscore_file = open(os.path.join("ASSETS", 'Highscore.txt'))
    highscore = highscore_file.read()

    #FLASHY SCREEN
    gameover_flash()
    gameover_flash()
    display.fill(dark_grey)
    gameover_text('GAME OVER', dark_red)
    pygame.display.update()
    time.sleep(0.1)
    instruction_text("Play again? Press an arrow key to start!", white)
    highscore_text('Highscore: ' + highscore, white)
    pygame.display.update()
    
    #WAITS FOR ARROW KEY TO PLAY AGAIN
    #CLEAR CACHE
    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        #X BUTTON CLOSES GAME
        if event.type == pygame.QUIT:
            pygame.mixer.Sound.fadeout(music)
            pygame.quit()

        #CHECKS FOR ARROWS IN CACHE
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT or pygame.K_UP or pygame.K_UP:
                gameloop()
                
#MUSICCCCCCC
music = pygame.mixer.Sound(os.path.join("ASSETS", 'Music.mp3'))
#                            loops   ms played   fade in
pygame.mixer.Sound.play(music, 500, 2000000000, 8000)
pygame.mixer.Sound.set_volume(music, volume)

#ENTRY SCREEN
gameplay = False
entry_screen = True 
while entry_screen:
    #READ HIGHSCORE .TXT
    highscore_file = open(os.path.join("ASSETS", 'Highscore.txt'))
    highscore = highscore_file.read()
    #BACKGROUNT COLOUR AND INSTRUCTION TEXT
    display.fill(Background_colour)
    instruction_text('Click the arrow keys to start!', white)
    highscore_text('Highscore: ' + highscore, white)

    #STICK TITLE ON 
    display.blit(title, [centre[0] - Title_width/2, centre[0]*5/9 - Title_height/2])
    pygame.display.update()

    #X BUTTON CLOSES GAME
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.Sound.fadeout(music)
            entry_screen = False

        #ARROWS KEYS MOVE GAME FROM ENTRY SCREEN TO GAMEPLAY
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT or pygame.K_UP or pygame.K_UP:
                gameplay = True
                entry_screen = False
    #FPS
    clock.tick(fps)
    #UPDATE
    pygame.display.update()
    
#GAME LOOP
addpoint = False
def gameloop():
    snake_List = []
    gameplay = True
    points = 0
    Length_of_snake = 1
    #CREATES SNAKE COORDS AND MOVEMENT VARIABLES
    snake_x = display.get_rect().center[0]
    snake_y = display.get_rect().center[1]
    snake_x_change = 0
    snake_y_change = 0
    #APPLE RANDOM COORDS
    applex = round(random.randrange(0, Screen_width - apple_size))
    appley = round(random.randrange(0, Screen_height - apple_size))
    apple_centre_x = applex + apple_size/2
    apple_centre_y = appley + apple_size/2

    while gameplay:
        #READ HIGHSCORE .TXT
        highscore_file = open(os.path.join("ASSETS", 'Highscore.txt'))
        highscore = highscore_file.read()
        
        for event in pygame.event.get():
            #X BUTTON CLOSES GAME
            if event.type == pygame.QUIT:
                pygame.mixer.Sound.fadeout(music)
                gameplay = False
            #ARROWS CAUSE MOVEMENT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake_x_change = -movement_amount
                    snake_y_change = 0
                if event.key == pygame.K_RIGHT:
                    snake_x_change = movement_amount
                    snake_y_change = 0
                if event.key == pygame.K_UP:
                    snake_x_change = 0
                    snake_y_change = -movement_amount
                if event.key == pygame.K_DOWN:
                    snake_x_change = 0
                    snake_y_change = movement_amount

        #IF SNAKE TOUCHES EDGES -> STOPS GAMEPLAY
        if snake_x >= Screen_width or 0 >= snake_x or snake_y >= Screen_height or 0 >= snake_y:
            gameplay = False
            gameover_screen()

        #CHANGES SNAKE COORDS VARIABLES
        snake_x += snake_x_change
        snake_y += snake_y_change

        #PRINT IT ALL
        display.fill(Background_colour)
        #MAKES A LARGER CIRCLE UNDER THE SNAKE HEAD TO GIVE IT A RANGE TO COLLIDE WITH APPLES
        snake_head_range = pygame.draw.circle(display, dark_blue, [snake_x, snake_y],  snake_size + apple_size*2/5)
        #APPLE AND SNAKEHEAD
        display.blit(apple, [applex, appley])
        pygame.draw.circle(display, snake_colour, [snake_x, snake_y], snake_size)

        #COLLISION
        applepos = apple_centre_x, apple_centre_y
        collide = snake_head_range.collidepoint(applepos)
        #MAKIN THE APPLE MOVE WITH COLLISION
        previoustimestamp = 0

        if collide:
            newtimestamp = pygame.time.get_ticks()
            #CHECKS IF TIMES PASSED
            if newtimestamp - previoustimestamp >= 1000:
                #MOVES APPLE
                applex = round(random.randrange(0, Screen_width - apple_size))
                appley = round(random.randrange(0, Screen_height - apple_size))
                apple_centre_x = applex + apple_size/2
                apple_centre_y = appley + apple_size/2
                #NEW TIMESTAMP
                previoustimestamp = pygame.time.get_ticks()
                #PROMPT POINTS GOING UP AND SNAKE ELONGATING
                Length_of_snake += 10
                points += 1

        #SNAKE LENGTH WHEN COLLIDE
        snake_Head = []
        snake_Head.append(snake_x)
        snake_Head.append(snake_y)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List:
            pygame.draw.circle(display, white, [x[0], x[1]], snake_size)

        #removes the s in points when its 1
        if points != 1:
            points_text(str(points) + " points!", yellow)
        else:
            points_text(str(points) + " point!", yellow)

        #HIGHSCORE 
        if int(points) > int(highscore):
            #READ HIGHSCORE .TXT
            highscore_file = open(os.path.join("ASSETS", 'Highscore.txt'))
            highscore = highscore_file.read()
            #UPDATE PROLLY?
            updatehs = open(os.path.join("ASSETS", 'Highscore.txt'), "w")
            updatehs.write(str(points))
            updatehs.close()

        #FPS
        clock.tick(fps)
        #UPDATE
        pygame.display.update()

#PLAYS THE GAME
gameloop()

#CLOSE GAME
pygame.quit()
quit()