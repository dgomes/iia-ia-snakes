from game import *
from human import HumanSnake
from agent1 import Agent1

#start the game
if __name__ == "__main__":
    snake=SnakeGame(hor=60, ver=40, fps=20)
    snake.SetObstacles(15) #level of obstacles
    snake.setplayers([  
        Agent1([(60,40)]),
        Agent1(),
    ])
    snake.start()
