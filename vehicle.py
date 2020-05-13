#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 22:04:30 2020

@author: jakub

Nagel-Schreckenberg model simulation steps:
    1. Accelerate each car
    2. Check if movement with this velocity will be safe
    3. if not - slow down to a safe speed
    4. randomize - with set probability slow down by 1 step
    5. move
"""

import random
import copy

class Vehicle:
    """
    Distances measured in METERS
     1 m/s = 3.6 km/h, so
     50 km/h (city speed limit) ~= 14 m/s

    size:
         length - length of the vehicle
         width - width of the vehicle
         Both are set by default for a car
    velocity:
         max - max velocity
         v_change - rate of velocity change between ticks
         current - current/starting velocity
    safe_distance - distance to the vehicle ahead considered to be safe
        TODO: Calculating based on velocity?
    """
    def __init__(self, length=5, width=2,
                 v_max=14, v_change=1, current=[0, 0], direction="up",
                 safe_distance=1, slowdown_probability=0.3,
                 on_screen=[0, 0]):
        if direction == "up":
            current[1] *= -1
            v_change = [0, v_change*-1]
        elif direction == "down":
            v_change = [0, v_change]
        elif direction == "left":
            current[0] *= -1
            v_change = [v_change*-1, 0]
        elif direction == "right":
            v_change = [v_change, 0]

        self.safe_distance = safe_distance
        self.size = {"length": length, "width": width}
        self.max_velocity = v_max
        self.velocity = current
        self.velocity_change = v_change
        self.slowdown_probability = slowdown_probability
        self.on_screen = on_screen
        self.direction = direction
        self.moved = False

    def advance(self, grid, index_x, index_y):
        '''Advance the simulation by one step'''
        self.speed_up()

        vehicle_ahead = self.check_ahead(grid, index_x, index_y)
        if vehicle_ahead is not None:
            self.keep_safe(vehicle_ahead)

        self.randomize()
        new_grid = self.move(grid, index_x, index_y)
        self.moved = True
        return new_grid

    def speed_up(self):
        '''Accelerate'''
        if abs(self.velocity[0]) < self.max_velocity:
            self.velocity[0] += self.velocity_change[0]
        if abs(self.velocity[1]) < self.max_velocity:
            self.velocity[1] += self.velocity_change[1]

    def check_ahead(self, grid, index_x, index_y):
        '''Find closest car ahead'''
        if self.direction == "right" and index_y + 1 >= len(grid[index_x]):
            index_y -= len(grid[index_x])

        if self.direction == "down" and index_x + 1 >= len(grid[index_y]):
            index_x -= len(grid[index_x])

        if self.direction == "right" or self.direction == "left":
            ahead = self.check_horizontal(grid, index_x, index_y)
        elif self.direction == "up" or self.direction == "down":
            ahead = self.check_vertical(grid, index_x, index_y)
        return ahead

    def check_horizontal(self, grid, index_x, index_y):
        '''Check for a car ahead in x axis'''
        border = index_y + 1 + self.velocity[0]
        for i in range(index_y+1, border):
            if i >= len(grid[index_x]):
                j = i - len(grid[index_x])
            else:
                j = i
            if grid[index_x][j] != " ":
                return grid[index_x][j]
        return None

    def check_vertical(self, grid, index_x, index_y):
        '''Check for a car ahead in y axis'''
        border = index_x + 1 + self.velocity[1]
        for i in range(index_x+1, border):
            if i >= len(grid):
                j = i - len(grid)
            else:
                j = i
            if grid[j][index_y] != " ":
                return grid[j][index_y]
        return None

    def keep_safe(self, ahead):
        '''Slow down, if distance to vehicle ahead is not safe'''
        if self.direction == "right" or self.direction == "left":
            self.keep_safe_horizontal(ahead)
        elif self.direction == "up" or self.direction == "down":
            self.keep_safe_vertical(ahead)

    def keep_safe_horizontal(self, ahead):
        '''Decrease horizontal velocity if it is not safe'''
        dist = self.distance_horizontal(ahead)
        if dist < self.safe_distance + self.velocity[0]:
            self.velocity[0] = dist

    def distance_horizontal(self, vehicle):
        '''Return distance in x axis between
        self and vehicle passed as argument'''
        return abs(vehicle.on_screen[0] - self.on_screen[0])

    def keep_safe_vertical(self, ahead):
        '''Decrease vertical velocity if it is not safe'''
        dist = self.distance_vertical(ahead)
        if dist < self.safe_distance + self.velocity[1]:
            self.velocity[1] = dist

    def distance_vertical(self, vehicle):
        '''Return distance in t axis between
        self and vehicle passed as argument'''
        return abs(vehicle.on_screen[1] - self.on_screen[1])

    def randomize(self):
        '''with set probability slow down by 1 step'''
        rnd = random.random()
        if rnd < 1 - self.slowdown_probability:
            return

        if self.direction == "right" or self.direction == "left":
            self.slow_down(0)
        elif self.direction == "up" or self.direction == "down":
            self.slow_down(1)

    def slow_down(self, index):
        '''Decrease vehicle's velocity in a proper axis
            index=0 for horizontal slow down,
            index=1 for vertical slow down'''
        changed = self.velocity[index] - self.velocity_change[index]
        if self.velocity[index] * changed < 0:
            self.velocity[index] = 0
        else:
            self.velocity[index] = changed

    def move(self, grid, index_x, index_y):
        '''Move the vehicle and return a grid with it moved'''
        if self.direction == "right" or self.direction == "left":
            new_grid = self.move_horizontal(grid, index_x, index_y)
        elif self.direction == "up" or self.direction == "down":
            new_grid = self.move_vertical(grid, index_x, index_y)
        return new_grid

    def move_horizontal(self, grid, index_x, index_y):
        '''Move the vehicle in x axis'''
        new_grid = copy.copy(grid)
        new_index = index_y + self.velocity[0]
        if new_index >= len(grid[index_x]):
            new_index -= len(grid[index_x])
        new_grid[index_x][index_y], new_grid[index_x][new_index] = \
            new_grid[index_x][new_index], new_grid[index_x][index_y]
        return new_grid

    def move_vertical(self, grid, index_x, index_y):
        '''Move the vehicle in y axis'''
        return ''
