#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 10:26:05 2020
@author: jakub
"""

import random
import vehicle
import config

class Lane:
    """
    length - length of the lane
    vehicles - a list of vehicles on the lane
    spawn_probability - probability of a new car spawning on beginning of lane
    ticks_per_second - number of simulation ticks / second;
        used to adjust speed limit and vlocity changes of the vehicles
    """
    def __init__(self, length=100, spawn_probability=config.car_spawn_prob,
                 speed_limit=config.car_speed_limit, ticks_per_second=config.tps):
        self.length = length
        self.vehicles = []
        self.spawn_probability = spawn_probability
        self.speed_limit = speed_limit
        self.ticks_per_second = ticks_per_second
        self.v_max = 0
        self.starting_velocity = speed_limit
        self.lit = False

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

        for i in range(1, len(self.vehicles)):
            prev = self.vehicles[i-1]
            curr = self.vehicles[i]
            prev.calculate_safe_distance()
            prev.keep_safe(curr)


        for car in self.vehicles:
            car.move()


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

    def add_vehicle(self, length=4, width=2,
                    v_change=config.car_v_change,
                    slowdown_probability=config.car_slow_prob,
                    travelled=0, slow_duration=config.car_slow_duration):
        '''Add a new vehicle to the lane'''
        if len(self.vehicles) != 0 and \
            self.vehicles[0].travelled - self.vehicles[0].size["length"] <= 0:
            return

        new_vehicle = vehicle.Vehicle(
            length, width,
            self.speed_limit/self.ticks_per_second,
            v_change/self.ticks_per_second,
            self.starting_velocity/self.ticks_per_second,
            slowdown_probability,
            travelled-length, slow_duration, self.ticks_per_second/10)

        self.vehicles.insert(0, new_vehicle)

    def add_traffic_lights(self, distance):
        '''Add traffic lights that are `distance` away from the beggining of
        the lane'''
        if self.lit:
            return

        index = self.find_index(distance)
        traffic_lights = vehicle.Vehicle(1, 2, 0, 0, 0, 0, distance, 0, 0)
        self.vehicles.insert(index, traffic_lights)
        self.lit = True

    def find_index(self, distance):
        '''Find correct index for something that is `distance` away'''
        index = 0
        while index < len(self.vehicles) and \
            self.vehicles[index].travelled < distance:
            index += 1
        return index

    def delete_traffic_lights(self):
        '''Delete traffic lights from the lane'''
        if not self.lit:
            return

        for index, veh in enumerate(self.vehicles):
            if veh.max_velocity == 0:
                self.vehicles.pop(index)
        self.lit = False

    def printl(self):
        '''Print the lane on the console'''
        count = -1
        index = 0
        while count < self.length-1:
            count += 1
            if index >= len(self.vehicles):
                print("_", end='')
                continue

            if count < self.vehicles[index].travelled:
                print("_", end='')
            else:
                print("#", end='')
                index += 1
        print("|| Current max:" + str(self.v_max) + " | Limit:" + str(self.speed_limit))