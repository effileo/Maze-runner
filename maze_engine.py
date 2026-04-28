class MazeEngine:
    def __init__(self):
        self.rows = 0
        self.cols = 0
        self.north_wall = []
        self.east_wall = []
        
        # Stats
        self.path_length = 0
        self.cells_visited = 0
        self.backtracks = 0

    def reset(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # Implement 2D list initialization in Phase 2
        pass
