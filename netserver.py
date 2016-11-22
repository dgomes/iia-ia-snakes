#!/usr/bin/env python
import asyncio
import websockets
import json
import sys
import logging
import sqlite3

logging.basicConfig(format=':%(levelname)s:%(message)s', level=logging.INFO)
proxy = dict() 
agent = dict()
conn = sqlite3.connect('scores.db')
sql = "CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY AUTOINCREMENT, t TIMESTAMP DEFAULT CURRENT_TIMESTAMP, player1 STRING, player1_score INTEGER, player2 STRING, player2_score INTEGER) ;"
c = conn.cursor()
c.execute(sql)
conn.commit()

async def agentserver(websocket, path):
    global proxy, agent,conn
    score = None
    try:
        _msg = await websocket.recv()
        msg = json.loads(_msg)
        name = msg['agent_name'] 
        logging.info("INIT: {}".format(msg))
        if msg['cmd'] == "AGENT":
            agent[name] = websocket
            while True:
                m = await agent[name].recv()
                logging.debug("AGENT: {}".format(m))
                await proxy[name].send(m)
        elif msg['cmd'] == 'PROXY':
            proxy[name] = websocket
            if agent[name] == None:
                logging.error("Agent must connect before Proxy")
                proxy[name].send("CLOSE")
                proxy[name].close()
                return
            while True:
                m = await proxy[name].recv()
                logging.debug("PROXY: {}".format(m))

                msg = json.loads(m)
                if msg['cmd'] == 'update':
                    score = msg['points']

                await agent[name].send(m)
    except websockets.exceptions.ConnectionClosed as e:
        if name in proxy.keys() and proxy[name] != None:
            proxy[name].close(1001,"Other end closed")
            proxy[name] = None
        if name in agent.keys() and agent[name] != None:
            agent[name].close(1001,"Other end closed")
            agent[name] = None
        if score != None:
            logging.info(score)
            c = conn.cursor()
            c.execute('INSERT INTO scores (player1, player1_score, player2, player2_score) VALUES (?,?,?,?)', (score[0][0], score[0][1], score[1][0], score[1][1] ))
            conn.commit()

if len(sys.argv) < 2:
    print("Usage: python3 {} port_number".format(sys.argv[0]))
    sys.exit(1)
start_server = websockets.serve(agentserver, port=int(sys.argv[1]))

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
