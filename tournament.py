from start import main as game_main
import os
import json
import sys
import sqlite3
import subprocess
import time
import random

def initdb():
    conn = sqlite3.connect('scores.db')
    sql = "CREATE TABLE IF NOT EXISTS points (tournament STRING, t TIMESTAMP DEFAULT CURRENT_TIMESTAMP, player STRING, score INTEGER, mapa STRING) ;"
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()

def match(tournament, p1, p2, mapa, points=1):
    print("{} VS {}".format(p1,p2))
    
    #there is no need to open a new terminal window... it just helps to analyse progress"
    launch = "open -g -b com.apple.terminal /Users/dgomes/Documents/Universidade_Aveiro/Aulas/DET/ai/Avaliacoes/tg-correccao-2017/snake/{}/run.sh"
    subprocess.Popen(launch.format(p1), shell=True)
    subprocess.Popen(launch.format(p2), shell=True)
    time.sleep(2)
    

    port = 8888
    gameops = "-s NetAgent,{},ws://localhost:{} -o NetAgent,{},ws://localhost:{} --timeout 1000 --disable-video -m {}".format(p1,port,p2,port,mapa).split(" ")
    game_main(gameops)
   
    # well.. you don't need this if you don't open the previous windows 
    clean = """osascript -e "tell application \\\"Terminal\\\" to close (every window whose name contains \\\"AGENT{}\\\")" """
    subprocess.Popen(clean.format(p1),shell=True)
    subprocess.Popen(clean.format(p2),shell=True)
    time.sleep(3)
    
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute("select * from scores order by t desc limit 1;")
    uuid,t,pl1,pl1_score,pl2,pl2_score = c.fetchone()
    if int(pl1_score) >= int(pl2_score): #vantagem para a casa (tem q haver um criterio de desempate!)
        w = pl1
    else:
        w = pl2
    c.execute('INSERT INTO points (tournament, player, score, mapa) VALUES (?,?,?,?)', (tournament, w, points, mapa))
    conn.commit()
    conn.close()
    return w

if __name__ == "__main__":
    initdb()
    s = dict()
    tournament = sys.argv[1]
    mapa = sys.argv[2] 
    snakes = sys.argv[3:]
    random.shuffle(snakes)
    s['round_n'] = 0
    s['round_points'] = 1
   
    if os.path.isfile('state.json'): 
        with open('state.json') as fi:
            s = json.load(fi)
            snakes = s['snakes']
            s['round_n']-=1

    while len(snakes) > 1:
        if len(snakes)%2 == 1:
            snakes.append(random.choice(snakes[:-1])) #give someone a chance / only valid for 1st round
        s['round_n']+=1
        
        if 'winners' in s:
            winners = s['winners']
            losers = s['losers']
        else:
            winners = []
            losers = [] 
    

        if len(snakes+winners) == 2:
            print("FINAL: {}".format(snakes))
        elif len(winners) == 4:
            print("MEIA FINAL: {}".format(snakes))
        else:
            print("ROUND {}: {}".format(s['round_n'], snakes))

        p1 = None
        p2 = None
        for i,p in enumerate(snakes):
            if p1 == None:
                p1 = p
            elif p2 == None:
                p2 = p
            
            if p1 != None and p2 != None:
                if p1 != p2:
                    w = str(match(tournament,p1,p2,mapa,s['round_points']))
                else:
                    w = p1
                
                winners.append(w)
                if w in p1:
                    losers.append(p2)
                elif w in p2:
                    losers.append(p1)
                    
                print("Winner: {}".format(w))
                p1 = None
                p2 = None
                s['winners'] = winners
                s['losers'] = losers
                s['snakes'] = snakes[(i+1):] 
                with open('state.json','w') as fo:
                    json.dump(s, fo)
 
        if len(winners) >1 and len(winners)%2 == 1:
            winners.append(random.choice(s['losers'])) #repescagem 
        print("Winners: {}".format(winners))
        snakes = winners
        s['round_points'] = 2*s['round_points']
        s['winners'] = []
        s['losers'] = []
    print("Champion: {}".format(snakes[0]))
    os.remove('state.json')
