from game import *
from human import HumanSnake
from agent1 import ComputerSnake

#start the game
if __name__ == "__main__":
    snake=SnakeGame(hor=30, ver=20, fps=20)
    snake.SetObstacles(15) #level of obstacles
    snake.setplayers([  
        HumanSnake([(12,14)]),
        ComputerSnake(),
    ])
    snake.start()
