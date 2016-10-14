from game import *
from human import HumanSnake
from agent1 import Agent1

#start the game
if __name__ == "__main__":
    snake=SnakeGame(hor=40, ver=30, fps=20)
    snake.setObstacles(15) #level of obstacles
    snake.setplayers([  
        Agent1([(40,30)]),
        Agent1(),
    ])
    snake.start()
