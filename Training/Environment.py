#El entorno sera una matriz de tiles
class Environment:
    def __init__(self, prey, pred, map):
        self.prey = prey
        self.pred = pred
        self.grid = map

    def __str__(self):
        return "Prey: " + str(self.prey) + "\nPred: " + str(self.pred) + "\nGrid: " + str(self.grid)
    
    def FreeSpaces(self):
        free_spaces = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 0: # Assuming 0 represents a free space
                    free_spaces.append((i, j))
        return free_spaces
    
    def PosRecursos(self):
        recursos = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 3: # Assuming 3 represents a resource
                    recursos.append((i, j))
        return recursos

    def PosPreds(self):
        preds = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 2: # Assuming 2 represents a predator
                    preds.append((i, j))
        return preds
    
    def PosPreys(self):
        preys = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 1: # Assuming 1 represents a prey
                    preys.append((i, j))
        return preys
    
