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

# setting the title of the window
pygame.display.set_caption('FastClickerV2')

# creating the icon of our game
programIcon = pygame.image.load('assets/fclogo.png')
pygame.display.set_icon(programIcon)

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

    def outline(self, thic=1, frame_color=BLACK):
        pygame.draw.rect(mw, frame_color, pygame.Rect(self.rect.x - thic, self.rect.y - thic, self.rect.width + thic*2 , self.rect.height + thic*2), thic)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x,y)

class Label(Area):
    def set_text(self, text, tsize=12, tcolor=BLACK, tbold=False):
        self.image = pygame.font.SysFont('verdana', tsize, tbold,).render(text, True, tcolor)

    def drawtext(self, shift_x=0, shift_y=0,fillbfr=True):
        if fillbfr == True:
            self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename)
    
    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


# class Data():
#     def __init__(self, score):
#         self.score = score
    
#     def save(self)
        

#defining the time with the timer
text_time_n_points = Label(5,5,10,10)
text_time_n_points.set_text("Time:               Points:", 40, DARK_BLUE)

timer = Label(15,50,55,50)
timer.set_text("0",35, DARK_BLUE)

count = Label(400, 55,50,50)
count.set_text("0",35, DARK_BLUE)

#probably we are going to make these buttons a for loop with a list, and every position to be taken as a certain button. 
#defining the buttons after end screen
leave_buttton = Label(200,250,100,25,YELLOW)
leave_buttton.set_text("Leave Game", tbold=True)

play_again = Label(200,200,100,25,YELLOW)
play_again.set_text("Play again", tbold=True)

play_button = Label(200,200,100,25,YELLOW)
play_button.set_text("Play ", tbold=True)

# definning the start screen images
fastclicker_img = Picture("assets/Fastclickerlogo.png", 150, 100, 225, 83)


# Save_Button = Label(200,250,50,25,BACKDROP)
# # play_again.outline(2)
# play_again.set_text("Save score", tbold=True)

cards=[]
numcards = 4
x=60


# setting up the cards
for i in range(numcards):
    n_card = Label(x,170, 70, 100, YELLOW)
    n_card.set_text('CLICK', 17, BLACK, True)
    cards.append(n_card)
    x += 100

wait = 0
maxwait = 20
click = 0


#creating the game loop with the logic
# running[0] = the game loop loop
# running[1] = the actual game loop 
# running[2] = the game state, did tha player win or lose?
# running[3] = Start screen
running = [True,False,True,True]
while running[0]:

    while running[3]:
        mw.fill(BACKDROP)
        fastclicker_img.draw()
        play_button.outline(10)
        play_button.drawtext(5,5)

        leave_buttton.n_color(YELLOW)
        leave_buttton.outline(10)
        leave_buttton.drawtext(5,5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if leave_buttton.collidepoint(x,y):
                    leave_buttton.n_color(GREEN)
                    leave_buttton.drawtext(5,5)
                    pygame.display.update()
                    pygame.quit()
                    
                elif play_button.collidepoint(x, y):
                    play_button.n_color(GREEN)
                    play_button.drawtext(5,5)
                    running[1] = True # enable the game loop
                    running[3] = False # leave the current loop

        pygame.display.update()
        clock.tick(40)


    if running[1] == True:
        #resseting the variables
        points = 0
        start_time = time.time()
        cur_time = start_time

        #redrawing stuff
        mw.fill(BACKDROP)
        text_time_n_points.drawtext(0,0)
        count.set_text("0",35, DARK_BLUE)
        count.drawtext(0,0)
        timer.set_text("0",35, DARK_BLUE)
        timer.drawtext(0,0)
        for i in range(numcards):
            cards[i].fill()
            cards[i].outline(10)

    pygame.display.update()
    
    while running[1]:
        #it shows a new random card every "maxwait" frames
        if wait == maxwait: #if wait % 20 ==  0: ....
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
                running[0] = False
                running[1] = False

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
            running[1] = False # leaving the game loop
            running[2] = False # updating the state of our game to lost
    
        if points > 5:
            running[1] = False # leaving the game loop
            running[2] = True # updating the state of our game to won
      
        #updates the screen
        pygame.display.update()
        clock.tick(40)

    if running[0]:
        #making the screen to play again or leave
        mw.fill(BACKDROP)
        
        show_state_game = Label(100,150,300,20,RED if running[2]==False else GREEN)
        show_state_game.set_text('You lost from the timer...' if running[2]==False else 'You won the timer!!', tbold=True)
        if running[2]:
            resul_time = Label(100, 170, 300,20)
            resul_time.set_text("Completion time: " + str (int(new_time - start_time)) + " sec", tcolor=DARK_BLUE)
        show_state_game.drawtext(2,2)
        resul_time.drawtext(2,2)


        play_again.n_color(YELLOW)
        play_again.outline(10)
        play_again.drawtext(5,5)

        leave_buttton.n_color(YELLOW)
        leave_buttton.outline(10)
        leave_buttton.drawtext(5,5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running[0] = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if leave_buttton.collidepoint(x,y):
                    leave_buttton.n_color(GREEN)
                    leave_buttton.drawtext(5,5)
                    running[0] = False # leave the game loop loop
                    
                elif play_again.collidepoint(x, y):
                    play_again.n_color(GREEN)
                    play_again.drawtext(5,5)
                    running[1] = True # enable the game loop

        pygame.display.update()
        clock.tick(40)

#bug report:
#nothing
 
#additions before completion:
# Make a difficulty system.
# Make a save setting to save on a local txt file.
# Show the Highscore to the User in the start screen and play again screen.
# sound effects
# Make some of the code a bit more simpler

# Try to make the txt somewhat safe from the user to edit the file in order to "get" a higher score.