#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 11:31:11 2023

@author: sebastianpedraza
"""

from typing import Dict, Tuple, Type, List

'Libraries to generate mazes'
import numpy as np
from random import shuffle

class Maze:
    """
    Class to represent a maze.
    
    Attributes:
        
    height/width: Maze dimension
    
    maze (np.ndarray): Maze represented as a NumPy array.
        [[1 1 ... 1 1]
         [1 0 ... 0 1]
         [. . ... . .]
         [1 1 ... 1 1]]
    zero represents a passable cell and 1 represents a non-transitable cell.
    
    associated_graph (Dict[Tuple[int, int], List[[Tuple[int,int], Tuple[int, int]]]]): Graph associated with the maze.
    G = {v1: [adjacents vertices to v1], v2: [adjacents vertices to v2], ...,  vn: [adjacents vertices to vn]}
    
    start/end: (x,y) start/end point

    """
    def __init__(self, maze: List[List[int]], maze_height: int, maze_width: int):
        """
        Initialize the Maze with the given height, width, and maze layout.
        
        Args:
        maze (List[List[int]]): The layout of the maze.
        maze_height (int): The height of the maze.
        maze_width (int): The width of the maze.
        """
        
        self.maze_height: int                               = maze_height
        self.maze_width: int                                = maze_width
        self.maze: List[List[int]]                          = maze
        self.start: Tuple[int,int]                          = (1, 1)
        self.end: Tuple[int,int]                            = (maze_width - 2, maze_height -2)
        self.associated_graph: Dict[Tuple[int,int]: Tuple]  = self.maze_to_graph(maze)
        # self.contracted_graph: Dict[Tuple[int,int]: Tuple]  = self.graph_contractor(self.maze_to_graph(maze))
        
        

    def maze_to_graph(self, maze):
        return {(x, y): list((nx, ny) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)] if 0 <= (nx := x + dx) < len(maze[0]) and 0 <= (ny := y + dy) < len(maze) and maze[ny][nx] == 0)
        for y in range(len(maze)) for x in range(len(maze[y])) if maze[y][x] == 0}
    
    def graph_contractor(self, graph):
        return {node: [neighbor2 for neighbor1 in neighbors for neighbor2 in graph[neighbor1] if neighbor2 != node] for node, neighbors in graph.items() if len(neighbors) != 2}
    
    
    

    @classmethod
    def backtrack_generator(cls, maze_height: int = 9, maze_width: int = 9 ) -> Type['Maze']:
        """
        Generates a maze using backtrack algorithm.

        Parameters:
            maze_width (int).
            maze_height (int).

        Returns: Maze matrix 
        """
        maze = np.ones((maze_height, maze_width), dtype=int)

        def is_valid(x, y):
            return 0 <= x < maze_width and 0 <= y < maze_height and maze[y, x] == 1

        def backtrack(x, y):
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + 2 * dx, y + 2 * dy
                if is_valid(nx, ny):
                    maze[y + dy, x + dx] = 0
                    maze[ny, nx] = 0
                    backtrack(nx, ny)

        start_x, start_y = 1, 1
        maze[start_y, start_x] = 0
        backtrack(start_x, start_y)
        
        
        return cls(maze, maze_height, maze_width)

    @classmethod
    def empty_maze(cls, maze_height: int = 11, maze_width: int = 11 ) -> Type['Maze']:
        """
        Generates an empty maze with a border.
    
        Parameters:
            maze_width (int).
            maze_height (int).
    
        Returns: Maze matrix 
        """
        maze        = np.zeros((maze_height, maze_width), dtype=int)
        maze[0, :]  = maze[-1, :] = 1
        maze[:, 0]  = maze[:, -1] = 1
        
        return cls(maze, maze_height, maze_width)
    
    
