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
    size:
         length - length of the vehicle
         width - width of the vehicle
         Both are set by default for a car
    velocity:
         max - max velocity
         v_change - rate of velocity change between ticks
         current - current/starting velocity
    slowdown_probability - probability of the vehice slowing down in
        'randomization' phase
    travelled - distance from the beggining of the lane
    """

    def __init__(self, length=4, width=2,
                 v_max=14, v_change=1, current=0,
                 slowdown_probability=0.5,
                 travelled=0, slow_duration=2, safe_distance_coefficient=2):
        self.size = {"length": length, "width": width}
        self.max_velocity = v_max
        self.velocity = current
        self.velocity_change = v_change
        self.slowdown_probability = slowdown_probability
        self.travelled = travelled
        self.slow_duration = slow_duration
        self.slow_left = 0
        self.safe_distance = 1
        self.safe_dist_coeff = safe_distance_coefficient

    def speed_up(self):
        '''Accelerate'''
        if self.velocity < self.max_velocity:
            self.velocity += self.velocity_change
        self.velocity = min(self.velocity, self.max_velocity)
        # a guard for traffic lights as they are hacky -
        # vehicles with max velocity and velocity change < 0
        self.velocity = max(self.velocity, 0)

    def keep_safe(self, vehicle_ahead):
        '''Slow down to not crash into other vehicle'''
        ahead_travelled = vehicle_ahead.travelled - vehicle_ahead.size["length"]
        ahead_travelled -= self.safe_distance
        if self.travelled > ahead_travelled:
            diff = self.travelled - ahead_travelled
            new_velocity = self.velocity - diff
            self.velocity = max(0, new_velocity)

    def randomize(self):
        '''with set probability slow down by 1 step'''
        rnd = random.random()
        if self.slow_left > 0:
            self.slow_left -= 1
            self.slow_down()
        elif rnd <= self.slowdown_probability:
            self.slow_left -= self.slow_duration
            self.slow_down()

    def slow_down(self):
        '''Decrease vehicle's velocity'''
        changed = self.velocity - (self.velocity_change * 2)
        self.velocity = max(0, changed)

    def calculate_safe_distance(self):
        '''Calculate the safe distance to the preceding car'''
        dist = self.velocity * self.safe_dist_coeff
        self.safe_distance = max(1, dist)

    def move(self):
        '''Move the vehicle and return a grid with it moved'''
        self.travelled += self.velocity
