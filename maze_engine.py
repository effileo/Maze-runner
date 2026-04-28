import random

class MazeEngine:
    def __init__(self):
        self.rows = 0
        self.cols = 0
        
        # --- DATA STRUCTURE REQUIREMENTS (From Assignment PDF) ---
        # north_wall[R][C]: If 1, the cell has a solid upper wall.
        # The zeroth row is a phantom row of cells below the maze 
        # whose north walls make up the bottom edge of the maze.
        self.north_wall = [] 
        
        # east_wall[R][C]: Specifies where gaps appear in vertical walls.
        # east_wall[i][0] specifies gaps in the left edge of the maze.
        self.east_wall = []
        
        # Generation State
        self.stack = []
        self.visited = []
        self.current_cell = (0, 0)
        self.is_generating = False
        self.is_solving = False
        self.challenge_mode = False

        # Solver State
        self.solver_stack = []
        self.solver_visited = []
        self.dead_ends = []
        self.solver_current = (0, 0)

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
        self.is_solving = False
        self.cells_visited = 0
        self.path_length = 0
        self.backtracks = 0
        self.dead_ends = []

    def init_solver(self, challenge_mode=False):
        self.challenge_mode = challenge_mode
        self.solver_visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.solver_stack = []
        
        if self.challenge_mode:
            # Bonus: Interior start and end
            self.solver_current = (random.randint(0, self.rows-1), random.randint(0, self.cols-1))
            self.target_cell = (random.randint(0, self.rows-1), random.randint(0, self.cols-1))
            while self.target_cell == self.solver_current:
                self.target_cell = (random.randint(0, self.rows-1), random.randint(0, self.cols-1))
        else:
            self.solver_current = (0, 0)
            self.target_cell = (self.rows - 1, self.cols - 1)

        self.dead_ends = []
        self.is_solving = True
        self.path_length = 0
        self.backtracks = 0
        self.cells_visited = 0 

    def step_solve(self):
        """Performs one step of the backtracking solver."""
        if not self.is_solving:
            return False, ""

        r, c = self.solver_current
        log_msg = ""
        
        if not self.solver_visited[r][c]:
            self.solver_visited[r][c] = True
            self.cells_visited += 1

        # Check if reached the end
        if r == self.target_cell[0] and c == self.target_cell[1]:
            self.is_solving = False
            self.path_length = len(self.solver_stack) + 1
            return False, "--- REACHED EXIT! ---"

        # Find valid neighbors (no wall and not visited)
        neighbors = []
        # Up
        if r > 0 and self.north_wall[r][c] == 0 and not self.solver_visited[r-1][c]:
            neighbors.append((r-1, c))
        # Down
        if r < self.rows - 1 and self.north_wall[r+1][c] == 0 and not self.solver_visited[r+1][c]:
            neighbors.append((r+1, c))
        # Left
        if c > 0 and self.east_wall[r][c] == 0 and not self.solver_visited[r][c-1]:
            neighbors.append((r, c-1))
        # Right
        if c < self.cols - 1 and self.east_wall[r][c+1] == 0 and not self.solver_visited[r][c+1]:
            neighbors.append((r, c+1))

        if neighbors:
            # Move to the first available neighbor
            nr, nc = neighbors[0]
            self.solver_stack.append((r, c))
            log_msg = f"PUSH ({r}, {c})"
            self.solver_current = (nr, nc)
            self.path_length = len(self.solver_stack) + 1
        else:
            # Dead end: Backtrack
            self.dead_ends.append((r, c))
            log_msg = f"DEAD END ({r}, {c})"
            if self.solver_stack:
                self.solver_current = self.solver_stack.pop()
                r2, c2 = self.solver_current
                log_msg += f" -> POP ({r2}, {c2})"
                self.backtracks += 1
                self.path_length = len(self.solver_stack) + 1
            else:
                self.is_solving = False # No path found
                return False, "--- NO PATH FOUND ---"

        return True, log_msg
        
    def step_generation(self):
        """Performs one step of the DFS generation algorithm."""
        if not self.is_generating:
            return False, ""

        r, c = self.current_cell
        log_msg = ""
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

        # Bonus: 1 in 20 chance to eat an extra wall to a VISITED neighbor (creating a cycle)
        if self.challenge_mode and random.random() < 0.05:
            all_n = []
            if r > 0: all_n.append(('N', r-1, c))
            if r < self.rows - 1: all_n.append(('S', r+1, c))
            if c > 0: all_n.append(('W', r, c-1))
            if c < self.cols - 1: all_n.append(('E', r, c+1))
            v_n = [n for n in all_n if self.visited[n[1]][n[2]]]
            if v_n:
                d, nr_b, nc_b = random.choice(v_n)
                if d == 'N': self.north_wall[r][c] = 0
                elif d == 'S': self.north_wall[r+1][c] = 0
                elif d == 'W': self.east_wall[r][c] = 0
                elif d == 'E': self.east_wall[r][c+1] = 0

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
            log_msg = f"PUSH ({r}, {c})"
            self.current_cell = (nr, nc)
        elif self.stack:
            self.current_cell = self.stack.pop()
            r, c = self.current_cell
            log_msg = f"POP ({r}, {c})"
        else:
            self.is_generating = False
            return False, "--- FINISHED ---"
            
        return True, log_msg # More steps to go
