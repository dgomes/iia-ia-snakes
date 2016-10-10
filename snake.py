from constants import *

class Snake:
    def __init__(self,body , direction, color,speed):
        self.speed=speed
        self.body=body #initially located here
        self.color=color
        self.direction=self.newdirection=direction
        self.IsDead=False
    def UpdateDirection(self,game):
        self.direction=self.newdirection #the next direction is stored in newdirection....logic is updated here
    def Update(self,game):
        if self.IsDead:
            fadestep=5
            self.color=(max(self.color[0]-fadestep,0),max(self.color[1]-fadestep,0),max(self.color[2]-fadestep,0))
            if self.color[0]==0 and self.color[1]==0 and self.color[2]==0:
                self.color=(0,0,0)
                game.players.remove(self)
        else:
            #updates the snake...
            head=self.body[0]#head of snake
            head=(head[0]+self.direction[0],head[1]+self.direction[1])
            #wrap the snake around the window
            headx=game.hortiles if head[0]<0 else 0 if head[0]>game.hortiles else head[0]
            heady=game.verttiles if head[1]<0 else 0 if head[1]>game.verttiles else head[1]
            head=(headx,heady)
            #update the body and see if the snake is dead
            alivelist=[snake for snake in reversed(game.players) if not snake.IsDead]
            for snake in alivelist:
                if head in snake.body:
                    if head == snake.body[0]:#in case of head to head collision, kill both of the snakes
                        snake.IsDead=True
                    self.IsDead=True
                    return
            if head in game.obstacles:#hit an obstacle
                self.IsDead=True
                return
            elif head == game.foodpos:
                #the snake ate the food
                game.foodpos=0,0
                self.body.append((self.body[0]))
            #the snake hasnot collided....move along
            self.body=[head]+[self.body[i-1] for i in range(1,len(self.body))]
    def Draw(self,screen,game):
        for part in self.body:
            pygame.draw.rect(screen,self.color,(part[0]*game.tilesize,part[1]*game.tilesize,game.tilesize,game.tilesize),0)
    def processkey(self,key):
        pass #nothing to do here


