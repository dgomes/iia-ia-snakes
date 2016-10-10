from snake import Snake
from constants import *

class HumanSnake(Snake):
    def __init__(self,body=[(0,0)] , direction=(1,0),upkey=K_UP,downkey=K_DOWN,rightkey=K_RIGHT,leftkey=K_LEFT,color=(0,255,0)):
        super().__init__(body,direction,color,1)#speed is always 1
        #assign the keys to control the human snake
        self.upkey=upkey
        self.downkey=downkey
        self.rightkey=rightkey
        self.leftkey=leftkey
        
    def processkey(self,key):
        #we check the old direction not the new direction.
        if key==self.upkey:
            if self.direction != down:
                self.newdirection=up
        elif key==self.downkey:
            if self.direction != up:
                self.newdirection=down
        elif key==self.rightkey:
            if self.direction != left:
                self.newdirection=right
        elif key==self.leftkey:
            if self.direction != right:
                self.newdirection=left


