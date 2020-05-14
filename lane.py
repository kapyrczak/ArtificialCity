#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 10:26:05 2020

@author: jakub
"""

import random
import vehicle

class Lane:
    def __init__(self, length=100, vehicles=[], spawn_probability=0.15):
        self.length = length
        self.vehicles = vehicles
        self.spawn_probability = spawn_probability

    def update(self):
        self.tick_vehicles()
        self.clean_up()
        self.spawn()

    def tick_vehicles(self):
        for index, car in enumerate(self.vehicles):
            if index + 1 >= len(self.vehicles):
                ahead = None
            else:
                ahead = self.vehicles[index + 1]
            car.advance(ahead)

    def clean_up(self):
        index = 0
        while index < len(self.vehicles):
            if self.vehicles[index].travelled > self.length:
                self.vehicles.pop(index)
                index -= 1
            index += 1

    def spawn(self):
        if random.random() < self.spawn_probability:
            car = vehicle.Vehicle()
            self.vehicles.insert(0, car)
