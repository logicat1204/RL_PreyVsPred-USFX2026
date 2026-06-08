import random
from collections import deque


class Environment:
    EMPTY = 0
    PREY = 1
    PREDATOR = 2
    RESOURCE = 3

    SYMBOLS = {EMPTY: '.', PREY: 'P', PREDATOR: 'D', RESOURCE: 'R'}

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[self.EMPTY] * self.cols for _ in range(self.rows)]

    def clear_all(self):
        self.grid = [[self.EMPTY] * self.cols for _ in range(self.rows)]

    def FreeSpaces(self):
        free = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == self.EMPTY:
                    free.append((i, j))
        return free

    def PosRecursos(self):
        recursos = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == self.RESOURCE:
                    recursos.append((i, j))
        return recursos

    def PosPreds(self):
        preds = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == self.PREDATOR:
                    preds.append((i, j))
        return preds

    def PosPreys(self):
        preys = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == self.PREY:
                    preys.append((i, j))
        return preys

    def set_cell(self, pos, value):
        r, c = pos
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.grid[r][c] = value

    def get_cell(self, pos):
        r, c = pos
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c]
        return -1

    def is_valid(self, pos):
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def manhattan(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def nearest_empty(self, pos, count=1, max_dist=15):
        visited = {pos}
        q = deque([(pos, 0)])
        result = []
        while q and len(result) < count:
            curr, dist = q.popleft()
            if curr != pos and self.grid[curr[0]][curr[1]] == self.EMPTY:
                result.append(curr)
                if len(result) >= count:
                    break
            if dist < max_dist:
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = curr[0] + dr, curr[1] + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        q.append(((nr, nc), dist + 1))
        return result[:count]

    def spawn_resource(self, max_resources=20):
        free = self.FreeSpaces()
        if free and len(self.PosRecursos()) < max_resources:
            self.set_cell(random.choice(free), self.RESOURCE)

    def random_free_pos(self):
        free = self.FreeSpaces()
        return random.choice(free) if free else None

    def render(self):
        for row in self.grid:
            print(' '.join(self.SYMBOLS.get(c, '?') for c in row))
        print()
