from game import *
from human import HumanSnake
from agent1 import Agent1
from netagent import NetworkAgent
from maze import Maze

import asyncio
import websockets
import json
import logging
import sys, getopt

#start the game
def main(argv):
    inputfile = None
    visual = True
    network = False
    url = 'ws://localhost:8765' 
    try:
        opts, args = getopt.getopt(argv,"hm:u:",["map=","disable-video","url="])
    except getopt.GetoptError:
        print('start.py [-m/--map <mapfile> --disable-video -u/--url websocket_url]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('start.py -m <mapfile>')
            sys.exit()
        elif opt in ("-m", "--map"):
            inputfile = arg
        elif opt in ("--disable-video"):
            visual = False 
        elif opt in ("-u", "--url"):
            network = True
            url = arg            

    if network:
        asyncio.get_event_loop().run_until_complete(proxy(url))
    else:
        snake=SnakeGame(hor=60, ver=40, fps=20, visual=visual)
        snake.setObstacles(15,inputfile) #level of obstacles
        snake.setPlayers([  
            Agent1([snake.playerPos()]),
    #        Agent1([snake.playerPos()]),
            NetworkAgent([snake.playerPos()]),
        ])
        snake.start()

async def proxy(url):
    async with websockets.connect(url) as websocket:
        logger = logging.getLogger('websockets')
        logger.setLevel(logging.ERROR)
        logger.addHandler(logging.StreamHandler())

        #connect to proxy, get init values and announce ourselves through the agent name
        await websocket.send(json.dumps({'cmd': 'PROXY'}))
        init = json.loads(await websocket.recv())
        agent = Agent1([(b[0], b[1]) for b in init['body']],(init['direction'][0], init['direction'][1]), name = "Network")
        await websocket.send(agent.name)

        while True:
            m = await websocket.recv()
            msg = json.loads(m)
            if msg['cmd'] == 'updateBody':
                agent.updateBody([(b[0], b[1]) for b in msg['body']])
            if msg['cmd'] == 'update':
                logging.info(msg['points'])
                agent.update(points=[(p[0], p[1]) for p in msg['points']], mapsize=(msg['mapsize'],msg['mapsize']), count=msg['count'], agent_time=msg['agent_time'])
            elif msg['cmd'] == 'updateDirection':
                maze = Maze(None, None, None) #create void maze before loading the real one
                maze.fromNetwork(msg['maze'])
                agent.updateDirection(maze)
                await websocket.send(json.dumps(agent.direction))

if __name__ == "__main__":
   main(sys.argv[1:])

