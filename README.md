# Snakes Clone

![Demo](https://github.com/dgomes/iia-ia-snakes/raw/master/Screenshot%202019-11-14%20at%2015.46.26.png)

# Requirements:
- Python 3.5 (carefull! 3.4 will not work!)
- Create a virtualenv:
    virtualenv -p /usr/bin/python3.5 venv
    source venv/bin/activate
- Install requirements.txt
    pip install -r requirements.txt

# Agent Class naming:

The Student agent class must live in a file with the same name as the class, example:

StudentAgent -> studentagent.py

# Network Game:

A remote player (will not get video output) will play against a local player

step 1: (server) - python3 netserver.py 8765
step 2: (REMOTE player being proxied) - python3 start.py -p -s Agent1,remoto,ws://server:8765
step 3: (LOCAL player hosting the game) - python3 start.py -s Agent1,local -o NetAgent,remoto,ws://server:8765 

Don't forget about firewalls and ports!

There is a public server:  ws://barbrady.av.it.pt/snakes

# Practice against other agents

A game server has been setup where agent can meet dinamicaly and play against each other (no visual interface)

just run the script: 

treino.sh AgentClassName AgentName

# How to configure a remote repository (get updates from the teachers repository)

Since you probably cloned the professors repository and created your own repository, you need to configure a a remote repository:

    git remote add upstream https://code.ua.pt/git/iia-ia-snakes

Now you can fetch from the upstream and merge with your repository:

    git fetch upstream
    git checkout master (or other branch)
    git merge upstream/master (or other branch)


