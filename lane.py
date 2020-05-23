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
    def __init__(self, number=1, length=100, spawn_probability=config.car_spawn_prob,
                 speed_limit=config.car_speed_limit, ticks_per_second=config.tps):
        self.number = number
        self.length = length
        self.vehicles = []
        self.spawn_probability = spawn_probability
        self.speed_limit = speed_limit
        self.ticks_per_second = ticks_per_second
        self.v_max = 0
        self.starting_velocity = speed_limit
        self.lit = False
        self.went_through = 0

    def update(self):
        '''Move every car on lane, destroy ones that are out of border,
        spawn new ones'''
        self.tick_vehicles()
        self.clean_up()
        self.spawn()

        self.vehicles.sort(key=lambda car: car.travelled)

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
                self.went_through += 1
            index += 1

    def spawn(self):
        '''With set probability spawn new car at the beginning of the lane'''
        if random.random() < self.spawn_probability:
            self.add_vehicle()

    def add_vehicle(self, length=4, width=2,
                    v_change=config.car_v_change, current=-1,
                    slowdown_probability=config.car_slow_prob,
                    travelled=0, slow_duration=config.car_slow_duration):
        '''Add a new vehicle to the lane'''
        index = self.find_index(travelled)

        if len(self.vehicles) != 0 and \
            self.vehicles[index-1].travelled - self.vehicles[index-1].size["length"] <= \
                -self.vehicles[index-1].size["length"]:
            return

        if current < 0:
            current = self.starting_velocity / self.ticks_per_second

        new_vehicle = vehicle.Vehicle(
            length, width,
            self.speed_limit/self.ticks_per_second,
            v_change/self.ticks_per_second,
            current,
            slowdown_probability,
            travelled-length, slow_duration, self.ticks_per_second/10)

        self.vehicles.insert(index, new_vehicle)

    def find_index(self, distance):
        '''Find correct index for something that is `distance` away'''
        index = 0
        while index < len(self.vehicles) and \
            self.vehicles[index].travelled < distance:
            index += 1
        return index

    def add_traffic_lights(self, distance):
        '''Add traffic lights that are `distance` away from the beggining of
        the lane'''
        if self.lit:
            return

        index = self.find_index(distance)
        traffic_lights = vehicle.Vehicle(1, 4, 0, 0, 0, 0, distance, 0, 0)
        self.vehicles.insert(index, traffic_lights)
        self.lit = True

    def delete_traffic_lights(self):
        '''Delete traffic lights from the lane'''
        if not self.lit:
            return

        for index, veh in enumerate(self.vehicles):
            if veh.max_velocity == 0:
                self.vehicles.pop(index)
        self.lit = False

    def turn_into(self, other_lane, params):
        '''turn cars from the lane to other lane (it's a intersection ater all'''
        if other_lane is None:
            return

        for index, car in enumerate(self.vehicles):
            if car.travelled >= params[0] and car.travelled <= params[1]:
                # get index for car on lane it will turn into
                i = other_lane.find_index(params[2])

                # if there is a turn on the lane car will turn into get where
                # it ends
                dist = 0
                if self.__turn_exists_at(other_lane):
                    dist = config.turns[other_lane.number][2]
                
                # check if the car can turn: there are no other cars on the lane
                # OR there is space on the lane :
                #   all cars are further than the intersection
                #   OR all cars are closer than the intesection
                if len(other_lane.vehicles) == 0 or \
                other_lane.vehicles[i-1].travelled >= params[2] + car.size["length"] or \
                other_lane.vehicles[i-1].travelled < dist:
                    speed = car.velocity
                    self.vehicles.pop(index)
                    other_lane.add_vehicle(current=speed, travelled=params[2])
                else:
                    car.max_velocity = 0

    def __turn_exists_at(self, other_lane):
        return config.turns[other_lane.number] is not None
