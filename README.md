# MazeMaster Pro - Advanced CG Engine

A high-performance maze generation and solving application built with Python and CustomTkinter. This project implements a sophisticated "mouse" logic for maze creation and a backtracking algorithm for pathfinding.

## 🚀 Features
- **Dynamic Maze Generation**: Uses a stack-based Depth-First Search (DFS) algorithm.
- **Backtracking Solver**: Visualizes the solution path with real-time dead-end tracking.
- **Holographic UI**: Premium Cyberpunk-themed interface with high-contrast metric cards.
- **System Diagnostics**: Real-time logging of stack operations (PUSH/POP).
- **Challenge Mode (Bonus)**: 
  - **Cycle Creation**: 5% chance to create loops by carving extra walls.
  - **Random Interior Start/End**: Entry and exit points are randomized within the maze interior.

## 🧠 How it Works

### Maze Generation (The "Mouse" Logic)
The generator uses a **stack-based DFS** algorithm, often described as an "invisible mouse" eating through walls:
1. The mouse starts at a random cell and checks for unvisited neighbors.
2. It chooses a neighbor randomly, removes the dividing wall, and pushes the current location to a **stack**.
3. If the mouse becomes trapped (no unvisited neighbors), it **pops** the stack to backtrack to the last available junction.
4. The process continues until the stack is empty, ensuring a "proper" maze where every cell is connected.

### Maze Solver
The solver utilizes a **Backtracking** algorithm:
- **Red Dots**: Represent the current path (cells on the stack).
- **Blue Dots**: Mark dead ends that have been explored and discarded.
- The solver systematically explores the "tree" structure of the maze until the target "E" marker is reached.

## 🛠️ Requirements
- Python 3.x
- CustomTkinter (`pip install customtkinter`)

## 📜 Submission Details
This project fulfills all requirements for the **CG Assignment 1**, including the data structure implementation for `northWall` and `eastWall` and the bonus points for cycle creation and interior start/end positioning.
