#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 11:36:27 2023

@author: sebastianpedraza
"""

from Maze import *
from MazeSolver import *
from MazeVisualizer import *
import seaborn as sns
from tqdm import tqdm
import pandas as pd
import time


#  Show benchamark plot of time execution of Algorithms
def benchmark_algorithms():
    sizes       = range(5,111, 2)
    algorithms = [MazeSolver.bfs, MazeSolver.dfs, MazeSolver.dijkstra, MazeSolver.a_star, MazeSolver.bidirectional,MazeSolver.random, MazeSolver.greedy_best_first_search]
    times       = {alg.__name__: [] for alg in algorithms}
    sns.set(style="dark", palette="pastel")

    for size in tqdm(sizes, desc="Testing", unit="size"):
        for algorithm in algorithms:
            def time_execution(algorithm, size):
                maze       = Maze.backtrack_generator(size, size)
                solver     = MazeSolver(maze, MazeVisualizer(maze))
                start_time = time.perf_counter()
                algorithm(solver, False, False)
                return time.perf_counter() - start_time
            total_time = sum(time_execution(algorithm, size) for _ in range(10)) / 10
            times[algorithm.__name__].append(total_time)

    df              = pd.DataFrame(times)
    df["Maze Size"] = sizes

    plt.figure(figsize=(12, 8))
    sns.lineplot(data=df.melt(id_vars="Maze Size"), x="Maze Size", y="value", hue="variable")

    plt.xlabel('Maze Size', fontsize=14)
    plt.ylabel('Average Time (s)', fontsize=14)
    plt.title('Average Execution Time vs Maze Size', fontsize=16)
    plt.legend(title="Algorithm", title_fontsize='13', fontsize='12')
    plt.show()



# Show all Algorithms step by step
def show_algorithms():
    maze = Maze.backtrack_generator(41,41)
    algorithms = [MazeSolver.bfs, MazeSolver.dfs, MazeSolver.dijkstra, MazeSolver.a_star, MazeSolver.bidirectional,MazeSolver.random, MazeSolver.greedy_best_first_search]
    for algorithm in algorithms:
        MazeVisualizer(maze).visualize()
        input()
        print(str(algorithm))
        solver = MazeSolver(maze, MazeVisualizer(maze))
        try:
            algorithm(solver, True, True)
        except KeyboardInterrupt:
            print("Interrupted, moving to next algorithm")
            continue
        input()



def solver():
    '''
    >> Usage:
        maze = Maze.backtrack_generator(n,m)    # Create a maze nXm using backtrack
        mazeVisualizer(maze).visualize()        # Show maze
        mazeVisualizer(maze).graph()            # Show associated graph

        algorithms: bfs, dfs, dijkstra, a_star, bidirectional, random, greedy_best_first_search
        mazeSolver(maze, visualizer(maze)).algorithm(steps: bool, solution:bool)

    '''

    maze = Maze.empty_maze(21,21)
    MazeVisualizer(maze).visualize()
    input()
    MazeSolver(maze, MazeVisualizer(maze)).random(True, True)
    input()





if __name__ == '__main__':
    solver()
    show_algorithms()

