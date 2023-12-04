#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 11:31:52 2023

@author: sebastianpedraza
"""

from Maze import *
from typing import Dict, Tuple, Type, List


'Libraries to plot mazes, associated graphs and algorithms step by step'
import matplotlib.pyplot as plt
import networkx as nx


class MazeVisualizer:
    """
    Class to visualize a maze and the steps taken to solve it.
    
    Attributes:
    maze (Maze): The maze to visualize.

    """
    def __init__(self, maze: Type['Maze']):
        
        self.maze = maze

    def visualize(self):
        """
        Draw the  initial maze  using Matplotlib.

        Parameters: Maze
        
        Returns: Shows the initial maze
        """
        
        plt.figure(figsize=(8, 8))
        plt.imshow(self.maze.maze, cmap='binary', interpolation='nearest')
        plt.plot(self.maze.start[0], self.maze.start[1], 'go', markersize=10)
        plt.plot(self.maze.end[0], self.maze.end[1], 'ro', markersize=10)
        plt.axis('off')
        plt.show()


    def solution(self, path: List[Tuple[int, int]]) -> None:
        """
        Draw the maze solution using Matplotlib.

        Parameters: Maze
        
        Returns: Shows the maze solution
        """

        if path:
            plt.figure(figsize=(8, 8))

            plt.imshow(self.maze.maze, cmap='binary', interpolation='nearest')

            plt.plot(self.maze.start[0], self.maze.start[1], 'go', markersize=10)
            plt.plot(self.maze.end[0], self.maze.end[1], 'ro', markersize=10)
            path_x, path_y = zip(*path)
            plt.plot(path_x, path_y, color='blue', linewidth=2)
            plt.axis('off')
            plt.show()
        else:
            print("maze without solution.")


    
    
    def steps(self, current: [Tuple[int, int]], visited: List[Tuple[int, int]]) -> None:
        """
        Draw the steps of the  algorithms using Matplotlib.
        
        Parameters: visited_nodes (List[Tuple[int, int]])
        
        Returns: Shows the steps of the  algorithm
        """
    
        plt.figure(figsize=(8, 8))
        plt.imshow(self.maze.maze, cmap='binary', interpolation='nearest')
        plt.plot(self.maze.start[0], self.maze.start[1], 'go', markersize=10)
        plt.plot(self.maze.end[0], self.maze.end[1], 'ro', markersize=10)
        if visited:
            for point in visited:
                plt.plot(point[0], point[1], 'bs', markersize=10)
        if current:
            plt.plot(current[0], current[1], 'ms', markersize=10) 
        plt.axis('off')
        plt.show()
        
        
    def graph(self):
        '''
        '''
        nx.draw(nx.Graph(self.maze.associated_graph), nx.spring_layout(nx.Graph(self.maze.associated_graph)), with_labels=True, node_color='blue', font_color='white')
        plt.show()


