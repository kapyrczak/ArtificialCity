#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 09:28:19 2020

@author: jakub
"""

import vehicle
import time

if __name__ == "__main__":
    grid = []
    grid_len = 30
    interval = 0.3
    
    # create random number of vehicles on the road
    for i in range(grid_len):
        if vehicle.random.random() < 0.15:
            grid.append(vehicle.Vehicle(v_max=2,
                                        direction="right", on_screen=[i,0]))
        else:
            grid.append(" ")
        
    # print the road
    for cell in grid:
        if cell == " ":
            print(" ", end="")
        else:
            print("#", end="")
            cell.moved = False
            v = cell.velocity[0]
    print("\n"+("-"*grid_len))
    time.sleep(interval)
    
    for i in range(len(grid)*2):
        for index in range(len(grid)):
            if grid[index] != " " and (not grid[index].moved):
                grid = grid[index].advance(grid, index)
        # print the road
        print("\n\n\n")
        
        v = 0
        for cell in grid:
            if cell == " ":
                print(" ", end="")
            else:
                print("#", end="")
                cell.moved = False
                v = max(v, cell.velocity[0])
        print("||"+str(v))
        time.sleep(interval)
