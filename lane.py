#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 10:26:05 2020

@author: jakub
"""

import random
import vehicle

class Lane:
    """
    length - length of the lane
    vehicles - a list of vehicles on the lane
    spawn_probability - probability of a new car spawning on beginning of lane
    ticks_per_second - number of simulation ticks / second;
        used to adjust speed limit and vlocity changes of the vehicles
    """
    def __init__(self, length=100, vehicles=[], spawn_probability=0.01,
                 speed_limit=14, ticks_per_second=30):
        self.length = length
        self.vehicles = vehicles
        self.spawn_probability = spawn_probability
        self.speed_limit = speed_limit
        self.ticks_per_second = ticks_per_second
        self.v_max = 0

    def update(self):
        '''Move every car on lane, destroy ones that are out of border,
        spawn new ones'''
        self.tick_vehicles()
        self.clean_up()
        self.spawn()
        
        v_m = 0
        for car in self.vehicles:
            self.v_max = max(v_m, car.velocity)

    def tick_vehicles(self):
        '''Move every car on lane'''
        for car in self.vehicles:
            car.speed_up()

        for car in self.vehicles:
            car.randomize()

        for car in self.vehicles:
            car.move()
            car.moved = True

    def clean_up(self):
        '''Delete cars that went too far'''
        index = 0
        while index < len(self.vehicles):
            if self.vehicles[index].travelled > self.length:
                self.vehicles.pop(index)
                index -= 1
            index += 1

    def spawn(self):
        '''With set probability spawn new car at the beginning of the lane'''
        if random.random() < self.spawn_probability:
            self.add_vehicle()

    def add_vehicle(self, length=5, width=2,
                    v_change=2, current=0,
                    slowdown_probability=0.05,
                    travelled=0):
        '''Add a new vehicle to the lane'''
        new_vehicle = vehicle.Vehicle(
            length, width,
            self.speed_limit/self.ticks_per_second,
            v_change/self.ticks_per_second, current,
            slowdown_probability,
            travelled)
        self.vehicles.insert(0, new_vehicle)


def _get_travelled(car):
    return car.travelled
