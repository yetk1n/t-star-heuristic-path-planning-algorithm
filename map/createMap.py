import numpy as np


class Map():
    def __init__(self, row_size, column_size, propositions, obstacleList):
        self.row_size = row_size
        self.column_size = column_size    
        self.propositions = propositions
        self.obstacleList = obstacleList
        self.num_of_obstacles = len(obstacleList)
        self.map = []
        self.__createMap()

    #Create Map
    def __createMap(self):
        self.map = np.zeros((self.row_size, self.column_size), dtype=object)

        for i in range(self.num_of_obstacles):
            obstacle = self.obstacleList[i]
            self.map[obstacle[0]][obstacle[1]] = '#'

        for key in self.propositions:
            coordinates = self.propositions[key]
            self.map[coordinates[0]][coordinates[1]] = key

        return self.map

    def returnMap(self):
        return self.map

    def returnObstacleList(self):
        return self.obstacleList