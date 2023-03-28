#snake game
from tkinter import *
import math
from random import randrange

#fonction for place one part of snake at coord
def place_part(part,coord):
    global wpart
    space_g.coords(part,coord[0]-wpart,coord[1]-wpart,coord[0]+wpart,coord[1]+wpart)

#distance between two point
def distance(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

#fonction for deplace one part of snake
def deplace_ops(coord,vect_dp,s):
    return [coord[0]+s*vect_dp[0],coord[1]+s*vect_dp[1]]

#create one part of snake
def create_op(coord):
    global color,wpart
    return space_g.create_rectangle(coord[0]-wpart,coord[1]-wpart,coord[0]+wpart,coord[1]+wpart,fill = color)

#fonction to create food
def create_food():
    global wpart,xfood,yfood
    xfood = lfoodx[randrange(len(lfoodx))]
    yfood = lfoody[randrange(len(lfoody))]
    return space_g.create_oval(xfood-wpart,yfood-wpart,xfood+wpart,yfood+wpart,fill = "orange")

#fonction to eat food of snake
def eat():
    global xfood,yfood,wpart,food
    if distance([xfood,yfood],snake[0][0]) <= 2*wpart:
        space_g.delete(food)
        food = create_food()
        add_psnake()

#fonction to verify if the snake eat itself
def eat_itself():
    global wpart
    if len(snake)>3 :
        for part in snake[3:]:
            if distance(snake[0][0],part[0])< wpart*2 :
                return True
    return False

#move sanke
def move_snake1():
    global lx,ly
    #conservation of  position
    pos1,pos2 = snake[0][0],snake[0][0]
    snake[0][0] = deplace_ops(snake[0][0],snake[0][1],1)
    place_part(dpart[0],snake[0][0])
    i = 1
    while i<len(snake):
        pos2 = snake[i][0]
        snake[i][0] = pos1
        place_part(dpart[i],snake[i][0])
        pos1 = pos2
        i += 1
    
    lx,ly = deplace_ops(snake[i-1][0],snake[i-1][1],-1)


#deplacement of snake
def deplace_snake():
    move_snake1()
    eat()
    if not (arrest()):
        root.after(150,deplace_snake)

#add one part of snake at last
def add_psnake():
    global lx,ly
    snake.append([[lx,ly],snake[-1][1]])
    dpart.append(create_op(snake[-1][0]))

#fonction to arrest
def arrest():
    global max_size_snake 
    x,y = snake[0][0][0],snake[0][0][1]
    if distance([x,y],[x,hs])<=0 or distance([x,y],[x,0])<=0 or distance([x,y],[ws,y])<=10 or distance([x,y],[0,y])<=10 or len(snake)>max_size_snake:
        return True
    if eat_itself():
        return True
    return False

#fonction for change directions
def fup(event) :
    global direction
    if direction != 4:
        snake[0][1] = [0,-20] 
        direction = 3
    
def fleft(event) :
    global direction
    if direction != 2:
        snake[0][1] = [-20,0] 
        direction = 1

def fright(event) :
    global direction
    if direction !=1:
        snake[0][1] = [20,0]
        direction = 2

def fdown(event) :
    global direction
    if direction != 3:
        snake[0][1] = [0,20]
        direction = 4



#main window
root = Tk()

#space of game
ws = hs = 500
space_g = Canvas(root,width = ws,height = hs,bg = "gray")
root.bind("<Up>",fup)
root.bind("<Left>",fleft)
root.bind("<Right>",fright)
root.bind("<Down>",fdown)

#contrainte of direction
# 1 : left
# 2 : right
# 3 : up
# 4 : down
global direction
direction = 1

#data structure for snake
global color, wpart, max_size_snake
color,wpart = "light blue",10
snake = [[[ws/2,hs/2],[-10,0]]]
max_size_snake = 20

#coord for last position of the last part of snake
global lx,ly
lx,ly = 430,450

#different part of snake
dpart = [create_op(snake[0][0])]
color = "red"

#creation of food
global xfood,yfood,food
lfoodx = []
lfoody = []
for i in range(10,ws,10):
    lfoodx.append(i)
    lfoody.append(i)

food = create_food()

deplace_snake()

#adaptation for space of game
space_g.grid()

#start of gui
root.mainloop()
