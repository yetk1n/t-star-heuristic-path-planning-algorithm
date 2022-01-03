from itertools import product


class DjkstraOld():
    def __init__(self):
        self.INFINITY_COST = 2**10

    def __find_destination_position(self, level_matrix, state):
        for r in range(len(level_matrix)):
            for c in range(len(level_matrix[0])):
                if (level_matrix[r][c] == state):
                    return (r, c)
        return (-1, -1)

    def __get_nodes(self,row_len,colum_len,obstacleList): #Create mape çekilicek
        return [(i, j) for i, j in product(range(row_len), range(colum_len)) if (i, j) not in obstacleList]
    
    def __get_adjacent(self,map_matrix, node):
        i = node[0]
        j = node[1]

        if i < 0 or i >= len(map_matrix) or j < 0 or j >= len(map_matrix[0]):
            raise Exception("Out of bounds")

        if map_matrix[i][j] == "#":
            return []

        adjacent = []

        for del_pos in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if 0 <= i + del_pos[0] < len(map_matrix[0]) and 0 <= j + del_pos[1] < len(map_matrix[0]):
                if map_matrix[i + del_pos[0]][j + del_pos[1]] != "#":
                    adjacent.append((i + del_pos[0], j + del_pos[1]))

        return adjacent

    def solve(self,map_matrix, start_pos, state, obstacleList):
        Q = self.__get_nodes(len(map_matrix), len(map_matrix[0]),obstacleList)
        dist = {node : self.INFINITY_COST for node in Q}
        prev = {node : None for node in Q}
        dest = self.__find_destination_position(map_matrix,state)


        dist[start_pos] = 0
        count = 0
        while Q:
            u = min(Q, key = dist.__getitem__)
            Q.remove(u)
            
            for v in self.__get_adjacent(map_matrix,u):
                count += 1
                alt = dist[u] + 1
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u

        path = [dest]
        cur = dest

        while prev[cur]:
            # count += 1
            path.append(prev[cur])
            cur = prev[cur]

        return list(reversed(path)), count

