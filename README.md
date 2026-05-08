# Maze Generator & Solver

A robust, interactive Python application built with **Pygame** to visualize maze generation and solving algorithms. This project implements a variety of search and traversal techniques on a custom 2D grid structure.

## 🚀 Features

- **Interactive UI**: Custom-built dark-themed UI with glassmorphism effects.
- **Dynamic Grid**: Adjust rows and columns (5 to 50) in real-time via spin-boxes or direct text input.
- **Responsive Design**: Resizable window with an adaptive layout.
- **Generation Animations**: Watch the "mouse" carve paths through the grid.
- **Solver Animations**: Visualize pathfinding with real-time stats (Path Length, Cells Visited, Backtracks).

## 🐭 Generation Algorithms

- **DFS (Depth-First Search)**: Uses a stack to create long, tortuous paths for a challenging maze.
- **BFS (Breadth-First Search)**: Uses a queue to generate highly branching mazes with shorter corridors.
- **Challenge Mode**: Introduces cycles (loops) into the maze, transforming it from a "perfect" tree into a more complex network.

## 🧀 Solver Algorithms

- **Backtracking (Stack-based)**: A recursive-style search that visually marks dead ends in blue and the active path in red.
- **BFS (Shortest Path)**: Guarantees finding the absolute shortest route through the maze using a breadth-first expansion.
- **Shoulder-to-Wall (Left-Hand Rule)**: A navigation strategy that follows the wall on the left. Includes **Cycle Detection** to identify loops in Challenge Mode mazes.

## 🛠️ Technical Details

- **Language**: Python 3.15+
- **Library**: Pygame CE (Community Edition)
- **Data Structures**:
  - `northWall[R][C]`: 2D array managing horizontal walls.
  - `eastWall[R][C]`: 2D array managing vertical walls.
  - Supports "phantom row 0" and custom left-edge entrance gaps as per project requirements.

## 🏃 Getting Started

1.  **Install Dependencies**:
    ```bash
    pip install pygame-ce
    ```

2.  **Run the Application**:
    ```bash
    py maze.py
    ```

## 🎮 Controls

- **Rows/Cols**: Click the +/- buttons or click the number to type a value.
- **Next Step**: Manually advance the algorithm when "Step-by-Step Mode" is enabled.
- **Animation Delay**: Use the slider to speed up or slow down the visualization.
- **Generate/Solve**: Click to start the selected algorithm.
