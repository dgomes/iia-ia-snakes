from snake import Snake
from constants import *
from websocket import create_connection
import json
import pygame
import logging
import sys

class NetAgent(Snake):
    def __init__(self,body=[(0,0)] , direction=(1,0), name="network", url="ws://localhost:8765"):
        self.ws = create_connection(url)
        self.ws.send(json.dumps({'cmd': 'PROXY', 'agent_name': name}))
        super().__init__(body,direction,name=name)
        self.ws.send(json.dumps({'cmd':'init', 'body':body, 'direction':direction}))
        self.name = self.ws.recv()
        if self.name == "":
            logging.error("Agent must connect before NetAgent")
        
    def ping(self):
        s = pygame.time.get_ticks()
        self.ws.send(json.dumps({'cmd':'ping'}))
        self.ws.recv()
        f = pygame.time.get_ticks()
        return f-s
    def updateBody(self,body):
        self.ws.send(json.dumps({'cmd':'updateBody', 'body':body}))
    def update(self,points=None, mapsize=None, count=None,agent_time=None):
        self.ws.send(json.dumps({'cmd':'update', 'points':points, 'mapsize':mapsize, 'count':count, 'agent_time': agent_time}))
        pass
    def updateDirection(self,maze):
        updateInfo = json.dumps({'cmd':'updateDirection', 'maze':maze.toNetwork()})
        self.ws.send(updateInfo)
        newdir = self.ws.recv()
        self.direction=json.loads(newdir)
 
