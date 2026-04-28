import customtkinter as ctk
import tkinter as tk
from maze_engine import MazeEngine

class MazeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.engine = MazeEngine()

        # Basic Configuration
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        self.title("HealthNet - Maze Generator & Solver")
        self.geometry("1100x700")

        # Configure grid layout (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Left Panel: Configuration ---
        self.left_panel = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.left_panel.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)
        self.left_panel.grid_propagate(False)

        self.setup_left_panel()

        # --- Right Panel: Canvas ---
        self.right_panel = ctk.CTkFrame(self, corner_radius=10)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=(10, 5))
        self.right_panel.grid_rowconfigure(0, weight=1)
        self.right_panel.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            self.right_panel, 
            bg="#1a1a1a", 
            highlightthickness=0,
            bd=0
        )
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.canvas.bind("<Configure>", lambda e: self.draw_maze())

        # --- Bottom Panel: Stats ---
        self.bottom_panel = ctk.CTkFrame(self, height=60, corner_radius=10)
        self.bottom_panel.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(5, 10))
        self.bottom_panel.grid_propagate(False)
        
        self.setup_bottom_panel()

    def setup_left_panel(self):
        # Title
        self.label_title = ctk.CTkLabel(self.left_panel, text="Maze Config", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_title.pack(pady=(20, 20))

        # Rows Input
        self.label_rows = ctk.CTkLabel(self.left_panel, text="Rows:")
        self.label_rows.pack(anchor="w", padx=20)
        self.entry_rows = ctk.CTkEntry(self.left_panel, placeholder_text="20")
        self.entry_rows.pack(fill="x", padx=20, pady=(0, 10))
        self.entry_rows.insert(0, "20")

        # Cols Input
        self.label_cols = ctk.CTkLabel(self.left_panel, text="Columns:")
        self.label_cols.pack(anchor="w", padx=20)
        self.entry_cols = ctk.CTkEntry(self.left_panel, placeholder_text="20")
        self.entry_cols.pack(fill="x", padx=20, pady=(0, 10))
        self.entry_cols.insert(0, "20")

        # Generator Algorithm
        self.label_gen = ctk.CTkLabel(self.left_panel, text="Generation Algorithm:")
        self.label_gen.pack(anchor="w", padx=20)
        self.option_gen = ctk.CTkOptionMenu(self.left_panel, values=["Stack-based DFS", "Prim's Algorithm"])
        self.option_gen.pack(fill="x", padx=20, pady=(0, 10))

        # Solver Algorithm
        self.label_solve = ctk.CTkLabel(self.left_panel, text="Solver Algorithm:")
        self.label_solve.pack(anchor="w", padx=20)
        self.option_solve = ctk.CTkOptionMenu(self.left_panel, values=["Backtracking", "Breadth-First Search"])
        self.option_solve.pack(fill="x", padx=20, pady=(0, 10))

        # Challenge Mode Checkbox
        self.check_challenge = ctk.CTkCheckBox(self.left_panel, text="Challenge Mode")
        self.check_challenge.pack(anchor="w", padx=20, pady=10)

        # Animation Delay Slider
        self.label_delay = ctk.CTkLabel(self.left_panel, text="Animation Delay (ms):")
        self.label_delay.pack(anchor="w", padx=20)
        self.slider_delay = ctk.CTkSlider(self.left_panel, from_=0, to=100, number_of_steps=100)
        self.slider_delay.pack(fill="x", padx=20, pady=(0, 20))
        self.slider_delay.set(10)

        # Buttons
        self.btn_next = ctk.CTkButton(self.left_panel, text="Next Step", fg_color="transparent", border_width=2)
        self.btn_next.pack(fill="x", padx=20, pady=5)

        self.btn_generate = ctk.CTkButton(self.left_panel, text="Generate Maze", command=self.on_generate_maze)
        self.btn_generate.pack(fill="x", padx=20, pady=5)

        self.btn_solve = ctk.CTkButton(self.left_panel, text="Solve Maze", fg_color="#2ecc71", hover_color="#27ae60")
        self.btn_solve.pack(fill="x", padx=20, pady=5)

    def on_generate_maze(self):
        try:
            rows = int(self.entry_rows.get())
            cols = int(self.entry_cols.get())
            self.engine.reset(rows, cols)
            self.draw_maze()
        except ValueError:
            print("Invalid input for rows/cols")

    def draw_maze(self):
        self.canvas.delete("all")
        if self.engine.rows == 0 or self.engine.cols == 0:
            return

        # Canvas dimensions
        canv_w = self.canvas.winfo_width()
        canv_h = self.canvas.winfo_height()
        
        # Calculate cell size and offsets to center the maze
        margin = 20
        cell_w = (canv_w - 2 * margin) / self.engine.cols
        cell_h = (canv_h - 2 * margin) / self.engine.rows
        cell_size = min(cell_w, cell_h)
        
        offset_x = (canv_w - (cell_size * self.engine.cols)) / 2
        offset_y = (canv_h - (cell_size * self.engine.rows)) / 2

        # Draw North Walls (horizontal)
        for r in range(self.engine.rows + 1):
            for c in range(self.engine.cols):
                if self.engine.north_wall[r][c] == 1:
                    x1 = offset_x + c * cell_size
                    y1 = offset_y + r * cell_size
                    x2 = x1 + cell_size
                    y2 = y1
                    self.canvas.create_line(x1, y1, x2, y2, fill="white", width=2)

        # Draw East Walls (vertical)
        for r in range(self.engine.rows):
            for c in range(self.engine.cols + 1):
                if self.engine.east_wall[r][c] == 1:
                    x1 = offset_x + c * cell_size
                    y1 = offset_y + r * cell_size
                    x2 = x1
                    y2 = y1 + cell_size
                    self.canvas.create_line(x1, y1, x2, y2, fill="white", width=2)

    def setup_bottom_panel(self):
        # Use a grid inside bottom panel to distribute labels
        self.bottom_panel.grid_columnconfigure((0, 1, 2), weight=1)
        self.bottom_panel.grid_rowconfigure(0, weight=1)

        self.stat_path = ctk.CTkLabel(self.bottom_panel, text="Path Length: 0", font=ctk.CTkFont(size=13))
        self.stat_path.grid(row=0, column=0)

        self.stat_visited = ctk.CTkLabel(self.bottom_panel, text="Cells Visited: 0", font=ctk.CTkFont(size=13))
        self.stat_visited.grid(row=0, column=1)

        self.stat_backtracks = ctk.CTkLabel(self.bottom_panel, text="Backtracks/Turns: 0", font=ctk.CTkFont(size=13))
        self.stat_backtracks.grid(row=0, column=2)
