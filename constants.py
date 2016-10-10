import pygame,random
from pygame.locals import *
from sys import exit
import math

fps=50 #frames per second. The higher, the harder
#direction of snake
left=-1,0
right=1,0
up=0,-1
down=0,1
directions=[up,down,right,left]

