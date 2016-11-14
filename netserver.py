#!/usr/bin/env python
import asyncio
import websockets
import json

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
        print("Sent")
        while True:
            m = await agent.recv()
            print("AGENT: {}".format(m))
            await proxy.send(m)

start_server = websockets.serve(proxyserver, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
