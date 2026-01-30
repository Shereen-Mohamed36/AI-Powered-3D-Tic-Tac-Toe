
An advanced 3D Tic-Tac-Toe game featuring a sophisticated AI with multiple search algorithms and evaluation heuristics. Built using Python and Tkinter, this project demonstrates high-level AI concepts like **Minimax**, **Alpha-Beta Pruning**, and **State-Space Optimization**.

##  Key Features
- **3D Gameplay:** Played on a 4x4x4 grid (64 positions) across 4 layers.
- **Multiple AI Algorithms:**
  - **Minimax:** Standard recursive search.
  - **Alpha-Beta Pruning:** Optimized search that cuts down computation time by ~80%.
- **Heuristic Engine:** Two different heuristic evaluation functions (Basic vs. Advanced Positional) to score the board.
- **Modern UI:** Sleek Dark-Mode interface with real-time performance tracking (Timer & Move analysis).
- **Benchmarking:** Compare AI decision speed and intelligence between different algorithms.

##  AI Concepts Implemented
- **Alpha-Beta Pruning:** To handle the massive search tree of a 3D board.
- **Memoization:** Caching board states to avoid redundant calculations.
- **Positional Weighting:** Scoring centers, corners, and edges differently to mimic human strategic thinking.

## How to Run
```bash
python main.py

