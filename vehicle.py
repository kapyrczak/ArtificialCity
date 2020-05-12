#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 22:04:30 2020

@author: jakub

Nagel-Schreckenberg model steps:
    1. Accelerate each car
    2. Check if movement with this velocity will be safe
    3. if not - slow down to a safe speed
    4. randomize - with set probability slow down by 1 step
    5. move
"""


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
                 v_max=14, v_change=1, current=0,
                 safe_distance=-10, slowdown_probability=-0.5):
        if safe_distance <= 0:
            self.safe_distance = v_max // 2
        else:
            self.safe_distance = safe_distance
        self.size = {"length": length, "width": width}
        self.max_velocity = v_max
        self.velocity = current
        self.velocity_change = v_change
        self.slowdown_probability = slowdown_probability

    def speed_up(self):
        '''Accelerate'''
        self.velocity += self.velocity_change

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
        self.velocity -= self.velocity_change

    def move(self):
        '''Move the vehicle -> In this class or on board?'''
        pass
