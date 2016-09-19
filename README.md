# npuzzle-search
Simple implementation of basic graph search methods applied to the N-Puzzle problem.

# About

This project is a simple and concise implementation of graph search methods that I developed as an undergraduate student at UFMG. The following algorithms are included in the code:
  * Greedy Search (Manhattan Distance)
  * A* Search (Manhattan Distance)
  * Breadth-first Search
  * Uniform Cost Search
  * Iterative Deepening Search
  
**Disclaimer:** the project is not meant to be a reference implementation for the above algorithms.

# Example Run

```
user@my-desktop:~$ python npuzzle.py

Running greedy algorithm...
Found a solution costing 39 steps in 0.0047 seconds

Running astar algorithm...
Found a solution costing 31 steps in 1.0394 seconds

Running breadth algorithm...
Found a solution costing 31 steps in 7.7959 seconds

Running ucs algorithm...
Found a solution costing 31 steps in 23.0636 seconds

Running ids algorithm...
Found a solution costing 31 steps in 53.7837 seconds

```