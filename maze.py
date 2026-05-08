import pygame
import sys
import random
import math
from collections import deque

# --- Constants & Configuration ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 850  # Increased height for better spacing
LEFT_PANEL_WIDTH = 350
BOTTOM_PANEL_HEIGHT = 100
MAZE_AREA_WIDTH = SCREEN_WIDTH - LEFT_PANEL_WIDTH
MAZE_AREA_HEIGHT = SCREEN_HEIGHT - BOTTOM_PANEL_HEIGHT

# Colors (Premium Dark Theme / GitHub Dark Style)
BG_COLOR = (13, 17, 23)           # Deep black-blue
PANEL_COLOR = (22, 27, 34)        # Secondary panel
PANEL_BORDER = (48, 54, 61)       # Subtle borders
ACCENT_BLUE = (88, 166, 255)      # Soft primary blue
ACCENT_GREEN = (46, 160, 67)      # Success green
ACCENT_RED = (248, 81, 73)        # Error red
TEXT_PRIMARY = (230, 237, 243)    # Bright text
TEXT_SECONDARY = (139, 148, 158)  # Muted text
GRID_COLOR = (33, 38, 45)         # Grid background
WALL_COLOR = (139, 148, 158)      # Wall color
PATH_COLOR = (248, 81, 73)        # Red for current path dots
MOUSE_COLOR = (248, 81, 73)       # Red mouse dot
VISITED_COLOR = (33, 38, 45)      # Visited cells background
DEAD_END_COLOR = (56, 139, 253)   # Blue for explored/dead end dots

# Fonts
pygame.font.init()
def get_font(size, bold=False):
    name = "Segoe UI" if sys.platform == "win32" else "Arial"
    return pygame.font.SysFont(name, size, bold)

FONT_SM = get_font(14)
FONT_MD = get_font(16)
FONT_LG = get_font(20, True)
FONT_TITLE = get_font(36, True)
FONT_SUB = get_font(18)

# --- UI Component System ---

class UIComponent:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.is_hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        return False

    def draw(self, surface):
        pass

class Button(UIComponent):
    def __init__(self, x, y, w, h, text, color=ACCENT_BLUE, callback=None, enabled=True):
        super().__init__(x, y, w, h)
        self.text = text
        self.color = color
        self.callback = callback
        self.enabled = enabled

    def handle_event(self, event):
        super().handle_event(event)
        if self.enabled and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.callback:
                self.callback()
                return True
        return False

    def draw(self, surface):
        draw_color = self.color if self.enabled else (48, 54, 61)
        if self.enabled and self.is_hovered:
            # Subtle glow effect
            glow_rect = self.rect.inflate(4, 4)
            pygame.draw.rect(surface, (*self.color, 40), glow_rect, border_radius=10)
            draw_color = tuple(min(255, c + 30) for c in draw_color)
        
        # Shadow/Deep border
        pygame.draw.rect(surface, (13, 17, 23), self.rect.move(0, 2), border_radius=6)
        pygame.draw.rect(surface, (60, 66, 74), self.rect, border_radius=6)
        pygame.draw.rect(surface, draw_color, self.rect.inflate(-2, -2), border_radius=5)
        
        txt_color = TEXT_PRIMARY if self.enabled else TEXT_SECONDARY
        txt_surf = FONT_MD.render(self.text, True, txt_color)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)

class Slider(UIComponent):
    def __init__(self, x, y, w, min_val, max_val, current_val, label):
        super().__init__(x, y, w, 20)
        self.min_val = min_val
        self.max_val = max_val
        self.current_val = current_val
        self.label = label
        self.dragging = False
        self.thumb_rect = pygame.Rect(0, 0, 14, 14)
        self.update_thumb_pos()

    def update_thumb_pos(self):
        ratio = (self.current_val - self.min_val) / (self.max_val - self.min_val)
        self.thumb_rect.center = (self.rect.x + int(ratio * self.rect.w), self.rect.centery)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.thumb_rect.inflate(10, 10).collidepoint(event.pos) or self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            rel_x = max(0, min(event.pos[0] - self.rect.x, self.rect.w))
            ratio = rel_x / self.rect.w
            self.current_val = self.min_val + ratio * (self.max_val - self.min_val)
            self.update_thumb_pos()
            return True
        return False

    def draw(self, surface):
        lbl_surf = FONT_SM.render(f"{self.label}: {int(self.current_val)}ms", True, TEXT_SECONDARY)
        surface.blit(lbl_surf, (self.rect.x, self.rect.y - 20))
        
        # Track
        pygame.draw.rect(surface, (48, 54, 61), (self.rect.x, self.rect.centery - 2, self.rect.w, 4), border_radius=2)
        # Active track
        ratio = (self.current_val - self.min_val) / (self.max_val - self.min_val)
        pygame.draw.rect(surface, ACCENT_BLUE, (self.rect.x, self.rect.centery - 2, int(self.rect.w * ratio), 4), border_radius=2)
        # Thumb
        pygame.draw.circle(surface, (230, 237, 243), self.thumb_rect.center, 7)
        pygame.draw.circle(surface, ACCENT_BLUE, self.thumb_rect.center, 5)

class Checkbox(UIComponent):
    def __init__(self, x, y, label, checked=False, callback=None):
        super().__init__(x, y, 18, 18)
        self.label = label
        self.checked = checked
        self.callback = callback

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered or pygame.Rect(self.rect.x, self.rect.y, 200, 20).collidepoint(event.pos):
                self.checked = not self.checked
                if self.callback: self.callback(self.checked)
                return True
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, (48, 54, 61), self.rect, border_radius=4)
        if self.checked:
            pygame.draw.rect(surface, ACCENT_BLUE, self.rect.inflate(-6, -6), border_radius=2)
        
        lbl_surf = FONT_MD.render(self.label, True, TEXT_PRIMARY)
        lbl_rect = lbl_surf.get_rect(midleft=(self.rect.right + 12, self.rect.centery))
        surface.blit(lbl_surf, lbl_rect)

class SpinBox(UIComponent):
    def __init__(self, x, y, w, label, val, min_val, max_val, callback=None):
        super().__init__(x, y, w, 32)
        self.label = label
        self.val = val
        self.min_val = min_val
        self.max_val = max_val
        self.callback = callback
        self.editing = False
        self.temp_text = str(val)
        
        btn_w = 32
        self.btn_minus = Button(x + w - btn_w*2 - 8, y, btn_w, btn_w, "-", color=(33, 38, 45), callback=self.decrement)
        self.btn_plus = Button(x + w - btn_w, y, btn_w, btn_w, "+", color=(33, 38, 45), callback=self.increment)
        self.val_rect = pygame.Rect(self.rect.x + 95, self.rect.y, 50, 32)

    def decrement(self):
        if self.val > self.min_val:
            self.val -= 1; self.temp_text = str(self.val)
            if self.callback: self.callback(self.val)

    def increment(self):
        if self.val < self.max_val:
            self.val += 1; self.temp_text = str(self.val)
            if self.callback: self.callback(self.val)

    def handle_event(self, event):
        if self.btn_minus.handle_event(event) or self.btn_plus.handle_event(event): return True
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.val_rect.collidepoint(event.pos):
                self.editing = True
                self.temp_text = str(self.val)
                return True
            else:
                if self.editing:
                    self.finish_edit()
                self.editing = False
        
        if self.editing and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.finish_edit(); self.editing = False
            elif event.key == pygame.K_BACKSPACE:
                self.temp_text = self.temp_text[:-1]
            elif event.unicode.isdigit() and len(self.temp_text) < 3:
                self.temp_text += event.unicode
            return True
        return False

    def finish_edit(self):
        try:
            v = int(self.temp_text)
            self.val = max(self.min_val, min(self.max_val, v))
            self.temp_text = str(self.val)
            if self.callback: self.callback(self.val)
        except ValueError:
            self.temp_text = str(self.val)

    def draw(self, surface):
        lbl_surf = FONT_MD.render(self.label, True, TEXT_PRIMARY)
        surface.blit(lbl_surf, (self.rect.x, self.rect.y + 6))
        
        # Value Box Glow if editing
        if self.editing:
            pygame.draw.rect(surface, (88, 166, 255, 100), self.val_rect.inflate(4, 4), border_radius=8)
        
        pygame.draw.rect(surface, (13, 17, 23), self.val_rect, border_radius=6)
        border_col = ACCENT_BLUE if self.editing else (48, 54, 61)
        pygame.draw.rect(surface, border_col, self.val_rect, 1 if not self.editing else 2, border_radius=6)
        
        display_text = self.temp_text if self.editing else str(self.val)
        if self.editing and (pygame.time.get_ticks() // 500) % 2 == 0:
            display_text += "|"
            
        val_surf = FONT_MD.render(display_text, True, TEXT_PRIMARY)
        val_txt_rect = val_surf.get_rect(center=self.val_rect.center)
        surface.blit(val_surf, val_txt_rect)
        
        self.btn_minus.rect.x = self.val_rect.right + 10
        self.btn_plus.rect.x = self.btn_minus.rect.right + 8
        self.btn_minus.draw(surface)
        self.btn_plus.draw(surface)

class Dropdown(UIComponent):
    def __init__(self, x, y, w, options, label, current_idx=0):
        super().__init__(x, y, w, 36)
        self.options = options
        self.label = label
        self.current_idx = current_idx
        self.expanded = False

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.expanded:
                for i in range(len(self.options)):
                    opt_rect = pygame.Rect(self.rect.x, self.rect.bottom + i*36, self.rect.w, 36)
                    if opt_rect.collidepoint(event.pos):
                        self.current_idx = i
                        self.expanded = False
                        return True
                self.expanded = False
            elif self.is_hovered:
                self.expanded = True
                return True
        return False

    def draw(self, surface):
        lbl_surf = FONT_SM.render(self.label, True, TEXT_SECONDARY)
        surface.blit(lbl_surf, (self.rect.x, self.rect.y - 20))
        
        # Glow if expanded
        if self.expanded:
            pygame.draw.rect(surface, (88, 166, 255, 60), self.rect.inflate(4, 4), border_radius=8)
            
        pygame.draw.rect(surface, (33, 38, 45), self.rect, border_radius=6)
        border_col = ACCENT_BLUE if self.expanded or self.is_hovered else (48, 54, 61)
        pygame.draw.rect(surface, border_col, self.rect, 1 if not self.expanded else 2, border_radius=6)
        
        txt_surf = FONT_MD.render(self.options[self.current_idx], True, TEXT_PRIMARY)
        surface.blit(txt_surf, (self.rect.x + 12, self.rect.y + 8))
        
        # Arrow
        color = ACCENT_BLUE if self.is_hovered else TEXT_SECONDARY
        arrow_y = self.rect.centery + (2 if self.expanded else -2)
        pygame.draw.polygon(surface, color, [
            (self.rect.right - 25, arrow_y), 
            (self.rect.right - 10, arrow_y), 
            (self.rect.right - 17.5, arrow_y + (-6 if self.expanded else 6))
        ])

    def draw_options(self, surface):
        if self.expanded:
            for i, opt in enumerate(self.options):
                opt_rect = pygame.Rect(self.rect.x, self.rect.bottom + i*36, self.rect.w, 36)
                bg_color = (48, 54, 61) if opt_rect.collidepoint(pygame.mouse.get_pos()) else (33, 38, 45)
                pygame.draw.rect(surface, bg_color, opt_rect)
                pygame.draw.rect(surface, (60, 66, 74), opt_rect, 1)
                opt_txt = FONT_MD.render(opt, True, TEXT_PRIMARY)
                surface.blit(opt_txt, (opt_rect.x + 12, opt_rect.y + 8))

# --- Maze Application ---

class MazeApp:
    def __init__(self):
        # Use a more conservative default size and enable resizing
        self.width = 1100
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("Maze Generator & Solver")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # State
        self.rows = 20
        self.cols = 20
        self.northWall = []
        self.eastWall = []
        self.visited = []
        
        self.status = "Ready"
        self.animating = False
        self.step_by_step = False
        self.challenge_mode = False
        self.animation_delay = 50
        
        # Stats
        self.path_length = 0
        self.cells_visited = 0
        self.backtracks = 0
        
        # Algos
        self.generator_iter = None
        self.solver_iter = None
        self.active_gen_cell = None  # Track the current generation "mouse"
        self.solve_path = []
        self.solve_visited = []
        self.dead_ends = []
        self.failed = False
        
        self.init_maze()
        self.init_ui()

    def init_ui(self):
        self.ui_components = []
        x = 35
        y = 180
        w = 280
        
        self.row_spin = SpinBox(x, y, w, "Rows:", self.rows, 5, 50, self.set_rows)
        y += 55
        self.col_spin = SpinBox(x, y, w, "Cols:", self.cols, 5, 50, self.set_cols)
        y += 75
        
        self.gen_drop = Dropdown(x, y, w, ["DFS (Stack) - Tortuous", "BFS (Queue) - Wide"], "Generation Algorithm")
        y += 80
        self.solve_drop = Dropdown(x, y, w, ["Backtracking (Stack)", "BFS Shortest Path", "Shoulder to Wall (Left)"], "Solver Algorithm")
        y += 70
        
        self.ui_components.append(Checkbox(x, y, "Challenge Mode (Cycles)", False, self.set_challenge))
        y += 55
        self.delay_slider = Slider(x, y, w, 0, 500, 50, "Animation Delay")
        y += 65
        self.ui_components.append(Checkbox(x, y, "Step-by-Step Mode", False, self.set_step_by_step))
        
        # Add interactive ones to list
        self.ui_components.extend([self.row_spin, self.col_spin, self.gen_drop, self.solve_drop, self.delay_slider])
        
        # Control Buttons
        y = 620
        self.btn_next = Button(x, y, w, 42, "Next Step", color=(35, 134, 54), callback=self.trigger_step, enabled=False)
        y += 50
        self.btn_gen = Button(x, y, w, 42, "Generate Maze", color=ACCENT_BLUE, callback=self.start_generation)
        y += 50
        self.btn_solve = Button(x, y, w, 42, "Solve Maze", color=ACCENT_BLUE, callback=self.start_solving, enabled=False)
        
        self.ui_components.extend([self.btn_next, self.btn_gen, self.btn_solve])
        self.update_layout() # Ensure initial positioning is correct

    def set_rows(self, v): self.rows = v; self.init_maze()
    def set_cols(self, v): self.cols = v; self.init_maze()
    def set_challenge(self, v): self.challenge_mode = v
    def set_step_by_step(self, v): 
        self.step_by_step = v
        self.btn_next.enabled = v and self.animating

    def init_maze(self):
        R, C = self.rows, self.cols
        self.northWall = [[1 for _ in range(C + 1)] for _ in range(R + 1)]
        self.eastWall = [[1 for _ in range(C + 1)] for _ in range(R + 1)]
        self.visited = [[False for _ in range(C + 1)] for _ in range(R + 1)]
        self.solve_path = []
        self.solve_visited = []
        self.dead_ends = []
        self.status = "Ready"
        self.animating = False
        self.generator_iter = None
        self.solver_iter = None
        self.failed = False
        if hasattr(self, 'btn_solve'): self.btn_solve.enabled = False

    def start_generation(self):
        self.init_maze()
        self.animating = True
        self.status = "Generating..."
        self.btn_next.enabled = self.step_by_step
        if self.gen_drop.current_idx == 0: self.generator_iter = self.gen_dfs()
        else: self.generator_iter = self.gen_bfs()

    def start_solving(self):
        self.animating = True
        self.status = "Solving..."
        self.btn_next.enabled = self.step_by_step
        self.solve_path = []
        self.solve_visited = []
        self.dead_ends = []
        self.path_length = 0
        self.cells_visited = 0
        self.backtracks = 0
        self.failed = False
        idx = self.solve_drop.current_idx
        if idx == 0: self.solver_iter = self.solve_backtrack()
        elif idx == 1: self.solver_iter = self.solve_bfs()
        else: self.solver_iter = self.solve_shoulder()

    def trigger_step(self):
        self.update_algorithm()

    def gen_dfs(self):
        R, C = self.rows, self.cols
        start_r, start_c = random.randint(1, R), random.randint(1, C)
        stack = [(start_r, start_c)]
        self.visited[start_r][start_c] = True
        while stack:
            r, c = stack[-1]
            neighbors = []
            if r < R and not self.visited[r+1][c]: neighbors.append(('U', r+1, c))
            if r > 1 and not self.visited[r-1][c]: neighbors.append(('D', r-1, c))
            if c < C and not self.visited[r][c+1]: neighbors.append(('R', r, c+1))
            if c > 1 and not self.visited[r][c-1]: neighbors.append(('L', r, c-1))
            if neighbors:
                move, nr, nc = random.choice(neighbors)
                if move == 'U': self.northWall[r][c] = 0
                elif move == 'D': self.northWall[r-1][c] = 0
                elif move == 'R': self.eastWall[r][c] = 0
                elif move == 'L': self.eastWall[r][c-1] = 0
                if self.challenge_mode and random.random() < 0.05:
                    self.remove_random_wall()
                self.visited[nr][nc] = True
                self.active_gen_cell = (nr, nc)
                stack.append((nr, nc))
                yield
            else:
                self.active_gen_cell = stack.pop()
                yield
        self.active_gen_cell = None
        self.finish_gen()

    def gen_bfs(self):
        R, C = self.rows, self.cols
        start_r, start_c = random.randint(1, R), random.randint(1, C)
        queue = deque([(start_r, start_c)])
        self.visited[start_r][start_c] = True
        while queue:
            r, c = queue.popleft()
            neighbors = []
            if r < R and not self.visited[r+1][c]: neighbors.append(('U', r+1, c))
            if r > 1 and not self.visited[r-1][c]: neighbors.append(('D', r-1, c))
            if c < C and not self.visited[r][c+1]: neighbors.append(('R', r, c+1))
            if c > 1 and not self.visited[r][c-1]: neighbors.append(('L', r, c-1))
            random.shuffle(neighbors)
            for move, nr, nc in neighbors:
                if not self.visited[nr][nc]:
                    if move == 'U': self.northWall[r][c] = 0
                    elif move == 'D': self.northWall[r-1][c] = 0
                    elif move == 'R': self.eastWall[r][c] = 0
                    elif move == 'L': self.eastWall[r][c-1] = 0
                    self.visited[nr][nc] = True
                    self.active_gen_cell = (nr, nc)
                    queue.append((nr, nc))
                    yield
        self.active_gen_cell = None
        self.finish_gen()

    def remove_random_wall(self):
        R, C = self.rows, self.cols
        if random.choice([True, False]):
            r, c = random.randint(1, R-1), random.randint(1, C); self.northWall[r][c] = 0
        else:
            r, c = random.randint(1, R), random.randint(1, C-1); self.eastWall[r][c] = 0

    def finish_gen(self):
        self.animating = False
        self.status = "Maze Ready"
        self.btn_solve.enabled = True
        self.btn_next.enabled = False
        self.eastWall[self.rows][0] = 0 # Start opening
        self.eastWall[1][self.cols] = 0 # End opening
        
        # Guarantee cycles in Challenge Mode by removing extra walls at the end
        if self.challenge_mode:
            R, C = self.rows, self.cols
            extra_walls = (R * C) // 15 # Remove ~7% more walls
            for _ in range(extra_walls):
                self.remove_random_wall()

    def solve_backtrack(self):
        R, C = self.rows, self.cols
        start, end = (R, 1), (1, C)
        stack = [start]
        visited = {start}
        while stack:
            r, c = stack[-1]
            self.cells_visited += 1
            if (r, c) == end: self.status = "Solved!"; self.animating = False; yield; return
            neighbors = []
            if r < R and self.northWall[r][c] == 0 and (r+1, c) not in visited: neighbors.append((r+1, c))
            if r > 1 and self.northWall[r-1][c] == 0 and (r-1, c) not in visited: neighbors.append((r-1, c))
            if c < C and self.eastWall[r][c] == 0 and (r, c+1) not in visited: neighbors.append((r, c+1))
            if c > 1 and self.eastWall[r][c-1] == 0 and (r, c-1) not in visited: neighbors.append((r, c-1))
            if neighbors:
                nr, nc = random.choice(neighbors)
                visited.add((nr, nc))
                stack.append((nr, nc))
                self.solve_path = list(stack)
                self.path_length = len(self.solve_path); yield
            else:
                self.dead_ends.append(stack.pop())
                self.solve_path = list(stack)
                self.backtracks += 1; yield
        self.status = "FAILED"; self.failed = True; self.animating = False

    def solve_bfs(self):
        R, C = self.rows, self.cols
        start, end = (R, 1), (1, C)
        queue = deque([start]); parents = {start: None}; visited = {start}
        while queue:
            r, c = queue.popleft(); self.cells_visited += 1; self.solve_visited.append((r, c))
            if (r, c) == end:
                path = []
                curr = end
                while curr: path.append(curr); curr = parents[curr]
                self.solve_path = path[::-1]; self.path_length = len(self.solve_path)
                self.status = "Solved!"; self.animating = False; yield; return
            moves = []
            if r < R and self.northWall[r][c] == 0: moves.append((r+1, c))
            if r > 1 and self.northWall[r-1][c] == 0: moves.append((r-1, c))
            if c < C and self.eastWall[r][c] == 0: moves.append((r, c+1))
            if c > 1 and self.eastWall[r][c-1] == 0: moves.append((r, c-1))
            for nr, nc in moves:
                if (nr, nc) not in visited:
                    visited.add((nr, nc)); parents[(nr, nc)] = (r, c); queue.append((nr, nc))
            yield

    def solve_shoulder(self):
        R, C = self.rows, self.cols
        r, c = R, 1; d = 1; end = (1, C)
        self.solve_path = [(r, c)]; steps = 0; max_s = R * C * 4
        while (r, c) != end:
            steps += 1
            if steps > max_s: self.status = "Cycle Detected!"; self.failed = True; self.animating = False; yield; return
            d = (d - 1) % 4
            while self.has_wall(r, c, d): d = (d + 1) % 4
            if d == 0: r += 1
            elif d == 1: c += 1
            elif d == 2: r -= 1
            elif d == 3: c -= 1
            self.solve_path.append((r, c)); self.path_length = len(self.solve_path); self.cells_visited += 1; yield
        self.status = "Solved!"; self.animating = False

    def has_wall(self, r, c, d):
        R, C = self.rows, self.cols
        if d == 0: return r == R or self.northWall[r][c] == 1
        if d == 1: return c == C or self.eastWall[r][c] == 1
        if d == 2: return r == 1 or self.northWall[r-1][c] == 1
        if d == 3: return c == 1 or self.eastWall[r][c-1] == 1
        return True

    def update_algorithm(self):
        if self.generator_iter:
            try: next(self.generator_iter)
            except StopIteration: self.generator_iter = None
        elif self.solver_iter:
            try: next(self.solver_iter)
            except StopIteration: self.solver_iter = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            
            if event.type == pygame.VIDEORESIZE:
                self.width, self.height = event.size
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                self.update_layout() # Recalculate component positions
            
            # Handle dropdowns first (z-index)
            if self.gen_drop.expanded:
                if self.gen_drop.handle_event(event): return
            elif self.solve_drop.expanded:
                if self.solve_drop.handle_event(event): return
            else:
                for comp in self.ui_components:
                    if comp.handle_event(event): break

    def update_layout(self):
        # Dynamic layout constants
        global LEFT_PANEL_WIDTH, MAZE_AREA_WIDTH, MAZE_AREA_HEIGHT, SCREEN_HEIGHT, SCREEN_WIDTH
        SCREEN_WIDTH, SCREEN_HEIGHT = self.width, self.height
        MAZE_AREA_WIDTH = SCREEN_WIDTH - LEFT_PANEL_WIDTH
        MAZE_AREA_HEIGHT = SCREEN_HEIGHT - BOTTOM_PANEL_HEIGHT
        
        # Update component positions
        x = 35
        y = 135
        w = LEFT_PANEL_WIDTH - 70
        
        v_gap = 75 # Standardized vertical gap
        
        self.row_spin.rect.update(x, y, w, 32); y += v_gap
        self.col_spin.rect.update(x, y, w, 32); y += v_gap
        self.gen_drop.rect.update(x, y, w, 36); y += v_gap + 10
        self.solve_drop.rect.update(x, y, w, 36); y += v_gap + 5
        
        self.delay_slider.rect.update(x, y + 15, w, 20); 
        self.delay_slider.update_thumb_pos() # Fix floating thumb
        y += v_gap
        
        # Find checkboxes and position them
        for comp in self.ui_components:
            if isinstance(comp, Checkbox):
                if "Challenge" in comp.label:
                    comp.rect.update(x, self.solve_drop.rect.bottom + 15, 18, 18)
                else:
                    comp.rect.update(x, self.delay_slider.rect.bottom + 15, 18, 18)
        
        # Anchor buttons to bottom of panel
        btn_y = SCREEN_HEIGHT - 230
        self.btn_next.rect.update(x, btn_y, w, 42); btn_y += 50
        self.btn_gen.rect.update(x, btn_y, w, 42); btn_y += 50
        self.btn_solve.rect.update(x, btn_y, w, 42)
        
        # Status Bar
        # Handled in draw for simplicity

    def update(self):
        if self.animating and not self.step_by_step:
            delay = int(self.delay_slider.current_val)
            if delay == 0:
                for _ in range(5): self.update_algorithm()
            else:
                self.update_algorithm()
                pygame.time.delay(delay)

    def draw(self):
        self.screen.fill(BG_COLOR)
        
        # Left Panel Base
        pygame.draw.rect(self.screen, PANEL_COLOR, (0, 0, LEFT_PANEL_WIDTH, SCREEN_HEIGHT))
        pygame.draw.line(self.screen, PANEL_BORDER, (LEFT_PANEL_WIDTH, 0), (LEFT_PANEL_WIDTH, SCREEN_HEIGHT), 1)
        
        # Header Area (Right)
        title_x = LEFT_PANEL_WIDTH + 50
        title_surf = FONT_TITLE.render("Maze Generator & Solver", True, ACCENT_BLUE)
        self.screen.blit(title_surf, (title_x, 40))
        sub_surf = FONT_SUB.render("Visualize algorithms in real-time.", True, TEXT_SECONDARY)
        self.screen.blit(sub_surf, (title_x, 95))
        
        # Configuration Box (Glassmorphism effect)
        config_h = min(480, SCREEN_HEIGHT - 320)
        config_rect = pygame.Rect(20, 85, LEFT_PANEL_WIDTH - 40, config_h)
        
        # Subtle semi-transparent overlay
        s = pygame.Surface((config_rect.w, config_rect.h), pygame.SRCALPHA)
        pygame.draw.rect(s, (33, 38, 45, 120), (0, 0, config_rect.w, config_rect.h), border_radius=12)
        self.screen.blit(s, (config_rect.x, config_rect.y))
        
        pygame.draw.rect(self.screen, PANEL_BORDER, config_rect, 1, border_radius=12)
        
        header_lbl = FONT_LG.render("Configuration", True, TEXT_PRIMARY)
        self.screen.blit(header_lbl, (40, 100))
        
        # UI Components
        for comp in self.ui_components:
            comp.draw(self.screen)
        
        # Status Bar Styling (Anchored to bottom)
        status_rect = pygame.Rect(20, SCREEN_HEIGHT - 70, LEFT_PANEL_WIDTH - 40, 48)
        pygame.draw.rect(self.screen, (13, 17, 23), status_rect, border_radius=10)
        pygame.draw.rect(self.screen, PANEL_BORDER, status_rect, 1, border_radius=10)
        
        color = ACCENT_RED if self.failed else (ACCENT_GREEN if "Solved" in self.status else TEXT_PRIMARY)
        status_txt = FONT_LG.render(self.status, True, color)
        self.screen.blit(status_txt, status_txt.get_rect(center=status_rect.center))
        
        # Draw Dropdown Options (Top-most)
        self.gen_drop.draw_options(self.screen)
        self.solve_drop.draw_options(self.screen)
        
        # Maze & Stats
        self.draw_maze()
        self.draw_stats()
        
        pygame.display.flip()

    def draw_maze(self):
        margin = 60
        area_w, area_h = MAZE_AREA_WIDTH - margin*2, MAZE_AREA_HEIGHT - margin*2 - 50
        cell_size = min(area_w / self.cols, area_h / self.rows)
        
        ox = LEFT_PANEL_WIDTH + (MAZE_AREA_WIDTH - cell_size * self.cols) // 2
        oy = 150 + (area_h - cell_size * self.rows) // 2
        
        # Grid Background
        maze_rect = pygame.Rect(ox, oy, self.cols*cell_size, self.rows*cell_size)
        pygame.draw.rect(self.screen, GRID_COLOR, maze_rect, border_radius=4)
        
        # Generation Progress
        if self.generator_iter or self.animating:
            for r in range(1, self.rows+1):
                for c in range(1, self.cols+1):
                    if self.visited[r][c]:
                        rect = pygame.Rect(ox + (c-1)*cell_size, oy + (self.rows-r)*cell_size, cell_size, cell_size)
                        pygame.draw.rect(self.screen, VISITED_COLOR, rect.inflate(-2, -2))
            
            # Active generation mouse
            if self.active_gen_cell:
                r, c = self.active_gen_cell
                center = (int(ox + (c-0.5)*cell_size), int(oy + (self.rows-r+0.5)*cell_size))
                pygame.draw.circle(self.screen, PATH_COLOR, center, cell_size // 2.5)
                pygame.draw.circle(self.screen, (255, 255, 255), center, cell_size // 4, 2)

        # Solve Progress
        # Draw all visited cells as blue dots first
        for r, c in self.solve_visited:
            center = (int(ox + (c-0.5)*cell_size), int(oy + (self.rows-r+0.5)*cell_size))
            pygame.draw.circle(self.screen, DEAD_END_COLOR, center, cell_size // 2.5)
            
        # Draw dead ends as blue dots (redundant if solve_visited covers it, but good for clarity)
        for r, c in self.dead_ends:
            center = (int(ox + (c-0.5)*cell_size), int(oy + (self.rows-r+0.5)*cell_size))
            pygame.draw.circle(self.screen, DEAD_END_COLOR, center, cell_size // 2.5)

        # Draw current path as red dots
        if self.solve_path:
            for r, c in self.solve_path:
                center = (int(ox + (c-0.5)*cell_size), int(oy + (self.rows-r+0.5)*cell_size))
                pygame.draw.circle(self.screen, PATH_COLOR, center, cell_size // 2.5)
            
            # Current mouse head (optional extra glow or marker)
            curr_r, curr_c = self.solve_path[-1]
            center = (int(ox + (curr_c-0.5)*cell_size), int(oy + (self.rows-curr_r+0.5)*cell_size))
            pygame.draw.circle(self.screen, (255, 255, 255), center, cell_size // 4, 2)

        # Walls
        for r in range(self.rows + 1):
            for c in range(self.cols + 1):
                x, y = ox + (c-1)*cell_size, oy + (self.rows-r)*cell_size
                if r <= self.rows and c >= 1 and c <= self.cols and self.northWall[r][c]:
                    pygame.draw.line(self.screen, WALL_COLOR, (x, y), (x + cell_size, y), 2)
                if c <= self.cols and r >= 1 and r <= self.rows and self.eastWall[r][c]:
                    pygame.draw.line(self.screen, WALL_COLOR, (x + cell_size, y), (x + cell_size, y + cell_size), 2)

        # Emojis
        emoji_font = get_font(int(cell_size * 0.8), True)
        m_lbl = emoji_font.render("🐭", True, TEXT_PRIMARY)
        self.screen.blit(m_lbl, (ox + cell_size*0.1, oy + cell_size*0.1))
        c_lbl = emoji_font.render("🧀", True, TEXT_PRIMARY)
        self.screen.blit(c_lbl, (ox + (self.cols-1.1)*cell_size, oy + (self.rows-1.1)*cell_size))

    def draw_stats(self):
        panel_y = SCREEN_HEIGHT - BOTTOM_PANEL_HEIGHT
        pygame.draw.line(self.screen, PANEL_BORDER, (LEFT_PANEL_WIDTH, panel_y), (SCREEN_WIDTH, panel_y), 1)
        
        stats = [("PATH LENGTH", self.path_length), ("CELLS VISITED", self.cells_visited), ("BACKTRACKS", self.backtracks)]
        spacing = (SCREEN_WIDTH - LEFT_PANEL_WIDTH) // 3
        for i, (label, val) in enumerate(stats):
            x = LEFT_PANEL_WIDTH + spacing * i + spacing // 2
            lbl = FONT_SM.render(label, True, TEXT_SECONDARY)
            self.screen.blit(lbl, lbl.get_rect(center=(x, panel_y + 35)))
            val_txt = FONT_TITLE.render(str(val), True, ACCENT_BLUE)
            self.screen.blit(val_txt, val_txt.get_rect(center=(x, panel_y + 70)))

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    MazeApp().run()
