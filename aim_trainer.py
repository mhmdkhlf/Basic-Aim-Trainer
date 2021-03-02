#imports
import time
from random import randint
from math import sqrt
import os
import sys
import pygame

### functions of what we are displaying ###
def screen(NUM_OF_HITS):
    window.fill(WHITE)
    if NUM_OF_HITS==-1:
        TEXT = WORD_FONT.render("PRESS THE TARGET TO START THE ROUND!" , 1 ,BLACK)
        window.blit(TEXT, (int(WIDTH/2 - TEXT.get_width()/2), int(HEIGHT/2 - TEXT.get_height()/2)-150))
    else:
        COUNTER = WORD_FONT.render(str(NUM_OF_HITS) , 1 ,RED)
        window.blit(COUNTER, (int(WIDTH - COUNTER.get_width()),int(HEIGHT - COUNTER.get_height())))
    window.blit(target, (X, Y))
    pygame.draw.circle(window, BLACK, (X + TARGET_RADIUS - 1, Y + TARGET_RADIUS), TARGET_RADIUS, 1)
    pygame.display.update()

def hit():
    window.fill(WHITE)
    window.blit(hitmarker, (X, Y))
    COUNTER = WORD_FONT.render(str(NUM_OF_HITS) , 1 ,RED)
    window.blit(COUNTER, (int(WIDTH - COUNTER.get_width()),int(HEIGHT - COUNTER.get_height())))
    pygame.display.update()
    pygame.time.wait(150)

def miss():
    window.fill(WHITE)
    window.blit(missmarker, (click_x - MARKERS_RADIUS, click_y - MARKERS_RADIUS))
    pygame.display.update()
    pygame.time.wait(1000)

def display_num_of_target_hit(): #display number of hits
    if NUM_OF_HITS == 0:
        RESULT = "YOU DIDN'T HIT ANY TARGETS."
    elif NUM_OF_HITS == 1:
        RESULT = "YOU ONLY HIT THE FIRST TARGET!"
    else :
        RESULT = f"YOU HIT {NUM_OF_HITS} TARGETS BEFORE MISSING!"
    window.fill(WHITE)
    text = WORD_FONT.render(RESULT , 1 ,BLACK)
    window.blit(text, (int(WIDTH/2 - text.get_width()/2), int(HEIGHT/2 - text.get_height()/2)-55))
    pygame.display.update()
    pygame.time.wait(1000)

def display_reaction(): #display average time of reaction time
    if NUM_OF_HITS>0:
        SUM_TIME = 0
        del times_between_hits[0]
        for elapsed in times_between_hits:
            SUM_TIME += elapsed
        average_time = SUM_TIME / len(times_between_hits)
        average_time_between_hits = "AVERAGE REACTION TIME: "+format(average_time,'.3f')+'s'
        text = WORD_FONT.render(average_time_between_hits, 1 ,BLACK)
        window.blit(text, (int(WIDTH/2 - text.get_width()/2), int(HEIGHT/2 - text.get_height()/2)+45))
        pygame.display.update()
        pygame.time.wait(1000)

def new_round_button(): #display start new round button
    title1 = "start new"
    title2 = "   round "
    text1 = WORD_FONT.render(title1, 1, BLACK)
    text2 = WORD_FONT.render(title2, 1, BLACK)
    window.blit(text1,(0,-2))
    window.blit(text2,(0,int(text1.get_height())))
    global button
    button = pygame.Rect(-2,-2,int(text1.get_width())+6,int(text1.get_height())+int(text2.get_height()))
    pygame.draw.rect(window,RECT_COLOR,button,4)
    pygame.display.update()

#initializing pygame
pygame.init()

#colors and font
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
RECT_COLOR = (100,100,100)
WORD_FONT = pygame.font.SysFont('moderno20', 50)

#button variables
TARGET_RADIUS = 16
MARKERS_RADIUS = 15

#load images
directory = os.path.dirname('C:\\Users\\moham\\Dropbox\\My PC (LAPTOP-NODFI3I4)\\Desktop\\Random\\Random Python files\\Aim Trainer\\')
target = pygame.image.load(os.path.join(directory, "target.jpg"))
hitmarker = pygame.image.load(os.path.join(directory, "hitmarker.jpg"))
missmarker = pygame.image.load(os.path.join(directory, "missmarker.jpg"))

#setup display
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Aim Ttainer")

# setup for main loop
FPS = 60
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
NUM_OF_HITS = -1
pygame.event.clear()
pygame.mouse.set_pos([WIDTH // 2, HEIGHT // 2])
X = WIDTH // 2-TARGET_RADIUS+1
Y = HEIGHT // 2-TARGET_RADIUS
times_between_hits = []
screen(NUM_OF_HITS)
start_time = time.time()
end_game = False

### GAME MAIN LOOP ###
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and not end_game:
            end_time = time.time()
            time_between_hit = end_time-start_time
            click_x, click_y = pygame.mouse.get_pos()
            distance = sqrt((X + TARGET_RADIUS - 1 - click_x)**2 + (Y + TARGET_RADIUS - click_y)**2)
            if distance < TARGET_RADIUS:
                times_between_hits.append(time_between_hit)
                NUM_OF_HITS += 1
                hit()
                X = randint(0, WIDTH - TARGET_RADIUS*2)
                Y = randint(0, HEIGHT - TARGET_RADIUS*2)
                screen(NUM_OF_HITS)
                start_time = time.time()
                continue
            elif NUM_OF_HITS==-1:
                pass
            else:
                miss()
                display_num_of_target_hit()
                display_reaction()
                new_round_button()
                end_game = True

        if event.type == pygame.MOUSEBUTTONDOWN and end_game:
            if button.collidepoint(event.pos):
                NUM_OF_HITS = -1
                pygame.event.clear()
                pygame.mouse.set_pos([WIDTH // 2, HEIGHT // 2])
                X = WIDTH // 2-TARGET_RADIUS+1
                Y = HEIGHT // 2-TARGET_RADIUS
                times_between_hits = []
                screen(NUM_OF_HITS)
                start_time = time.time()
                end_game = False
                pygame.time.wait(1000)

### END GAME & MAIN LOOP###