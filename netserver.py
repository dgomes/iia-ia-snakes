#!/usr/bin/env python
import asyncio
import websockets
import json
import sys
import logging

logging.basicConfig(format=':%(levelname)s:%(message)s', level=logging.INFO)
proxy = None
agent = None

async def agentserver(websocket, path):
    global proxy, agent

    try:
        _msg = await websocket.recv()
        msg = json.loads(_msg) 
        logging.info("INIT: {}".format(msg))
        if msg['cmd'] == "HELLO":
            agent = websocket
            while True:
                m = await agent.recv()
                logging.debug("AGENT: {}".format(m))
                await proxy.send(m)
            
        else:
            proxy = websocket
            if agent == None:
                logging.error("Agent must connect before Proxy") 
                proxy.close()
                return
            await agent.send(_msg) #proxy 1st message is the __init__ that must be sent to the agent
            while True:
                m = await proxy.recv()
                logging.debug("PROXY: {}".format(m))
                await agent.send(m)

    except websockets.exceptions.ConnectionClosed as e:
        if proxy != None:
            proxy.close(1001,"Other end closed")
            proxy = None
        if agent != None:
            agent.close(1001,"Other end closed")
            agent = None

if len(sys.argv) < 2:
    print("Usage: python3 {} port_number".format(sys.argv[0]))
    sys.exit(1)
start_server = websockets.serve(agentserver, port=int(sys.argv[1]))

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
