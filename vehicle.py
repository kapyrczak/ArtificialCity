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
                 safe_distance=1, slowdown_probability=0.5):
        if direction == "up":
            v_max *= -1
            current[1] *= -1
            v_change = [0, v_change*-1]
        elif direction == "left":
            v_max *= -1
            current[0] *= -1
            v_change = [v_change*-1, 0]

        self.safe_distance = safe_distance
        self.size = {"length": length, "width": width}
        self.max_velocity = v_max
        self.velocity = {"x": current[0], "y": current[1]}
        self.velocity_change = v_change
        self.slowdown_probability = slowdown_probability
        self.on_screen = [0, 0]

    def speed_up(self):
        '''Accelerate'''
        self.velocity[0] += self.velocity_change[0]
        self.velocity[1] += self.velocity_change[1]

    def keep_safe(self, ahead):
        '''Slow down, if distance to vehicle ahead is not safe'''
        dist = self.distance(ahead)
        if dist > self.safe_distance:
            self.velocity = dist

    def distance(self, vehicle):
        '''Return distance between self and vehicle passed as argument'''
        return 0

    def randomize(self):
        '''with set probability slow down by 1 step'''
        rnd = random.random()
        if rnd < 1 - self.slowdown_probability:
            return

        changed = self.velocity - self.velocity_change
        if self.velocity * changed < 0:
            self.velocity = 0
        else:
            self.velocity = changed

    def move(self):
        '''Move the vehicle -> In this class or on board?'''
        pass
    
    def advance(self, vehicle_ahead):
        '''Advance the simulation by one step'''
        self.speed_up()
        self.keep_safe(vehicle_ahead)
        self.randomize()
        self.move()
