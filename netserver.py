#!/usr/bin/env python
import asyncio
import websockets
import json
import sys

agent = None
proxy = None

async def proxyserver(websocket, path):
    global agent, proxy

    _msg = await websocket.recv()
    msg = json.loads(_msg) 
    print("INIT: {}".format(msg))
    if msg['cmd'] == "PROXY":
        proxy = websocket
        while True:
            m = await proxy.recv()
            print("PROXY: {}".format(m))
            await agent.send(m)
        
    else:
        agent = websocket
        await proxy.send(_msg)
        while True:
            m = await agent.recv()
            print("AGENT: {}".format(m))
            await proxy.send(m)

if len(sys.argv) < 2:
    print("Usage: python3 {} port_number".format(sys.argv[0]))
    sys.exit(1)
start_server = websockets.serve(proxyserver, port=int(sys.argv[1]))

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
