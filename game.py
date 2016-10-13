# Snake Game Version 1.0 
# Initially based on the code provided by http://www.virtualanup.com at https://gist.githubusercontent.com/virtualanup/7254581/raw/d69804ce5b41f73aa847f4426098dca70b5a1294/snake2.py
# Diogo Gomes <dgomes@av.it.pt>

import copy
from sys import exit
import pygame,random
from pygame.locals import *
import constants
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
      
class Maze:
    def __init__(self, o, p, f):
        self.obstacles = copy.deepcopy(o)
        self.playerpos = copy.deepcopy(p)
        self.foodpos = copy.deepcopy(f)

class Player:
    def __init__(self, agent, color=(255,0,0)):
        self.agent = agent 
        self.body = agent.body 
        self.name = agent.name
        self.color = color 
        self.IsDead = False
    def kill(self):
        self.IsDead = True
        self.agent.IsDead = True

class SnakeGame:
    def __init__(self, hor=60, ver=40, tilesize=20, fps=50):
        #create the window and do other stuff
        pygame.init()
        self.tilesize=tilesize  #tile size, adjust according to screen size
        self.hortiles=hor   #number of horizontal tiles
        self.verttiles=ver  #number of vertical tiles
        self.screen = pygame.display.set_mode(((self.hortiles+1)*self.tilesize,(self.verttiles+1)*self.tilesize+25))
        pygame.display.set_caption('Python Snake')
        
        #load the font
        self.font = pygame.font.Font(None, 30)
        self.obstacles=[]
        self.obscolor=(139,69,19)
        self.foodcolor=(0,255,0)
        self.foodpos=(0,0)
        self.fps=fps #frames per second. The higher, the harder

    def GenerateFood(self):
        if self.foodpos == (0,0):
            self.foodpos=random.randrange(1,self.hortiles),random.randrange(1,self.verttiles)
            while (self.foodpos in self.playerpos or self.foodpos in self.obstacles):
                self.foodpos=random.randrange(1,self.hortiles),random.randrange(1,self.verttiles)

    def SetObstacles(self,level):
        for i in range(1,level+1):
            lo=random.randrange(1,self.hortiles),random.randrange(1,self.verttiles) #last obstacle
            self.obstacles.append(lo)
            for j in range(1,random.randint(1,int(level/2))):
                if random.randint(1,2) == 1:
                    lo=(lo[0]+1,lo[1])
                else:
                    lo=(lo[0],lo[1]+1)
                if 0<lo[0]<=self.hortiles and 0<lo[1]<=self.verttiles :
                    self.obstacles.append(lo)

    def setplayers(self,players):
        self.players=[Player(p,random.choice(constants.colours)) for p in players]
    
    def printstatus(self):
        if len(self.players) >1:
            players = [p.name for p in self.players]
        
            text=self.font.render(players[0],1,self.players[0].color)
            textpos = text.get_rect(x=self.tilesize,y=(self.verttiles+1)*self.tilesize)
            self.screen.blit(text, textpos)
            text=self.font.render(players[1],1,self.players[1].color)
            textpos = text.get_rect(x=self.screen.get_width()-self.tilesize-self.font.size(players[1])[0],y=(self.verttiles+1)*self.tilesize)
            self.screen.blit(text, textpos)
            
            text = self.font.render("{} vs {}".format(players[0], players[1]), 1,(255,255,255))
        elif len(self.players) >0:
            text=self.font.render("{} is the Winner!".format(self.players[0].name),1,self.players[0].color)
        else:
            text=self.font.render("All dead...",1,(255,0,0))
        textpos = text.get_rect(centerx=self.screen.get_width()/2,y=(self.verttiles+1)*self.tilesize)
        self.screen.blit(text, textpos)
    
    def UpdatePlayerInfo(self):
        #update where the players are in the board just before updating the logic
        self.playerpos=[]
        for player in self.players:
            self.playerpos+=player.body

    def Update(self,snake):
        if snake.IsDead:
            self.players.remove(snake)
            logging.info("Player <{}> is dead".format(snake.name))
            return
        #updates the snake...
        head=snake.body[0]#head of snake
        head=(head[0]+snake.agent.direction[0],head[1]+snake.agent.direction[1])
        #wrap the snake around the window
        headx=self.hortiles if head[0]<0 else 0 if head[0]>self.hortiles else head[0]
        heady=self.verttiles if head[1]<0 else 0 if head[1]>self.verttiles else head[1]
        head=(headx,heady)
        #update the body and see if the snake is dead
        alivelist=[alive for alive in reversed(self.players) if not alive.IsDead]
        for alive in alivelist:
            if head in alive.body:
                if head == alive.body[0]:#in case of head to head collision, kill both of the snakes
                    alive.kill()
                snake.kill()
                return
        if head in self.obstacles:#hit an obstacle
            snake.kill()
            return
        elif head == self.foodpos:
            #the snake ate the food
            self.foodpos=0,0
            snake.body.append((snake.body[0]))
        #the snake hasnot collided....move along
        snake.body=[head]+snake.body[:-1]

        snake.agent.body = copy.deepcopy(snake.body)
    def start(self):
        clock = pygame.time.Clock()
        count=0
        while True:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == QUIT or event.type == pygame.KEYDOWN and event.key == K_q: #close window or press Q
                    pygame.quit();
                    exit()
                elif event.type == pygame.KEYDOWN:
                    for player in self.players:
                        player.agent.processkey(event.key)
            count+=1
            self.screen.fill((0,0,0))
            #game logic is updated in the code below
            self.UpdatePlayerInfo()
            self.GenerateFood() #generate food if necessary
            for player in [a for a in self.players if not a.IsDead]:
                maze = Maze(self.obstacles, self.playerpos, self.foodpos)   #just a copy of our information (avoid shameful agents that tinker with the game server) 
                player.agent.UpdateDirection(maze) #update game logic (only for alive players)
            for player in self.players:
                self.Update(player)
            #print all the content in the screen
            for player in self.players: #print players
                for part in player.body:
                    pygame.draw.rect(self.screen, player.color, (part[0]*self.tilesize,part[1]*self.tilesize,self.tilesize,self.tilesize),0)

            for obstacle in self.obstacles: #print obstacles
                pygame.draw.rect(self.screen,self.obscolor,(obstacle[0]*self.tilesize,obstacle[1]*self.tilesize,self.tilesize,self.tilesize),0)

            #print food
            pygame.draw.rect(self.screen,self.foodcolor,(self.foodpos[0]*self.tilesize,self.foodpos[1]*self.tilesize,self.tilesize,self.tilesize),0)
            self.printstatus()
            pygame.display.update()
