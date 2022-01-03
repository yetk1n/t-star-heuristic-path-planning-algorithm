import ltl_to_buchi as LTL_BA
import createMap
from astar import Astar
from djkstra_tstar import Djkstra

class TStar():
    def __init__(self, map_row, map_colum, pro_positions, obstacle, start_pos, ltl, v_init_loc):
        self.map_row = map_row
        self.map_colum = map_colum
        self.pro_positions = pro_positions
        self.obstacle = obstacle
        self.s0 = start_pos
        self.ltl = ltl
        self.T = createMap.Map(self.map_row, self.map_colum, self.pro_positions, self.obstacle).map
        self.direction = [[-1,0],[1,0],[0,1],[0,-1]]   #UP, DOWN, RIGHT, LEFT 
        self.Ur = []  #discovered array
        self.v_init_loc = v_init_loc

    def ltl_to_Buchi(self):
        ltl_to_ba = LTL_BA.LTL_To_Buchi(self.ltl)
        return ltl_to_ba.createAutomata()

    def heuristic(self, position, destination):
        return abs(position[0] - destination[0]) + abs(position[1] - destination[1])

    def Generate_Redc_Graph(self, B):  
        v_init = [self.v_init_loc, 0]

        Q = []                              #List for Qeuue
        Q_list = []                         #List for same direction states transition 
        Q_list.append(v_init)
        Q.append(Q_list)

        Gr = []                             #Reduced Graph
        layer = []                          #Represent layers of the graph

        states = []                         #Will hold P1,P2,P3. It means that state is achieved
        initial_state = False               #Will hold if the P0 should achieved or not
        fin = False
        while Q != []:
            Q_list = []                     #List for same direction states transition
            layer = []                      #Represent layers of the graph
            queuedStates = Q.pop(0)         #Popped list for same direction states transition
            loopFin = True                  #Checks if the graph is reduced or not
            for vi in queuedStates:
                #Checks if büchi automaton's states self loop is negative or not and outgoing status is positive or not
                if ((B[vi[1]].selfloop_status == "Negative") and ("Negative" not in B[vi[1]].outgoing_status)) :  
                    #Checks if any of the states has been visited
                    if states == []:
                        #If it is visited and now trying to came back to initial positon
                        if initial_state and vi[1] != 0:
                            state = "P0"
                            fin = True
                        #If it is not visited
                        else:
                            state = "P1"
                            states.append(state)
                            loopFin = False
                    #Looks for the next state
                    elif loopFin and len(states) != 3:
                        state = "P2" if len(states) == 1 else "P3"
                        states.append(state)

                    vl = self.pro_positions[state]          #Finds the next states position
                    wr = self.heuristic(vi[0], vl)          #Heuristic cosr between next state and current position

                    #If vi-vl road is not already visited
                    if (vi,vl) not in self.Ur:              
                        self.Ur.append([(vi[0],vl),False])             #Add vi-vl road as visited
                        #If this is not the first time in P0 position
                        if state != "P0":
                            vl_final = [vl, (int(state[1]) + 1 if state != "P3" else 0)]
                        #If this is the first time in P0 position
                        else:
                            vl_final = [vl, 0]
                        layer.append([vi,wr,vl_final])      #Add road and its cost to reduce graph
                        #If the next state is not on the queue ad it on queue
                        if vl_final not in Q_list:          
                            Q_list.append(vl_final)
                
                else:
                    #Checks for all possible moving directions
                    for pos in self.direction:
                        vl = (vi[0][0] + pos[0],vi[0][1] + pos[1])
                        #If next moving posiiton is not out of map or a wall
                        if vl[0] >= 0 and vl[1] >= 0 and vl[0] <= self.map_row and vl[1] <= self.map_row and self.T[vl[0]][vl[1]]  != "#":
                                wr = 1
                                #If vi-vl road is not already visited
                                if (vi,vl) not in self.Ur:
                                    self.Ur.append([(vi[0],vl),True])
                                    #If this is not the first time going from P0 position
                                    if len(states) != 0:
                                        vl_final = [vl,4]
                                    #If this is the first time going from P0 position 
                                    else:
                                        vl_final = [vl,1]
                                    layer.append([vi,wr,vl_final])  #Add road and its cost to reduce graph
                                    Q_list.append(vl_final)         #If the next state is not on the queue ad it on queue
                    
                    #If graph reduction is finished
                    if len(states) != 0:    
                        states = []
                        initial_state = True

            Gr.append(layer)
            Q.append(Q_list)
            if fin:
                break
        return Gr

    def update_edges(self, Rf, Gr, B, path): # icerde GR updatelenecek
        total_count = 0
        N = 0
        d = []
        for i in range(len(Rf)):
            for j in self.Ur:
                if (B[Rf[i][1]].selfloop_status == "Negative") and (Rf[i][0], Rf[i+1][0]) in j and j[1] == False :
                    d,count = Astar().solve(self.T, Rf[i][0], Rf[i + 1][0])
                    total_count += count
                    path.append([Rf[i][0],Rf[i+1][0],d])
                    for node in range(len(Gr)):
                        for next_node in range(len(Gr[node])):  
                            if Gr[node][next_node][0][0] == Rf[i][0] and Gr[node][next_node][2][0] == Rf[i+1][0]:
                                Gr[node][next_node][1] = len(d)
                    for node in range(len(self.Ur)):
                        if self.Ur[node][0][0] == Rf[i][0] and self.Ur[node][0][1] == Rf[i+1][0]:
                            self.Ur[node][1] = True

                    N += 1

        return N, Gr, path,total_count

    def find_path(self, Gr, v0):
        return Astar().solve(self.T, v0[0], self.v_init_loc)

    def run(self): #T, obstacle, LTL
        B = self.ltl_to_Buchi()
        Gr = self.Generate_Redc_Graph(B)
        path = []
        N = 1
        total_node_count = 0
        while N > 0:
            Rf,djk_node_count = Djkstra().run(Gr)
            N, Gr, path, astar_node_count = self.update_edges(Rf,Gr,B, path)
            total_node_count += djk_node_count
            total_node_count += astar_node_count
        Rf_suf = Rf
        v0 = (self.s0, 0)
        Rf_pre, find_path_count = self.find_path(Gr,v0)
        total_node_count += find_path_count
        for i in range(len(Rf) - 1):
            if Rf[i][0][0] - Rf[i+1][0][0] == 1 and Rf[i][0][1] - Rf[i+1][0][1] == 0:
                path.append([Rf[i][0],Rf[i+1][0],["U"]])
            if Rf[i][0][0] - Rf[i+1][0][0] == -1 and Rf[i][0][1] - Rf[i+1][0][1] == 0:
                path.append([Rf[i][0],Rf[i+1][0],["D"]])
            if Rf[i][0][0] - Rf[i+1][0][0] == 0 and Rf[i][0][1] - Rf[i+1][0][1] == 1:
                path.append([Rf[i][0],Rf[i+1][0],["L"]])
            if Rf[i][0][0] - Rf[i+1][0][0] == 0 and Rf[i][0][1] - Rf[i+1][0][1] == -1:
                path.append([Rf[i][0],Rf[i+1][0],["R"]])     
        Rp_suf = []
        for i in range(len(Rf) - 1):
            for j in path:
                if (Rf[i][0],Rf[i+1][0]) == (j[0], j[1]):
                    Rp_suf.append(j[2])
        Rp = []
        Rp = Rf_pre.copy()
        for i in Rp_suf:
            for j in i:
                Rp.append(j)

        return Rp,total_node_count