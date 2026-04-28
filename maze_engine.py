import random

class MazeEngine:
    def __init__(self):
        self.rows = 0
        self.cols = 0
        self.north_wall = []
        self.east_wall = []
        
        # Generation State
        self.stack = []
        self.visited = []
        self.current_cell = (0, 0)
        self.is_generating = False

        # Stats
        self.path_length = 0
        self.cells_visited = 0
        self.backtracks = 0

    def reset(self, rows, cols):
        self.rows = rows
        self.cols = cols
        
        # Walls
        self.north_wall = [[1 for _ in range(cols)] for _ in range(rows + 1)]
        self.east_wall = [[1 for _ in range(cols + 1)] for _ in range(rows)]
        
        # State
        self.visited = [[False for _ in range(cols)] for _ in range(rows)]
        self.stack = []
        self.current_cell = (0, 0)
        self.is_generating = True
        self.cells_visited = 0
        
    def step_generation(self):
        """Performs one step of the DFS generation algorithm."""
        if not self.is_generating:
            return False

        r, c = self.current_cell
        if not self.visited[r][c]:
            self.visited[r][c] = True
            self.cells_visited += 1

        # Find neighbors
        neighbors = []
        # Up
        if r > 0 and not self.visited[r-1][c]:
            neighbors.append(('N', r-1, c))
        # Down
        if r < self.rows - 1 and not self.visited[r+1][c]:
            neighbors.append(('S', r+1, c))
        # Left
        if c > 0 and not self.visited[r][c-1]:
            neighbors.append(('W', r, c-1))
        # Right
        if c < self.cols - 1 and not self.visited[r][c+1]:
            neighbors.append(('E', r, c+1))

        if neighbors:
            # Pick a random neighbor
            direction, nr, nc = random.choice(neighbors)
            
            # Remove wall
            if direction == 'N':
                self.north_wall[r][c] = 0
            elif direction == 'S':
                self.north_wall[r+1][c] = 0
            elif direction == 'W':
                self.east_wall[r][c] = 0
            elif direction == 'E':
                self.east_wall[r][c+1] = 0
            
            self.stack.append((r, c))
            self.current_cell = (nr, nc)
        elif self.stack:
            self.current_cell = self.stack.pop()
        else:
            self.is_generating = False
            return False # Finished
            
        return True # More steps to go
