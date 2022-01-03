class Node():
    def __init__(self, parent_node, start_position, g, h_value, f_value): 
        self.parent_node = parent_node
        self.start_position = start_position
        self.g = g
        self.h = h_value
        self.f = f_value

class Astar():
    def __init__(self):
        self.g_values = []
        self.INFINITY_COST = 2**10
        self.direction = [[-1,0],[1,0],[0,1],[0,-1]]    #UP, DOWN, RIGHT, LEFT 
    
    # def __find_destination_position(self, level_matrix, dest_position):
    #     for r in range(len(level_matrix)):
    #         for c in range(len(level_matrix[0])):
    #             if (level_matrix[r][c] == dest_position):
    #                 return (r, c)
    #     return (-1, -1)

    def __heuristic(self, start_row, start_column, destination_row, destination_column):
        return abs(start_row - destination_row) + abs(start_column - destination_column)
    
    def __get_fh_Value(self,Node):
        return Node.f, Node.h

    def __get_road(self,Node, start_pos):
        pos = Node.start_position
        g = self.g_values[pos[0]][pos[1]]
        road = []
        
        while pos != start_pos:
            for i in self.direction:
                if (pos[0] + i[0]) >= len(self.g_values) or (pos[1] + i[1]) >= len(self.g_values):
                    continue
                if g > self.g_values[pos[0] + i[0]][pos[1] + i[1]]:
                    if i == [0,-1]:
                        road.insert(0,"R")
                    elif i == [0,1]:
                        road.insert(0,"L")
                    elif i == [-1,0]:
                        road.insert(0,"D")
                    elif i==[1,0]:
                        road.insert(0,"U")
                    g = self.g_values[pos[0] + i[0]][pos[1] + i[1]]
                    pos = (pos[0] + i[0],pos[1] + i[1])
                    break
        return road

    def solve(self, map_matrix, start_position, dest_position):
        move_sequence = []

        initial_level_matrix = [list(row) for row in map_matrix] #deepcopy(level_matrix)
        
        level_height = len(initial_level_matrix)
        level_width = len(initial_level_matrix[0])
          
        #  initialize g values
        self.g_values = [ [self.INFINITY_COST]*level_width for i in range(level_height) ]
        
        #  initialize g of starting position 0
        self.g_values[start_position[0]][start_position[1]] = 0
        
        #  calculate heuristic value for starting position
        # (destination_row, destination_column) = self.__find_destination_position(initial_level_matrix, dest_position)
        (destination_row, destination_column) = dest_position

        initial_heuristic = self.__heuristic(start_position[0], start_position[1], destination_row, destination_column)

        ###--- Initializing necessary lists and booleans ---###
        queue = []   
        visited = []
        nodes_in_queue = []
        finished = False
        counter = 0
        ###--- Creating first node ---###
        first_node = Node(None, start_position, self.g_values[start_position[0]][start_position[1]], initial_heuristic, initial_heuristic)
        queue.append(first_node)

        while queue and not finished:
            
            ###--- Tie Breaking Options ---###
            queue.sort(key = self.__get_fh_Value)       #Tie breaking by smallest h values if there is a tie break in f values
            ###################################
            # last_node = 0
            ###--- Choosing next node ---###
            head_node = queue.pop(0)
            current_pos = head_node.start_position

            ###--- Exploring Up,Down,Right and Left nodes ---###
            for i in self.direction:
                
                next_pos = (current_pos[0] + i[0],current_pos[1] + i[1])

                if next_pos[0] < 0 or next_pos[1] < 0 or next_pos[0] >= len(map_matrix) or next_pos[1] >= len(map_matrix):
                    continue
                ###--- Looking for walls if there is any ---###
                if map_matrix[next_pos[0]][next_pos[1]] != "#":
                    counter += 1
                    ###--- Answer to: Will next move find the apple? ---### 
                    if (next_pos[0] == destination_row) and (next_pos[1] == destination_column):
                        ###--- Calculating g,h and f values ---###
                        g_new = self.g_values[current_pos[0]][current_pos[1]] + 1
                        ###--- Update g_value if there is a shorter way ---###
                        if self.g_values[next_pos[0]][next_pos[1]] > g_new:
                            self.g_values[next_pos[0]][next_pos[1]] = g_new
                        h_new = self.__heuristic(next_pos[0], next_pos[1], destination_row, destination_column)
                        f_new = g_new + h_new
                        
                        ###--- Creating last node (Apple is on this node) ---###
                        last_node = Node(head_node, next_pos, g_new, h_new, f_new)
                        finished = True
                    ###--- If next node not visited ---###
                    elif next_pos not in visited:
                        ###--- Calculating g,h and f values ---###
                        g_new = self.g_values[current_pos[0]][current_pos[1]] + 1
                        ###--- Update g_value if there is a shorter way ---###
                        if self.g_values[next_pos[0]][next_pos[1]] > g_new:
                            self.g_values[next_pos[0]][next_pos[1]] = g_new
                        h_new = self.__heuristic(next_pos[0], next_pos[1], destination_row, destination_column)
                        f_new = g_new + h_new
                        ###--- If node is not already in queue ---###
                        if next_pos not in nodes_in_queue:
                            new_node = Node(head_node, next_pos, g_new, h_new, f_new)
                            queue.append(new_node)
                            nodes_in_queue.append(next_pos)
            ###--- Append node as visiited ---###
            visited.append(current_pos)
                        
        ###--- Generating moving sequence ---###
        move_sequence = self.__get_road(last_node, start_position)

        return move_sequence,counter