import createMap
import numpy as np
from djkstra import *
import time
from tStar import *
import pandas as pd


PRO_POSITIONS =  {}
OBSTACLES = []
LTL = open(r"ltl.txt").readlines()

states_loc = [None,None,None,None,None,None]
states = ["P0","P1","P2","P3","P0"]

data = pd.read_csv("map.csv", header=None)
data = np.array(data)

ROW = data.shape[0]
COLUMN = data.shape[1] 
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        if data[i][j] == "#":
            OBSTACLES.append((i,j)) 
        if data[i][j] == "Start":
            START_POS = (i,j)
            states_loc[0] = (i,j)
        if data[i][j] == "P0":
            PRO_POSITIONS[data[i][j]] = (i,j)
            states_loc[1] = (i,j)
            states_loc[5] = (i,j)
        if data[i][j] == "P1":
            PRO_POSITIONS[data[i][j]] = (i,j)
            states_loc[2] = (i,j)
        if data[i][j] == "P2":
            PRO_POSITIONS[data[i][j]] = (i,j)
            states_loc[3] = (i,j)
        if data[i][j] == "P3":
            PRO_POSITIONS[data[i][j]] = (i,j)
            states_loc[4] = (i,j)


###----Comparing Results----####
start_time = time.time()
Tstar = TStar(ROW, COLUMN, PRO_POSITIONS, OBSTACLES , START_POS, LTL, PRO_POSITIONS["P0"])
road, count = Tstar.run()
print("T*:      --- {:0.4f} seconds ---".format(time.time() - start_time))

start_time = time.time()
counter1 = 0
grid = createMap.Map(ROW, COLUMN, PRO_POSITIONS, OBSTACLES).map
for i in range(len(states_loc)):
    if i+1 < len(states_loc):
        road,x = Astar().solve(grid,states_loc[i],states_loc[i+1])
        counter1 += x
print("A*:      --- {:0.4f} seconds ---".format(time.time() - start_time))

start_time = time.time()
counter2 = 0
grid = createMap.Map(ROW, COLUMN, PRO_POSITIONS, OBSTACLES).map
for i in range(len(states_loc)):
    if i+1 < len(states_loc):
        road2, x = DjkstraOld().solve(grid,states_loc[i],states[i],OBSTACLES)
        counter2 += x
print("Djkstra: --- {:0.4f} seconds ---".format(time.time() - start_time))


