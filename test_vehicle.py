#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 09:28:19 2020

@author: jakub
"""

import time
import vehicle

grid_size = [50, 4]
lane_index = 0
interval = 0.1
# "right", "left", "up" or "down"
# "up" and "down" require a 2d grid
direc = "left"
spawn_prob = 0.1


def main():
    grid = generate_horizontal(lane_index, direc)
    while True:
        print("\n\n\n\n\n\n\n\n\n\n")
        print_grid(grid, direc)
        time.sleep(interval)
        grid = tick(grid, lane_index, direc)

def generate_horizontal(lane_on, direc):
    grid = []
    for i in range(grid_size[1]):
        grid.append([])
        for j in range(grid_size[0]):
            if i == lane_on and vehicle.random.random() < spawn_prob:
                grid[lane_on].append(vehicle.Vehicle(v_max=2, direction=direc,
                                                     on_screen=[lane_on, j]))
            else:
                grid[i].append(" ")
    return grid

def generate_vertical(lane_on, direc):
    grid = []
    for i in range(grid_size[1]):
        grid.append([])
        for j in range(grid_size[0]):
            if j == lane_on and vehicle.random.random() < spawn_prob:
                grid[i].append(vehicle.Vehicle(v_max=2, direction=direc,
                                               on_screen=[i, lane_on]))
            else:
                grid[i].append(" ")
    return grid

def print_grid(grid, direction):
    for i in range(grid_size[1]):
        v = 0
        for cell in grid[i]:
            if cell == " ":
                print(" ", end="")
            else:
                print("#", end="")
                cell.moved = False
                if direction == "right":
                    v = max(v, cell.velocity[0])
                elif direction == "left":
                    v = min(v, cell.velocity[0])
        print("||"+str(v))
    print("\n"+("-"*grid_size[0]))

def tick(grid, lane_on, direction):
    if direction == "left" or direction == "right":
        new_grid = tick_horizontal(grid, lane_on)
    return new_grid

def tick_horizontal(grid, lane_on):
    new_grid = vehicle.copy.copy(grid)
    for index in range(len(new_grid[lane_on])):
        if new_grid[lane_on][index] != " " and (not new_grid[lane_on][index].moved):
            new_grid = new_grid[lane_on][index].advance(new_grid, lane_on, index)
    return new_grid

if __name__ == "__main__":
    main()
#    while True:
#        for index in range(len(grid[0])):
#            if grid[0][index] != " " and (not grid[0][index].moved):
#                grid = grid[0][index].advance(grid, 0, index)
#        # print the road
#        print("\n\n\n\n\n\n\n\n\n\n")
#
#        v = 0
#        for cell in grid[0]:
#            if cell == " ":
#                print(" ", end="")
#            else:
#                print("#", end="")
#                cell.moved = False
#                if direc == "right":
#                    v = max(v, cell.velocity[0])
#                elif direc == "left":
#                    v = min(v, cell.velocity[0])
#        print("||"+str(v))
#        time.sleep(interval)
