import time
import pygame
from random import randint
pygame.init()

#initializing the colors
# R G B
# (Red, Green, Blue)
BACKDROP = (200,255,255)
RED = (255, 0, 0)
GREEN = (0, 255, 51)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 100)
BLUE = (80, 80, 255)
LIGHT_GREEN = (200, 255, 200)
LIGHT_RED = (250, 128, 114)
BLACK = (0,0,0)

#creating the screen
mw = pygame.display.set_mode((500,500))
mw.fill(BACKDROP)

#initializing the time
clock = pygame.time.Clock()

#initializing the game "logic"
class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=(BACKDROP)):
        self.rect = pygame.Rect(x,y,width,height)
        self.fill_color = color
    
    def n_color(self,ncolor):
        self.fill_color = ncolor

    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)

    def outline(self, thic, frame_color):
        pygame.draw.rect(mw, frame_color, pygame.Rect(self.rect.x - thic, self.rect.y - thic, self.rect.width + thic*2 , self.rect.height + thic*2), thic)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x,y)

class Label(Area):
    def set_text(self, text, tsize=12, tcolor=BLACK, tbold=False):
        self.image = pygame.font.SysFont('verdana', tsize, tbold,).render(text, True, tcolor)

    def drawtext(self, shift_x=0, shift_y=0):
        self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))
    
#defining the start time
start_time = time.time()
cur_time = start_time

cards=[]
numcards = 4
x=60

#defining the time with the timer
text_time_n_points = Label(0,0,10,10)
text_time_n_points.set_text("Time:               Points:", 40, DARK_BLUE)
text_time_n_points.drawtext(5,5)

timer = Label(15,50,55,50)
timer.set_text("0",35, DARK_BLUE)
timer.drawtext(0,0)

count = Label(400, 55,50,50)
count.set_text("0",35,DARK_BLUE)
count.drawtext(0,0)

# setting up the cards
for i in range(numcards):
    n_card = Label(x,170, 70, 100, YELLOW)
    n_card.fill()  
    n_card.outline(10, BLACK)
    n_card.set_text('CLICK', 17, BLACK, True)
    cards.append(n_card)
    x += 100
    # n_card.drawtext(4,40)         # <--- Debug line

wait = 0
maxwait = 20
points = 0
click = 0

#creating the game loop with the logic
running = True
while running:
    #it shows a new random card every "maxwait" frames
    if wait == maxwait:
        click = randint(1, numcards)
        for i in range(numcards):
            cards[i].n_color(YELLOW)
            if (i+1) == click:
                cards[i].drawtext(4,40)
            else:
                cards[i].fill()
        wait = 0
    else:
        wait += 1

    #handling input from the player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            for i in range(numcards):
                if cards[i].collidepoint(x,y):
                    if i + 1 == click:
                        cards[i].n_color(GREEN)
                        cards[i].set_text('CLICKED!', 12, BLACK, True)
                        cards[i].drawtext(4,40)
                        cards[i].set_text('CLICK', 17, BLACK, True)                        
                        points += 1
                    else:
                        cards[i].n_color(RED)
                        cards[i].set_text('MISSED!', 12, BLACK, True)
                        cards[i].drawtext(4,40)
                        cards[i].set_text('CLICK', 17, BLACK, True)
                        points += -1
        
        count.set_text(str(points), 35, DARK_BLUE)
        count.fill()
        count.drawtext(0,0)
    new_time = time.time()

    #displaying time
    if int(new_time - cur_time) == 1:
        timer.set_text(str(int(new_time -  start_time)), 35, DARK_BLUE)
        timer.drawtext(0,0)
        cur_time = new_time
    
    #winning or losing
    if int(new_time - start_time) > 10:
        lost_screen = Label(0,0,500,500,RED)
        lost_screen.set_text("You were to slow.",50, True)
        lost_screen.drawtext(35,200)
    
    if points > 5:
        win_screen = Label(0,0,500,500,GREEN)
        win_screen.set_text("You WON, nicely done :)",35, True)
        win_screen.drawtext(27,200)

    #updates the screen
    pygame.display.update()
    clock.tick(40)

    # 151 - 16 = 135