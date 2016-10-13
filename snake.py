from constants import *
import logging

class Snake:
    def __init__(self,body , direction, name):
        self.body=body #initially located here
        self.name=name
        self.direction=self.newdirection=direction
        self.IsDead=False
        logging.basicConfig(format=':%(levelname)s:%(message)s', level=logging.DEBUG)
    def UpdateDirection(self,game):
        self.direction=self.newdirection #the next direction is stored in newdirection....logic is updated here
    def processkey(self,key):
        pass #nothing to do here it is just to support human players

