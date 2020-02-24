import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
dirnx=0
dirny=0
class cube (object):
    rows=20
    w=500
    def __init__(self,start,color=(255,0,0)):
        self.pos=start
        self.dirnx=0
        self.dirny=0
        self.color=color
        
    def move(self,dirnx,dirny):
        self.dirnx=dirnx
        self.dirny=dirny
        self.pos = ( self.pos[0] +self.dirnx ,self.pos[1]+self.dirny)
    def draw(self,surface,eyes=False ):
        dis= self.w//self.rows
        i=self.pos[0]
        j=self.pos[1]
        pygame.draw.rect(surface,self.color,(i*dis+1,j*dis+1,dis-2,dis-2))# (x,y) h w
        # draw eyes of the snake 
        if eyes :
            centre=dis//2
            radius=3
            circleMiddle=(i*dis + centre- radius ,j*dis+8)
            circleMiddle2=(i*dis + dis - radius*2 ,j*dis+8)
            pygame.draw.circle(surface,(0,0,0),circleMiddle,radius)
            pygame.draw.circle(surface,(0,0,0),circleMiddle2,radius)
            
class snake (object):
    body=[] # empty list
    turns={}#empty dic
    
    def __init__(self,color,pos):
        self.color=color
        self.head=cube(pos)
        self.body.append(self.head)
        #direction
        self.dirnx= 0
        self.dirny= 1
        
    def move(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            keys=pygame.key.get_pressed() # get  if  thers  any key pressed 
        
            for key in keys :
                if (keys[pygame.K_f] ==1):
                    #head mouvment .
                    self.dirnx= -1
                    self.dirny= 0
                    #rest of the body mouvment 
                    self.turns[self.head.pos[:]]=[self.dirnx,self.dirny]
                elif (keys[pygame.K_h] == 1):
                    #head mouvment 
                    self.dirnx= 1
                    self.dirny= 0
                    #rest of the body mouvment 
                    self.turns[self.head.pos[:]]=[self.dirnx,self.dirny]
                elif( keys[pygame.K_t] == 1):
                    #head mouvment 
                    self.dirnx= 0
                    self.dirny= -1
                    #rest of the body mouvment 
                    self.turns[self.head.pos[:]]=[self.dirnx,self.dirny]
                elif( keys[pygame.K_g] == 1):
                    #head mouvment 
                    self.dirnx= 0
                    self.dirny= 1
        #rest of the body mouvment 
                    self.turns[self.head.pos[:]]=[self.dirnx,self.dirny]
        for i,c in enumerate(self.body):
            p=c.pos[:] # just a copy postion of cube
            if p in self.turns:
                turn=self.turns[p] #turn dir of that cube
                c.move(turn[0],turn[1])
                if i==len(self.body)-1: # if  we  re in the  last cube of snake 
                    self.turns.pop(p) # remove the move
                #check edge of thee screen
            else:
                if c.dirnx==-1 and  c.pos[0]<=0 : c.pos=(c.rows-1,c.pos[1])
                elif c.dirnx==1 and  c.pos[0]>=c.rows-1 : c.pos=(0,c.pos[1])
                elif c.dirny==1 and  c.pos[1]>=c.rows-1 : c.pos=(c.pos[0],0)
                elif c.dirny==-1 and  c.pos[1]<=0 : c.pos=(c.pos[0],c.rows-1)
                else : c.move(c.dirnx,c.dirny)      
        
    def reset (self ,pos):
        self.head=cube(pos)
        self.body=[]
        self.body.append(self.head)
        self.turn={}
        self.dirnx= 0
        self.dirny= 1
        
        
    def addCube(self):
        tail=self.body[-1] #chek the position of  last cube in snake
        dx, dy=tail.dirnx,tail.dirny
        #chaekin the postion of adding the  snack to th snake  body
        if dx==1 and dy==0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx==-1 and dy==0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx==0 and dy==1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx==0 and dy==-1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
        #keep the same dir of mov of the snake for the new cube 
        self.body[-1].dirnx=dx
        self.body[-1].dirny=dy
        
    def draw(self,surface):
        for i, c in enumerate (self.body):
            if i==0:
                c.draw(surface,True) #head of snake 
            else:
                c.draw(surface)
            
        
def drawGrid(w,rows,surface):
    sizeBtwn= w // rows
    x=0
    y=0
    for l in range(rows):
        x=x+sizeBtwn
        y=y+sizeBtwn
        
        pygame.draw.line(surface,(255,255,255),(x,0),(x,w))
        pygame.draw.line(surface,(255,255,255),(0,y),(w,y ))
def redrawWindow(surface):
    global rows,width,s,snack
    surface.fill((0,0,0)) #Screnn cloor
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width,rows,surface)
    pygame.display.update()
    
        
def randomSnack (rows ,item): #cube  for  snacke to eat
       
        positions =item.body
        while True :
            x = random.randrange(rows)
            y = random.randrange(rows)
            if len (list(filter( lambda z:z.pos == (x,y),positions )))> 0:# chek if  snack postion an snake position 
                continue
            else :
                break
        return (x,y)
def message_box(subject,content):
        root=tk.Tk()
        root.attributes("-topmost",True)# be in top of any thing in pc screen
        root.withdraw() #be invis
        messagebox.showinfo(subject,content)
        try:
            root.destroy()
        except:
            pass
def main():
    global width,rows,s,snack
    width=500
    height=500
    rows=20
    win=pygame.display.set_mode((width,width))
    s=snake((255,0,0),(10,10))
    snack=cube(randomSnack (rows ,s),(0,255,0))
    flag=True
    clock=pygame.time.Clock()
    while flag:
        pygame.time.delay(50) # delay of 50 ms
        clock.tick(10) # snake can move 10 blocks in 1s
        #movement of the snake
        s.move()
        #chek if  head of  snake  hit the snack
        if s.body[0].pos==snack.pos:
            s.addCube()
            snack=cube(randomSnack (rows ,s),(0,255,0))
        for x in range(len(s.body)):
            #chek collusion
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                #print("Score:  ",len(s.body))
                message_box("You lost","Play again your Score: "+str(len(s.body)))
                s.reset((10,10))
                break
                
            
        redrawWindow(win)
        pass
        
    
main()
