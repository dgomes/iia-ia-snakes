#!/bin/bash

sqlite3 scores.db 'select player, sum(score) as points from points group by player order by points desc;'
