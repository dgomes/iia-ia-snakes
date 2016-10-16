# Snake Game Version 1.0 
# Initially based on the code provided by http://www.virtualanup.com at https://gist.githubusercontent.com/virtualanup/7254581/raw/d69804ce5b41f73aa847f4426098dca70b5a1294/snake2.py
# Diogo Gomes <dgomes@av.it.pt>

import copy
from collections import namedtuple
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
        self.points = 0
    def kill(self):
        self.IsDead = True
        self.agent.IsDead = True
    def point(self, point):
        self.points+=point
        self.agent.points+=point

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

    def generateFood(self):
        if self.foodpos == (0,0):
            self.foodpos=random.randrange(1,self.hortiles),random.randrange(1,self.verttiles)
            while (self.foodpos in self.playerpos or self.foodpos in self.obstacles):
                self.foodpos=random.randrange(1,self.hortiles),random.randrange(1,self.verttiles)

    def playerPos(self):
        pos = random.randrange(1, self.hortiles), random.randrange(1, self.verttiles)
        while (pos in self.obstacles):
            pos = random.randrange(1, self.hortiles), random.randrange(1, self.verttiles)
        return pos
    
    def setObstacles(self,level):
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

    def setPlayers(self,players):
        self.players=[]
        colors = [c for c in constants.colours if c not in [self.obscolor, self.foodcolor]]
        for p in players:
            c = random.choice(colors)
            colors.remove(c)
            self.players+=[Player(p,c)]
        self.dead=[]

    def printstatus(self):
        PlayerStat = namedtuple('PlayerStat', 'name color points')
        players = [PlayerStat(p.name, p.color, p.points) for p in self.players + self.dead]
       
        score = "{} vs {}".format(players[0].points, players[1].points)
        text = self.font.render(score, 1,(255,255,255))
        textpos = text.get_rect(centerx=self.screen.get_width()/2,y=(self.verttiles+1)*self.tilesize)


        player1_name=self.font.render(players[0].name,1,players[0].color)
        player1_pos = player1_name.get_rect(x=self.screen.get_width()/2 - self.font.size(score + players[0].name)[0],y=(self.verttiles+1)*self.tilesize)

        player2_name=self.font.render(players[1].name,1,players[1].color)
        player2_pos = player2_name.get_rect(x=self.screen.get_width()/2 + self.font.size(score)[0],y=(self.verttiles+1)*self.tilesize)
            
        
        self.screen.blit(player1_name, player1_pos)
        self.screen.blit(player2_name, player2_pos)
        self.screen.blit(text, textpos)
      
        text=None
        if len(self.players) == 1:
            text=self.font.render("{} is the Winner!".format(self.players[0].name),1,self.players[0].color)
        elif len(self.players) == 0:
            text=self.font.render("All dead...",1,(255,0,0))
        if text != None:
            textpos = text.get_rect(centerx=self.screen.get_width()/2,centery=self.screen.get_height()/2)
            self.screen.blit(text, textpos)
    
    def updatePlayerInfo(self):
        #update where the players are in the board just before updating the logic
        self.playerpos=[]
        for player in self.players:
            self.playerpos+=player.body

    def update(self,snake):
        if snake.IsDead:
            self.players.remove(snake)
            self.dead.append(snake)
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
            snake.point(10)
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
            self.updatePlayerInfo()
            self.generateFood() #generate food if necessary
            for player in [a for a in self.players if not a.IsDead]:
                maze = Maze(self.obstacles, self.playerpos, self.foodpos)   #just a copy of our information (avoid shameful agents that tinker with the game server)
                player.agent.updateDirection(maze) #update game logic (only for alive players)
                player.agent.update(points=[(a.name, a.points) for a in self.players], mapsize=(self.hortiles, self.verttiles), count=count) #update game logic (only for alive players)
            for player in self.players:
                self.update(player)
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
