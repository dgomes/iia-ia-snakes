#!/usr/bin/env python3
from agent1 import Agent1
import asyncio
import websockets
import json
from maze import Maze

import logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

agent = None

async def hello():
    async with websockets.connect('ws://localhost:8765') as websocket:
        
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
                maze = Maze(None, None, None)
                maze.fromNetwork(msg['maze'])
                agent.updateDirection(maze)
                await websocket.send(json.dumps(agent.direction))

asyncio.get_event_loop().run_until_complete(hello())
