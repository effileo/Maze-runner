import customtkinter as ctk
import tkinter as tk
from maze_engine import MazeEngine

class MazeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.engine = MazeEngine()

        # Basic Configuration
        ctk.set_appearance_mode("Dark")
        
        # --- PREMIUM THEME PALETTE ---
        self.bg_color = "#050505"      # OLED Black
        self.panel_color = "#121212"   # Deep Slate
        self.accent_color = "#00f2ff"  # Holographic Cyan
        self.text_main = "#ffffff"
        self.text_dim = "#888888"
        
        self.title("MazeMaster Pro")
        self.geometry("1200x800")
        self.configure(fg_color=self.bg_color)

        # Configure main grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Top Header Bar ---
        self.header = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color=self.panel_color, border_width=1, border_color="#222222")
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.header.grid_propagate(False)
        
        self.header_label = ctk.CTkLabel(self.header, text="MAZEMASTER PRO", font=ctk.CTkFont(family="Orbitron", size=22, weight="bold"), text_color=self.accent_color)
        self.header_label.pack(side="left", padx=30)
        
        self.version_label = ctk.CTkLabel(self.header, text="v2.0 | Advanced CG Engine", font=ctk.CTkFont(size=12), text_color="#444444")
        self.version_label.pack(side="right", padx=30)

        # --- Left Panel: Configuration (Now Scrollable) ---
        self.left_panel = ctk.CTkScrollableFrame(self, width=280, corner_radius=20, fg_color=self.panel_color, border_width=1, border_color="#222222")
        self.left_panel.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        self.setup_left_panel()

        # --- Right Panel: Canvas ---
        self.right_panel = ctk.CTkFrame(self, corner_radius=25, fg_color="#080808", border_width=1, border_color="#222222")
        self.right_panel.grid(row=1, column=1, sticky="nsew", padx=(0, 20), pady=(20, 10))
        self.right_panel.grid_rowconfigure(0, weight=1)
        self.right_panel.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            self.right_panel, 
            bg="#050505", 
            highlightthickness=0,
            bd=0
        )
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.canvas.bind("<Configure>", lambda e: self.draw_maze())

        # --- Bottom Panel: Stats ---
        self.bottom_panel = ctk.CTkFrame(self, height=80, corner_radius=20, fg_color=self.panel_color, border_width=1, border_color="#222222")
        self.bottom_panel.grid(row=2, column=1, sticky="ew", padx=(0, 20), pady=(10, 20))
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
        self.slider_delay = ctk.CTkSlider(self.left_panel, from_=0, to=500, number_of_steps=100)
        self.slider_delay.pack(fill="x", padx=20, pady=(0, 20))
        self.slider_delay.set(50)

        # Buttons
        self.btn_next = ctk.CTkButton(self.left_panel, text="Step Manual", fg_color="transparent", border_width=1, border_color=self.accent_color, hover_color="#1a1a1a", text_color=self.accent_color, height=35, font=ctk.CTkFont(weight="bold"), command=self.on_next_step)
        self.btn_next.pack(fill="x", padx=30, pady=5)

        self.btn_generate = ctk.CTkButton(self.left_panel, text="Initialize Grid", fg_color="#1a1a1a", border_width=1, border_color="#333333", hover_color="#252525", height=40, font=ctk.CTkFont(weight="bold"))
        self.btn_generate.configure(command=self.on_generate_maze, text="GENERATE MAZE")
        self.btn_generate.pack(fill="x", padx=30, pady=5)

        self.btn_solve = ctk.CTkButton(self.left_panel, text="SOLVE PATH", fg_color=self.accent_color, text_color="#000000", hover_color="#00c9d4", height=45, font=ctk.CTkFont(weight="bold"), command=self.on_solve_maze)
        self.btn_solve.pack(fill="x", padx=30, pady=15)

        # Stack Log Report
        self.label_log = ctk.CTkLabel(self.left_panel, text="SYSTEM DIAGNOSTICS", font=ctk.CTkFont(size=10, weight="bold"), text_color=self.accent_color)
        self.label_log.pack(anchor="w", padx=35, pady=(20, 0))
        
        self.stack_log = ctk.CTkTextbox(self.left_panel, height=250, font=ctk.CTkFont(family="Consolas", size=10), fg_color="#050505", text_color=self.accent_color, border_width=1, border_color=self.accent_color)
        self.stack_log.pack(fill="x", padx=25, pady=(5, 30))
        self.stack_log.configure(state="disabled")

    def log_message(self, message):
        self.stack_log.configure(state="normal")
        self.stack_log.insert("end", message + "\n")
        self.stack_log.see("end")
        self.stack_log.configure(state="disabled")

    def on_generate_maze(self):
        try:
            rows = int(self.entry_rows.get())
            cols = int(self.entry_cols.get())
            is_challenge = self.check_challenge.get()
            self.engine.challenge_mode = is_challenge
            self.engine.reset(rows, cols)
            self.stack_log.configure(state="normal")
            self.stack_log.delete("1.0", "end")
            self.stack_log.configure(state="disabled")
            self.log_message("--- START GENERATION ---")
            self.animate_generation()
        except ValueError:
            print("Invalid input for rows/cols")

    def on_solve_maze(self):
        is_challenge = self.check_challenge.get()
        self.engine.init_solver(challenge_mode=is_challenge)
        self.stack_log.configure(state="normal")
        self.stack_log.delete("1.0", "end")
        self.stack_log.configure(state="disabled")
        self.log_message("--- START SOLVER ---")
        self.animate_solving()

    def on_next_step(self):
        msg = ""
        if self.engine.is_generating:
            cont, msg = self.engine.step_generation()
        elif self.engine.is_solving:
            cont, msg = self.engine.step_solve()
        
        if msg:
            self.log_message(msg)
        self.draw_maze()
        self.update_stats()

    def animate_generation(self):
        if self.engine.is_generating:
            cont, msg = self.engine.step_generation()
            if msg:
                self.log_message(msg)
            self.draw_maze()
            self.update_stats()
            
            # Delay in ms from slider
            delay = int(self.slider_delay.get())
            self.after(delay, self.animate_generation)
        else:
            self.draw_maze() # Final redraw
            self.update_stats()

    def animate_solving(self):
        if self.engine.is_solving:
            cont, msg = self.engine.step_solve()
            if msg:
                self.log_message(msg)
            self.draw_maze()
            self.update_stats()
            
            delay = int(self.slider_delay.get())
            self.after(delay, self.animate_solving)
        else:
            self.draw_maze()
            self.update_stats()

    def update_stats(self):
        self.stat_path.configure(text=f"Path Length: {self.engine.path_length}")
        self.stat_visited.configure(text=f"Cells Visited: {self.engine.cells_visited}")
        self.stat_backtracks.configure(text=f"Backtracks/Turns: {self.engine.backtracks}")

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
        # Note: PDF logic - north_wall[0] is the bottom boundary
        for r in range(self.engine.rows + 1):
            for c in range(self.engine.cols):
                if self.engine.north_wall[r][c] == 1:
                    x1 = offset_x + c * cell_size
                    # Inverted Y for PDF logic: r=0 is bottom, r=rows is top
                    y1 = offset_y + (self.engine.rows - r) * cell_size
                    x2 = x1 + cell_size
                    y2 = y1
                    # Premium Holographic Wall Logic
                    self.canvas.create_line(x1, y1, x2, y2, fill="#003344", width=3)
                    self.canvas.create_line(x1, y1, x2, y2, fill=self.accent_color, width=1)

        # Draw East Walls (vertical)
        # Note: PDF logic - east_wall[r][0] is the left boundary
        for r in range(self.engine.rows):
            for c in range(self.engine.cols + 1):
                if self.engine.east_wall[r][c] == 1:
                    x1 = offset_x + c * cell_size
                    y1 = offset_y + (self.engine.rows - (r + 1)) * cell_size
                    x2 = x1
                    y2 = y1 + cell_size
                    # Holographic Vertical Wall
                    self.canvas.create_line(x1, y1, x2, y2, fill="#003344", width=3)
                    self.canvas.create_line(x1, y1, x2, y2, fill=self.accent_color, width=1)

        # Draw Current Cell (The "Mouse")
        if self.engine.is_generating:
            r, c = self.engine.current_cell
            x1 = offset_x + c * cell_size + 4
            y1 = offset_y + (self.engine.rows - (r + 1)) * cell_size + 4
            x2 = x1 + cell_size - 8
            y2 = y1 + cell_size - 8
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="#e74c3c", outline="")

        # Draw Solver Path (Red Dots)
        if (self.engine.is_solving or self.engine.solver_visited):
            # Challenge Mode: Hide path while solving
            is_challenge = self.check_challenge.get()
            if is_challenge and self.engine.is_solving:
                pass # Don't draw path yet
            else:
                # Draw Path
                for r, c in self.engine.solver_stack + [self.engine.solver_current]:
                    if not self.engine.is_solving and r == 0 and c == 0: continue
                    cx = offset_x + c * cell_size + cell_size / 2
                    cy = offset_y + (self.engine.rows - r - 0.5) * cell_size
                    radius = cell_size / 4
                    self.canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius, fill="#e74c3c", outline="")
                
                # Draw Dead Ends (Blue Dots)
                for r, c in self.engine.dead_ends:
                    cx = offset_x + c * cell_size + cell_size / 2
                    cy = offset_y + (self.engine.rows - r - 0.5) * cell_size
                    radius = cell_size / 6
                    self.canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius, fill="#3498db", outline="")

        # Draw Start and End Markers (Green/Yellow)
        if hasattr(self.engine, 'target_cell'):
            # Start
            if self.engine.is_solving or self.engine.solver_visited:
                sr, sc = self.engine.solver_current if len(self.engine.solver_stack) == 0 else self.engine.solver_stack[0]
            else:
                sr, sc = (0, 0)
            
            sx = offset_x + sc * cell_size + cell_size / 2
            sy = offset_y + (self.engine.rows - sr - 0.5) * cell_size
            self.canvas.create_text(sx, sy, text="S", fill="#2ecc71", font=ctk.CTkFont(size=int(cell_size*0.6), weight="bold"))
            
            # End
            er, ec = self.engine.target_cell
            ex = offset_x + ec * cell_size + cell_size / 2
            ey = offset_y + (self.engine.rows - er - 0.5) * cell_size
            self.canvas.create_text(ex, ey, text="E", fill="#f1c40f", font=ctk.CTkFont(size=int(cell_size*0.6), weight="bold"))

    def setup_bottom_panel(self):
        # Configure columns for 3 metric cards
        self.bottom_panel.grid_columnconfigure((0, 1, 2), weight=1)
        
        # --- Card 1: Path Length ---
        self.f_path = ctk.CTkFrame(self.bottom_panel, fg_color="transparent")
        self.f_path.grid(row=0, column=0, pady=10)
        self.lbl_path_val = ctk.CTkLabel(self.f_path, text="0", font=ctk.CTkFont(size=24, weight="bold"), text_color=self.accent_color)
        self.lbl_path_val.pack()
        self.lbl_path_title = ctk.CTkLabel(self.f_path, text="PATH MAGNITUDE", font=ctk.CTkFont(size=10, weight="bold"), text_color=self.text_dim)
        self.lbl_path_title.pack()

        # --- Card 2: Cells Visited ---
        self.f_visit = ctk.CTkFrame(self.bottom_panel, fg_color="transparent")
        self.f_visit.grid(row=0, column=1, pady=10)
        self.lbl_visit_val = ctk.CTkLabel(self.f_visit, text="0", font=ctk.CTkFont(size=24, weight="bold"), text_color=self.accent_color)
        self.lbl_visit_val.pack()
        self.lbl_visit_title = ctk.CTkLabel(self.f_visit, text="CELLS EXPLORED", font=ctk.CTkFont(size=10, weight="bold"), text_color=self.text_dim)
        self.lbl_visit_title.pack()

        # --- Card 3: Backtracks ---
        self.f_back = ctk.CTkFrame(self.bottom_panel, fg_color="transparent")
        self.f_back.grid(row=0, column=2, pady=10)
        self.lbl_back_val = ctk.CTkLabel(self.f_back, text="0", font=ctk.CTkFont(size=28, weight="bold"), text_color="#ff4757") # Bright Coral
        self.lbl_back_val.pack()
        self.lbl_back_title = ctk.CTkLabel(self.f_back, text="BACKTRACK EVENTS", font=ctk.CTkFont(size=9, weight="bold"), text_color="#666666")
        self.lbl_back_title.pack()

    def update_stats(self):
        self.lbl_path_val.configure(text=str(self.engine.path_length))
        self.lbl_visit_val.configure(text=str(self.engine.cells_visited))
        self.lbl_back_val.configure(text=str(self.engine.backtracks))
