# Snake Game Version 1.0 
# Based on the code provided by http://www.virtualanup.com at https://gist.githubusercontent.com/virtualanup/7254581/raw/d69804ce5b41f73aa847f4426098dca70b5a1294/snake2.py

from human import HumanSnake
from agent1 import ComputerSnake
from constants import *
       
class SnakeGame:
    tilesize=20
    hortiles=60
    verttiles=40
    def __init__(self):
        #create the window and do other stuff
        pygame.init()
        self.screen = pygame.display.set_mode(((self.hortiles+1)*self.tilesize,(self.verttiles+1)*self.tilesize+25))
        pygame.display.set_caption('Python Snake')
        
        #load the font
        self.font = pygame.font.Font(None, 30)
        self.obstacles=[]
        self.obscolor=(0,0,255)
        self.foodcolor=(0,255,255)
        self.foodpos=(0,0)
        self.playercount=0

    def GenerateFood(self):
        if(self.foodpos == (0,0)):
            self.foodpos=random.randrange(1,self.hortiles),random.randrange(1,self.verttiles)
            while (self.foodpos in self.playerpos or self.foodpos in self.obstacles):
                self.foodpos=random.randrange(1,self.hortiles),random.randrange(1,self.verttiles)

    def SetObstacles(self,level):
        for i in range(1,level+1):
            lo=random.randrange(1,self.hortiles),random.randrange(1,self.verttiles) #last obstacle
            self.obstacles.append(lo)
            for j in range(1,random.randint(1,int(level/2))):
                if(random.randint(1,2) == 1):
                    lo=(lo[0]+1,lo[1])
                else:
                    lo=(lo[0],lo[1]+1)
                if( 0<lo[0]<=self.hortiles and 0<lo[1]<=self.verttiles ):
                    self.obstacles.append(lo)

    def setplayers(self,players):
        self.playercount+=len(players)
        self.players=players
    
    def printstatus(self):
        if(len(self.players) >0):
            text = self.font.render(str(len(self.players))+" players playing", 1,(255,255,255))
        else:
            text=self.font.render("All players dead....press c for new computer snake or h for new human snake",1,(255,0,0))
        textpos = text.get_rect(centerx=self.screen.get_width()/2,y=(self.verttiles+1)*self.tilesize)
        self.screen.blit(text, textpos)
    
    def UpdatePlayerInfo(self):
        #update where the players are in the board just before updating the logic
        self.playerpos=[]
        for player in self.players:
            self.playerpos+=player.body
    def start(self):
        clock = pygame.time.Clock()
        count=0
        while True:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit();
                    exit()
                elif event.type == pygame.KEYDOWN:
                    for player in self.players:
                        player.processkey(event.key)
                    if event.key == K_h:
                        pass
                        self.players.append(HumanSnake())
                        self.playercount+=1
                    elif event.key == K_c:
                        pass
                        self.players.append(ComputerSnake())
                        self.playercount+=1
            count+=1
            self.screen.fill((0,0,0))
            #game logic is updated in the code below
            self.UpdatePlayerInfo()
            self.GenerateFood() #generate food if necessary
            for player in [a for a in self.players if not a.IsDead]:
                player.UpdateDirection(self) #update game logic (only for alive players)
            for player in self.players:
                player.Update(self)
            #print all the content in the screen
            for player in self.players:
                player.Draw(self.screen,self)
            for obstacle in self.obstacles:
                pygame.draw.rect(self.screen,self.obscolor,(obstacle[0]*self.tilesize,obstacle[1]*self.tilesize,self.tilesize,self.tilesize),0)
            pygame.draw.rect(self.screen,self.foodcolor,(self.foodpos[0]*self.tilesize,self.foodpos[1]*self.tilesize,self.tilesize,self.tilesize),0)
            self.printstatus()
            pygame.display.update()
#start the game
if(__name__ == "__main__"):
    snake=SnakeGame()
    snake.SetObstacles(50) #level of obstacles
    snake.setplayers([  
    #HumanSnake([(12,14)])
    #,ComputerSnake(),
    #ComputerSnake([(17,14)]*2,up)
    ])
    snake.start()
