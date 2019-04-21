#Chain Reaction
#Samuel Jeyaseelan
#11 A
#Roll no: 38
'''
Chain Reaction is a grid and turn-based game where each player has a particular colour and the backgroung colour indicates the player's turn.
In each turn a player can place an orb in a cell: either an empty one, or a cell that already has on orb of that colour.
If a cell contains too many orbs, it explodes/splits in surrounding cells, claiming those cells and the orbs in them for that colour.
A colour/player wins if there is only his/her coloured orbs in the whole grid.

Game can be played by two-eight players.
There is an undo button which goes back one turn.
'''

import pygame,sys
from pygame.locals import *
import os
import time
pygame.init()
FPS=15
fpsclock=pygame.time.Clock()
surf=pygame.display.set_mode((600,600))
pygame.display.set_caption('CHAIN REACTION')
#_____________________________________________________________________________________________________________________________________________________________________
#Some colour constants
GRAY     = (160, 160, 160)
VOYAGER  = ( 89, 205, 238)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)
#_____________________________________________________________________________________________________________________________________________________________________

WIDTH=7
HEIGHT=9
BOX_HEIGHT=BOX_WIDTH=50
HALF=(BOX_HEIGHT)/2
GAP=5
NUMBER_OF_TURNS=4
COLOURS=[RED,GREEN,BLUE,YELLOW,CYAN,GRAY,ORANGE,PURPLE]
colour_dict={RED:'RED',GREEN:'GREEN',BLUE:'BLUE',YELLOW:'YELLOW',
             CYAN:'CYAN',GRAY:'GRAY',ORANGE:'ORANGE',PURPLE:'PURPLE'}
Direction={'up':(0,-HALF),'down':(0,HALF),'left':(-HALF,0) ,'right':(HALF,0)} 

font1=pygame.font.SysFont('Calibri',36,True,False)
font2=pygame.font.SysFont('Calibri',38,True,False)
font3=pygame.font.SysFont('Calibri',20,True,False)
font4=pygame.font.SysFont('kitchenpolice',30,True,False)
font5=pygame.font.SysFont('tahoma',15,True,False)

undo=pygame.image.load('undo.png')
p2=pygame.image.load('2p.png')
p3=pygame.image.load('3p.png')
p4=pygame.image.load('4p.png')
p5=pygame.image.load('5p.png')
p6=pygame.image.load('6p.png')
p7=pygame.image.load('7p.png')
p8=pygame.image.load('8p.png')
arrow=pygame.image.load('arrow.jpg')
arrow2=pygame.image.load('arrow2.jpg')
tick=pygame.image.load('tick.jpg')
startpic=pygame.image.load('s.jpg')
home=pygame.image.load('home2.jpg')
cr=pygame.image.load('cr.png')
title=pygame.image.load('title.png')
won=pygame.image.load('won.jpg')
winner=pygame.image.load('victory.png')
inst=pygame.image.load('inst.png')
pygame.display.set_icon(cr)
#_____________________________________________________________________________________________________________________________________________________________________
#Basic drawing functions used in the game

def draw_circle(colour,x,y,number,direction=None):
    '''Draws 1,2,3 or 4 orbs'''
    if not(direction):
        if number == 1:
            pygame.draw.circle(surf,colour,(x,y),10)
        elif number == 2:
            pygame.draw.circle(surf,colour,(x-7,y),10)
            pygame.draw.circle(surf,BLACK,(x+7,y),11)
            pygame.draw.circle(surf,colour,(x+7,y),10)
        elif number == 3:
            pygame.draw.circle(surf,colour,(x-7,y),10)
            pygame.draw.circle(surf,BLACK,(x+7,y+8),11)
            pygame.draw.circle(surf,colour,(x+7,y+8),10)        
            pygame.draw.circle(surf,BLACK,(x+7,y-8),11)
            pygame.draw.circle(surf,colour,(x+7,y-8),10)
        else:
            pygame.draw.circle(surf,colour,(x-7,y+8),10)
            pygame.draw.circle(surf,BLACK,(x+7,y+8),11)
            pygame.draw.circle(surf,colour,(x+7,y+8),10)
            pygame.draw.circle(surf,BLACK,(x-7,y-8),11)
            pygame.draw.circle(surf,colour,(x-7,y-8),10)
            pygame.draw.circle(surf,BLACK,(x+7,y-8),11)
            pygame.draw.circle(surf,colour,(x+7,y-8),10)
    else:
         for dirn in direction:
             xplus=Direction[dirn][0]
             yplus=Direction[dirn][1]
             pygame.draw.circle(surf,BLACK,(x+xplus,y+yplus),11)
             pygame.draw.circle(surf,colour,(x+xplus,y+yplus),10)

def draw_square(x,y):
    pygame.draw.rect(surf,BLACK,(x,y,BOX_WIDTH,BOX_HEIGHT))

def make_button(x,y,text):
    textsurf=font3.render(text,True,BLACK,VOYAGER)
    textrect=textsurf.get_rect()
    textrect.topleft=(x,y)
    return textsurf,textrect
#______________________________________________________________________________________________________________________________________________________________________

#Matrix is a 2-D list containing the number of orbs in each cell
#Colour_matrix is a 2-D list containing the colours of each cell
#Direction_matrix is another 2-D list that tracks the directions in which a cell will split
# Eg:The top left corner cell will split(if at all) only to it's left and bottom.

#Other important functions
def startnew(k):
    '''Changes values of all game variables back to original state'''
    matrix=[[0 for col in range(WIDTH)] for row in range(HEIGHT)]
    Colour_matrix=[[None for col in range(WIDTH)] for row in range(HEIGHT)]
    max_value=[[3 for col in range(WIDTH)] for row in range(HEIGHT)]
    max_value[0][0]=max_value[0][WIDTH-1]=1
    max_value[HEIGHT-1][0]=max_value[HEIGHT-1][WIDTH-1]=1
    max_value[0][1:WIDTH-1]=max_value[HEIGHT-1][1:WIDTH-1]=[2]*(WIDTH-2)
    for i in range(1,HEIGHT-1):
        max_value[i][0]=max_value[i][WIDTH-1]=2
    NUMBER_OF_TURNS = k
    COLOUR=COLOURS[:NUMBER_OF_TURNS]
    turns_left=k
    turn=0
    All_played=False
    direction_matrix=[[None for col in range(WIDTH)] for row in range(HEIGHT)]

    return matrix,Colour_matrix,max_value,direction_matrix,NUMBER_OF_TURNS,COLOUR,turns_left,turn,All_played
    
[matrix,Colour_matrix,max_value,direction_matrix,NUMBER_OF_TURNS,COLOUR,turns_left,turn,All_played]=startnew(4)

def check(matrix):
    ''' Checks whether all squares won't split'''
    for row in range(HEIGHT):
        for col in range(WIDTH):
            if matrix[row][col]>max_value[row][col]:
                return False
            
    return True

def find_direction(index):
    ''' Returns possible directions to move to another box in the grid'''
    Dict={(index[0]-1,index[1]):'up',(index[0]+1,index[1]):'down',(index[0],index[1]-1):'left',(index[0],index[1]+1):'right'}
    dirn=[]
    for row,col in Dict.keys():
        if col in range(0,WIDTH) and row in range(0,HEIGHT):
            dirn.append(Dict[(row,col)])
    return dirn

def update1(matrix,splitlist):
    #Splitlist is a list of all indices that are in half-animation state
    for index in splitlist:
        row,col=index
        direction_matrix[row][col]=find_direction(index)
    return matrix,splitlist,direction_matrix

def surround(index):
    '''Returns a list of the indices above, below, to the left and right of it '''
    around=[(index[0]-1,index[1]),(index[0]+1,index[1]),(index[0],index[1]-1),(index[0],index[1]+1)]
    surr=[]
    for row,col in around:
        if col in range(0,WIDTH) and row in range(0,HEIGHT):
            surr.append((row,col))
    return surr

def update2(matrix,splittinglist):
    #splittinglist is a list of indices that have an extra circle/orb and will burst
    for index in splittinglist:
        row,col=index
        matrix[row][col]=0   #Since that box will burst
        direction_matrix[row][col]=None
        colour=Colour_matrix[row][col]
        surr=surround(index)
        for ind in surr:
            r,c=ind
            matrix[r][c]+=1   #Since surrounding boxes get one more circle
            Colour_matrix[r][c]=colour #Since colour gets transferred
            if matrix[r][c] > max_value[r][c]:  
                if ind not in splittinglist:
                    splittinglist.append(ind)  #Since that index will burst     
        splittinglist.remove(index)    #Since that index has been taken care of
    return matrix,splittinglist
        
def is_colour_present(colour):
    '''Returns false if the colour is not present'''
    for row in Colour_matrix:
        if colour in row:
            return True
    return False

def draw_board(matrix,Colour_matrix):
    '''Draws the grid and orbs'''
    for column in range(WIDTH):
        for row in range(HEIGHT):
            colour=Colour_matrix[row][column]
            num=matrix[row][column]
            x= ((column+1)*GAP) + (column*BOX_WIDTH)
            y=((row+1)*GAP) + (row*BOX_HEIGHT)
            draw_square(x,y)
            if num:   #Non-zero
                if direction_matrix[row][column]==None:
                    draw_circle(colour,x+(BOX_WIDTH/2) ,y+(BOX_HEIGHT/2) ,num)
                else:
                    draw_circle(colour,x+(BOX_WIDTH/2) ,y+(BOX_HEIGHT/2) ,num,direction_matrix[row][column])

def mouseonbox(mousex,mousey):
    '''Tests whether the mouse is on a cell'''
    GHEIGHT=GAP + BOX_HEIGHT
    GWIDTH=GAP + BOX_WIDTH
    if (GAP<=(mousex%(GWIDTH))<=(GWIDTH)) and mousex<(GWIDTH*WIDTH):
        if (GAP<=(mousey%(GHEIGHT))<=(GHEIGHT)) and mousey<(GHEIGHT*HEIGHT):
            return True
    return False

def blitbuttons():
    for i in button_list:
        surf.blit(i,POSITION[i])

def store_undo():
    '''Stores values for undo button'''
    global matrix,Colour_matrix,splitlist,turn,COLOUR,NUMBER_OF_TURNS,turns_left,All_played,direction_matrix
    global Umatrix,UColour_matrix,Usplitlist,Uturn,UCOLOUR,UNUMBER_OF_TURNS,Uturns_left,UAll_played,Udirection_matrix

    Udirection_matrix=[y[:] for y in direction_matrix]
    Umatrix = [x[:] for x in matrix]
    UColour_matrix = [x[:] for x in Colour_matrix]
    Usplitlist = list(splitlist)
    Uturn = turn
    UCOLOUR = list(COLOUR)
    UNUMBER_OF_TURNS=NUMBER_OF_TURNS
    Uturns_left = turns_left
    UAll_played = All_played

def win_text():
    '''Displays victory text after game is over'''
    surf2=surf.convert_alpha()
    pygame.draw.rect(surf2,(250,250,250,100),(0,0,450,600))
    surf.blit(surf2,(0,0))
    pygame.draw.rect(surf,BLACK,(0,240,450,50))
    surf.blit(won,(20,240))
    surf.blit(winner,(0,500))
    clr=COLOUR[0]
    clr=colour_dict[clr]
    text1=font1.render(clr + ' HAS WON',True,WHITE)
    surf.blit(text1,[150,250])
#_____________________________________________________________________________________________________________________________________________________________
playsurf = font4.render(' PLAY ',True,GREEN,BLACK)
playrect = playsurf.get_rect(topleft=(50,500))
instructionsurf = font4.render(' INSTRUCTIONS ',True,GREEN,BLACK)
instructionrect = instructionsurf.get_rect(topleft=(50,550))

#Home and instruction pages:

def instructions((mousex,mousey),swap):
    '''Instructions page'''
    
    surf.fill(BLACK)
    surf.blit(cr,(130,40))
    pygame.draw.rect(surf,(83,83,121),(0,390,600,90))
    surf.blit(inst,(0,0))
    s="""The objective of Chain Reaction is to take control of the board by
eliminating your opponents' orbs.
Players take turns to place their orbs in a cell. Once a cell has reached
critical mass the orbs explode into the surrounding cells adding an extra
orb and claiming the cell for the player.
A player may only place their orbs in a blank cell or a cell that contains
orbs of their own colour.
As soon as a player looses all their orbs they are out of the game.

CRITICAL MASS:
CORNER:                    EDGE:                        MIDDLE:
Splits at 2 orbs       Splits at 3 orbs      Splits at 4 orbs """
    i=1
    for line in s.split('\n'):
        instructionsurf = font5.render(line,True,GREEN,BLACK)
        instructionrect = instructionsurf.get_rect(topleft=(10,30*i+10))
        surf.blit(instructionsurf,instructionrect)
        i+=1

    surf.blit(playsurf,playrect)
    surf.blit(home,(400,500))
    homerect=home.get_rect(topleft=(400,500))

    box_positions=[(50,410),(175,410),(300,410)]
    direct=[['right','down'],['right','left','down'],['up','down','left','right']]
    number =2
    if 0<=(swap%30)<=15:    
        for k in box_positions:
            pygame.draw.rect(surf,BLACK,k+(BOX_WIDTH,BOX_WIDTH))
            x1,y1=k[0]+HALF,k[1]+HALF
            draw_circle(RED,x1,y1,number)
            number+=1
    else:
        number=2
        for k in box_positions:
            pygame.draw.rect(surf,BLACK,k+(BOX_WIDTH,BOX_WIDTH))
            x1,y1=k[0]+HALF,k[1]+HALF
            draw_circle(RED,x1,y1,number,direct[number-2])
            number+=1
    
    mx,my = pygame.mouse.get_pos()
    if homerect.collidepoint(mousex,mousey):
        hi = True
    else:
        hi = False
    if homerect.collidepoint(mx,my):
        pygame.draw.rect(surf,RED,(400,500,63,63),1)
    return hi


def display_start():
    surf.fill(BLACK)
    surf.blit(startpic,(0,0))
    surf.blit(playsurf,playrect)
    surf.blit(instructionsurf,instructionrect)
    surf.blit(title,(0,0))

    
def start():
    '''Home page'''
    hi=True
    swap=0
    while True:
        swap+=1
        mousex,mousey=0,0
        clicked=False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                clicked = True
                mousex,mousey = event.pos
                
        mx,my=pygame.mouse.get_pos()
        if hi == True:
            display_start()
            if instructionrect.collidepoint(mx,my):
                surf.blit(arrow2,(10,550))
        else:
            hi = instructions((mousex,mousey),swap)
            
        if playrect.collidepoint(mousex,mousey):
            break
        elif instructionrect.collidepoint(mousex,mousey):
            hi = False

        if playrect.collidepoint(mx,my):
            surf.blit(arrow2,(10,500))
         
        pygame.display.update()
        fpsclock.tick(FPS)
    return

def remove_player(COLOUR,turns_left,turn):
    '''Handles when one colour is eliminated'''
    for colr in COLOUR:
        if is_colour_present(colr)==False:
            if COLOUR.index(colr)<turn:
                COLOUR.remove(colr)
                turns_left-=1
                turn -= 1
            else:
                COLOUR.remove(colr)
                turns_left-=1
    return COLOUR,turns_left,turn

def board_update():
    draw_board(matrix,Colour_matrix)
    blitbuttons()
    time.sleep(0.05)
    pygame.display.update()
#____________________________________________________________________________________________________________________________________________________________________        
surf.fill(BLACK)

#Initializing game variables
turn = 0
turns_left=NUMBER_OF_TURNS
All_played=False
COLOUR=COLOURS[:NUMBER_OF_TURNS]
splitlist=[]
button_clicked=None

player_button_list=[p2,p3,p4,p5,p6,p7,p8]
button_list=[home,undo,p2,p3,p4,p5,p6,p7,p8]
POSITION = {home:(490,500),undo:(490,450),p2:(490,100),p3:(490,140),p4:(490,180),p5:(490,220),p6:(490,260),p7:(490,300),p8:(490,340)}

Udirection_matrix=[y[:] for y in direction_matrix] 
Umatrix = [x[:] for x in matrix]
UColour_matrix = [x[:] for x in Colour_matrix]
Uturn = turn
UCOLOUR = list(COLOUR)
UNUMBER_OF_TURNS=NUMBER_OF_TURNS
Uturns_left=turns_left
UAll_played=All_played
Usplitlist=[]

start()

#GAME LOOP:
while True:
    mousex,mousey=0,0
    turn_colour=COLOUR[turn]
    surf.fill(turn_colour)
    pygame.draw.rect(surf,BLACK,(450,0,200,600))
    
    clicked=False
    for event in pygame.event.get():
        '''Checking for click and quit events'''
        if event.type==QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type==MOUSEBUTTONUP:
            mousex,mousey=event.pos
            clicked=True

                
    if mouseonbox(mousex,mousey) and (len(COLOUR)<>1):
        '''Handles if user clicks on a cell'''
        store_undo()
        #Getting box at mouse position
        box_x= mousex//(GAP + BOX_WIDTH)
        box_y=mousey//(GAP + BOX_HEIGHT)
        splitlist=[(box_y,box_x)]
        if matrix[box_y][box_x]:
            if Colour_matrix[box_y][box_x] != turn_colour:
                continue
        matrix[box_y][box_x] += 1
        Colour_matrix[box_y][box_x] = turn_colour
    else:
        clicked=False
        '''handles if button has been clicked'''
        k=2
        for i in player_button_list:
            player_button_rect=i.get_rect(topleft=POSITION[i])
            if player_button_rect.collidepoint(mousex,mousey):
                button_clicked=i
                [matrix,Colour_matrix,max_value,direction_matrix,NUMBER_OF_TURNS,COLOUR,turns_left,turn,All_played] = startnew(k)
                break
            k+=1
        else:
            '''Handling undo button'''
            undorect = undo.get_rect(topleft=POSITION[undo])
            homerect = home.get_rect(topleft=POSITION[home])
            if undorect.collidepoint(mousex,mousey):
                draw_board(matrix,Colour_matrix)
                blitbuttons()
                direction_matrix=[y[:] for y in Udirection_matrix]
                matrix = [x[:] for x in Umatrix]
                Colour_matrix = [x[:] for x in UColour_matrix]
                splitlist = list(Usplitlist)
                turn = Uturn
                COLOUR = list(UCOLOUR)
                NUMBER_OF_TURNS = UNUMBER_OF_TURNS                
                turns_left=Uturns_left
                All_played=UAll_played

            elif homerect.collidepoint(mousex,mousey):
                start()
                surf.fill(BLACK)

                
    if button_clicked:
        x,y=POSITION[button_clicked]
        surf.blit(tick,(x-37,y))

    
    mx,my=pygame.mouse.get_pos()
    for i in button_list:
        button_rect=i.get_rect(topleft=POSITION[i])
        if button_rect.collidepoint(mx,my):
            x,y=POSITION[i]
            surf.blit(arrow,(x-30,y))

            
    while True:               
        if not(check(matrix)):   #Loop iterates as long as some cell is splitting
            if len(COLOUR)==1:                                                 
                draw_board(matrix,Colour_matrix)
                blitbuttons()
                break
            matrix,splittinglist,direction_matrix=update1(matrix,splitlist)
            board_update()
            surf.fill(turn_colour)
            pygame.draw.rect(surf,BLACK,(450,0,200,600))
            matrix,splitlist=update2(matrix,splittinglist)
            board_update()
            if All_played:
                COLOUR,turns_left,turn=remove_player(COLOUR,turns_left,turn)
        else:
            draw_board(matrix,Colour_matrix)
            blitbuttons()
            break

    if All_played:
        '''Once each player has started, handles if player is eliminated'''
        COLOUR,turns_left,turn=remove_player(COLOUR,turns_left,turn)
            
    if len(COLOUR)==1:
        '''Handles when player has won'''
        win_text()
        
    if clicked == True:
        '''Changing turns'''
        turn +=1
        if turn == NUMBER_OF_TURNS: #Each player has played once
            All_played=True
    turn = turn%(turns_left)
    
    pygame.display.update()
    fpsclock.tick(FPS)
#_______________________________________________________________________________________________________________________________________________________________
