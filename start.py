from game import *
from human import HumanSnake
from agent1 import Agent1
import sys, getopt

#start the game
def main(argv):
    inputfile = None 
    try:
        opts, args = getopt.getopt(argv,"hm:",["mapfile="])
    except getopt.GetoptError:
        print('start.py -m <mapfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('start.py -m <mapfile>')
            sys.exit()
        elif opt in ("-m", "--map"):
            inputfile = arg
   
    snake=SnakeGame(hor=60, ver=40, fps=20)
    snake.setObstacles(15,inputfile) #level of obstacles
    snake.setPlayers([  
        Agent1([snake.playerPos()]),
        Agent1([snake.playerPos()]),
    ])
    snake.start()



if __name__ == "__main__":
   main(sys.argv[1:])
