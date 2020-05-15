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
    """
    def __init__(self, length=100, vehicles=[], spawn_probability=0.15):
        self.length = length
        self.vehicles = vehicles
        self.spawn_probability = spawn_probability

    def update(self):
        '''Move every car on lane, destroy ones that are out of border,
        spawn new ones'''
        self.tick_vehicles()
        self.clean_up()
        self.spawn()

    def tick_vehicles(self):
        '''Move every car on lane'''
        for car in self.vehicles:
            if car.moved:
                continue
            car.speed_up()
        
        for index, car in enumerate(self.vehicles):
            if car.moved:
                continue
            if index + 1 < len(self.vehicles):
                ahead = self.vehicles[index + 1]
                car.keep_safe(ahead)
        
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
                    v_max=14, v_change=1, current=0,
                    safe_distance=1, slowdown_probability=0.3,
                    travelled=0):
        '''Add a new vehicle to the lane'''
        self.vehicles.insert(0, vehicle.Vehicle(
            length, width,
            v_max, v_change, current,
            safe_distance, slowdown_probability,
            travelled))
        self.vehicles.sort(key=_get_travelled)


def _get_travelled(car):
    return car.travlled
