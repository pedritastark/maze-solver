#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 11:34:01 2023

@author: sebastianpedraza
"""

from Maze import *
from MazeVisualizer import *


'Libraries to implement algorithms'
from collections import deque
import heapq
from random import choice


class MazeSolver:
    """
    Class to solve a given maze throw graph algorithms.
    
    Attributes:
    maze (Maze): The maze to solve.
    visualizer (MazeVisualizer): The visualizer to visualize the steps and solution.
    
    Methods: Algorithms to solve the maze throw graphs (bfs, dfs, dijsktra, A*, bi-directional).
    """
    def __init__(self, maze, visualizer):
        
        self.maze       = maze
        self.visualizer = visualizer


    def bfs(self, setps: bool = False, solution: bool = False):
        """        
        Solve maze using BFS algorithm.
    
        Parameters: 
        - setps: If True, visualize each step of the algorithm.
        - solution: If True, visualize the solution path.

        
    
    
        Returns: List[Tuple[int, int]] ->  List of tuples that represent the path from the start to the end of the maze.
                  each tuple contains the (x, y) coordinates of a position on the path.
                  If there is no solution, it returns an empty list.
                  
                  Optional -> show step by stept the algorithm 
                              show solution
        """
        
        graph       = self.maze.associated_graph # Get the graph associated with the maze
        queue       = deque([self.maze.start]) # Initialize a queue with the start node
        previous    = {self.maze.start: None}  # dict to track of the node that led to each node
        visited     = []     # Keep track of visited nodes



        while queue:
            node = queue.popleft() # Get the next node
            if node == self.maze.end:
                path = []
                while node is not None:
                    path.append(node)
                    node = previous[node]
                        
                if solution: self.visualizer.solution(path[::-1])
                return path

            # Visit all neighbors of the current node
            for neighbor in graph[node]:
                # If the neighbor has not been visited yet
                if neighbor not in previous:
                    queue.append(neighbor)  # Add it to the queue 
                    previous[neighbor] = node # Add it to track dict with they previous node
                    visited.append(neighbor) # Add it to visited nodes
                    if setps: self.visualizer.steps(neighbor, visited)


        return [] # Return empty list if no path is found
    
    
    def dfs(self, steps: bool = False, solution: bool = False):
        """        
        Solve maze using DFS algorithm.
    
        Parameters: Maze, setps, solution
        
    
    
        Returns: List[Tuple[int, int]] ->  List of tuples that represent the path from the start to the end of the maze.
                  each tuple contains the (x, y) coordinates of a position on the path.
                  If there is no solution, it returns an empty list.
                  
                  Optional -> show step by stept the algorithm 
                              show solution
        """
        graph       = self.maze.associated_graph
        stack       = [self.maze.start] # Initialize stack with start node
        previous    = {self.maze.start: None}  # Start node has no previous node
        visited     = []
    
        while stack:
            node = stack.pop()
            # If end node is reached, reconstruct and return path
            if node == self.maze.end:
                path = []
                while node is not None:
                    path.append(node)
                    node = previous[node]
                path = path[::-1]  ## Reverse path
                if solution: self.visualizer.solution(path)
                return path
    
            # For each neighbor of current node
            for neighbor in graph[node]:
                if neighbor not in previous:
                    stack.append(neighbor) # Add neighbor to stack
                    previous[neighbor] = node # Update previous node
                    visited.append(neighbor)
                    if steps: self.visualizer.steps(neighbor, visited)
    
        return [] 



    def dijkstra(self, steps: bool = False, solution: bool = False):
        """        
        Solve maze using Dijkstra algorithm.
    
        Parameters: Maze, setps, solution
        
    
    
        Returns: List[Tuple[int, int]] ->  List of tuples that represent the path from the start to the end of the maze.
                  each tuple contains the (x, y) coordinates of a position on the path.
                  If there is no solution, it returns an empty list.
                  
                  Optional -> show step by stept the algorithm 
                              show solution
        """
        graph       = self.maze
        graph       = self.maze.associated_graph
        heap        = [(0, self.maze.start)]
        distances   = {self.maze.start: 0}
        previous    = {self.maze.start: None}
        visited     = []

        while heap:
            (dist, node) = heapq.heappop(heap)  # Extract node with minimum distance

            # If end node is reached, reconstruct and return path
            if node == self.maze.end:
                path = []
                while node is not None:
                    path.append(node)
                    node = previous[node]
                path = path[::-1]  
                if solution: self.visualizer.solution(path)
                return path


            # For each neighbor of current node
            for neighbor in graph[node]:
                new_dist = distances[node] + 1  # new tentative distance

                # If new distance is shorter
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist  # Update distance
                    heapq.heappush(heap, (new_dist, neighbor))  # Add neighbor to heap
                    previous[neighbor] = node  # Update previous node
                    visited.append(neighbor)
                    if steps: self.visualizer.steps(neighbor, visited)

        return []  
    

    
    

    def heuristic(self, node):
        return abs(node[0] - self.maze.end[0]) + abs(node[1] - self.maze.end[1])
    
    def a_star(self, steps: bool = False, solution: bool = False):
        """        
        Solve maze using A* algorithm.
    
        Parameters: Maze, setps, solution
        
    
    
        Returns: List[Tuple[int, int]] ->  List of tuples that represent the path from the start to the end of the maze.
                  each tuple contains the (x, y) coordinates of a position on the path.
                  If there is no solution, it returns an empty list.
                  
                  Optional -> show step by stept the algorithm 
                              show solution
        """
        
        graph       = self.maze.associated_graph
        heap        = [(0, self.maze.start)]
        distances   = {self.maze.start: 0}
        previous    = {self.maze.start: None}
        visited     = []
    
        while heap:
            (distance, node) = heapq.heappop(heap) # Extract node with minimum distance
            
            # If end node is reached, reconstruct and return path
            if node == self.maze.end:
                path = []
                while node is not None:
                    path.append(node)
                    node = previous[node]
                path = path[::-1]  
                if solution: self.visualizer.solution(path)
                return path
    
            for neighbor in graph[node]:
                new_distance = distances[node] + 1
                
                # If new distance is lower
                if neighbor not in distances or new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    priority = new_distance + self.heuristic(neighbor)
                    heapq.heappush(heap, (priority, neighbor)) # Add neighbor to heap with priority
                    previous[neighbor] = node
                    visited.append(neighbor)
                    if steps: self.visualizer.steps(neighbor, visited)
    
        return []
    
    

        
        
    
        

    
    def bidirectional(self, steps: bool = False, solution: bool = False):
        """        
        Solve maze using bi-directional (bfs) algorithm.
    
        Parameters: Maze, setps, solution
        
    
    
        Returns: List[Tuple[int, int]] ->  List of tuples that represent the path from the start to the end of the maze.
                  each tuple contains the (x, y) coordinates of a position on the path.
                  If there is no solution, it returns an empty list.
                  
                  Optional -> show step by stept the algorithm 
                              show solution
        """
        
        graph               = self.maze.associated_graph
        forward_queue       = [self.maze.start]
        backward_queue      = [self.maze.end]
        forward_previous    = {self.maze.start: None}
        backward_previous   = {self.maze.end: None}
        forward_visited     = []
        backward_visited    = []
    
        while forward_queue and backward_queue:
            # Expand the forward search
            node = forward_queue.pop(0)
            for neighbor in graph[node]:
                if neighbor in backward_previous:
                    # The searches have met, reconstruct the path
                    forward_path = []
                    while node is not None:
                        forward_path.append(node)
                        node = forward_previous[node]
                    forward_path = forward_path[::-1]
    
                    backward_path = []
                    node = neighbor
                    while node is not None:
                        backward_path.append(node)
                        node = backward_previous[node]
    
                    path = forward_path + backward_path
                    if solution: self.visualizer.solution(path)
                    return path
    
                if neighbor not in forward_previous:
                    forward_queue.append(neighbor)
                    forward_previous[neighbor] = node
                    forward_visited.append(neighbor)
                    if steps: self.visualizer.steps(neighbor, forward_visited + backward_visited)
    
            # Expand the backward search
            node = backward_queue.pop(0)
            for neighbor in graph[node]:
                if neighbor in forward_previous:
                    # The searches have met, reconstruct the path
                    forward_path = []
                    node = neighbor
                    while node is not None:
                        forward_path.append(node)
                        node = forward_previous[node]
                    forward_path = forward_path[::-1]
    
                    backward_path = []
                    node = node
                    while node is not None:
                        backward_path.append(node)
                        node = backward_previous[node]
    
                    path = forward_path + backward_path
                    if solution: self.visualizer.solution(path)
                    return path
    
                if neighbor not in backward_previous:
                    backward_queue.append(neighbor)
                    backward_previous[neighbor] = node
                    backward_visited.append(neighbor)
                    if steps: self.visualizer.steps(neighbor, backward_visited + forward_visited)
    
        return []  # No path was found
    
    
    
    def random(self, steps: bool = False, solution: bool = False):
        """        
        Solve maze using random choices .
    
        Parameters: Maze, setps, solution
        
    
    
        Returns: List[Tuple[int, int]] ->  List of tuples that represent the path from the start to the end of the maze.
                  each tuple contains the (x, y) coordinates of a position on the path.
                  If there is no solution, it returns an empty list.
                  
                  Optional -> show step by stept the algorithm 
                              show solution
        """
        graph = self.maze.associated_graph
        start = self.maze.start
        end = self.maze.end
        path = [start]
        visited = {start}
    
        while path[-1] != end:
            current_node = path[-1]
            neighbors = [node for node in graph[current_node] if node not in visited]
            
            if not neighbors:  
                path.pop()
                continue
            
            next_node = neighbors[0] if len(neighbors) == 1 else choice(neighbors)
            path.append(next_node)
            visited.add(next_node)
            if steps: self.visualizer.steps(next_node, visited)
    
        if solution: self.visualizer.solution(path)
        
        return path
    
    

    def greedy_best_first_search(self, steps: bool = False, solution: bool = False):
        
        """        
        Solve maze using Greedy best first search Algorithm.
    
        Parameters: Maze, setps, solution
        
    
    
        Returns: List[Tuple[int, int]] ->  List of tuples that represent the path from the start to the end of the maze.
                  each tuple contains the (x, y) coordinates of a position on the path.
                  If there is no solution, it returns an empty list.
                  
                  Optional -> show step by stept the algorithm 
                              show solution
        """
        
        
        graph       = self.maze.associated_graph
        open_set    = []     # Initialize the open set, which will store nodes to be explored
        previous    = {self.maze.start: None} # Initialize the dict, which will store the path
        distances   = {self.maze.start: 0}  # Initialize the score  dictionary, which will store the scores of nodes
        heuristic   = lambda a,b: abs(a[0] - b[0]) + abs(a[1] - b[1])
        heapq.heappush(open_set, (0, self.maze.start)) # Add the start node to the open set
        # We use a heap to get the lowest cost node efficiently


    
    
        while open_set:
            current = heapq.heappop(open_set)[1]  # Get the node with the lowest cost
            if steps: self.visualizer.steps(current, list(previous.keys()))
            if current == self.maze.end:  # We found the end
                break
    
            for neighbor in graph[current]:
                tentative_distance = distances[current] + heuristic(current, neighbor)
                
                # If the neighbor has not been explored before or if the tentative score is less than its current score
                if neighbor not in distances or tentative_distance < distances[neighbor]: 
                    previous[neighbor] = current
                    distances[neighbor] = tentative_distance # Update the neighbor's previous node and score
                    heapq.heappush(open_set, (distances[neighbor], neighbor)) # Add the neighbor to the open set
    
    
        if current == self.maze.end:  # If we found a path
            path = []
            while current is not None:  # Backtrack to find the path
                path.append(current)
                current = previous[current]
            path.reverse()  # Reverse to get path from start to end
            if solution: self.visualizer.solution(path)
            return path
    
        return []  # No path found
        
    
    