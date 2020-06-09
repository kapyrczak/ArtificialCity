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

        self.went_through = 0

        if type(self) == Lane:
            self.__init_lights()

    def __init_lights(self):
        '''Initialize traffic lights for car lane'''
        if config.traffic_lights[self.number] is not None:
            self.yellow_lit = False
            self.red_lit = config.traffic_lights[self.number][3]

            if self.red_lit:
                self.red_lit = False # change it to false to allow adding the traffic lights
                self.add_traffic_lights(config.traffic_lights[self.number][0])

            self.green_light_elapsed = 0
            self.red_light_elapsed = 0
            self.yellow_lit = 0

    def update(self, through_lanes=None):
        '''Move every car on lane, destroy ones that are out of border,
        spawn new ones'''
        if through_lanes is not None:
            self.check_through_lanes(through_lanes)

        self.tick_vehicles()
        self.clean_up()
        self.spawn()
        self.update_lights()

        for car in self.vehicles:
            self.v_max = max(self.v_max, car.velocity)

    def check_through_lanes(self, through_lanes):
        '''For each car on lane check if other lane (ahead) is busy'''
        for car in self.vehicles:
            for through_lane in through_lanes:
                if car.travelled >= through_lane[-1] - 2 and \
                car.travelled <= through_lane[-1]:
                    if self.through_lane_busy(through_lane[:-1]):
                        car.max_velocity = 0
                    else:
                        car.max_velocity = self.speed_limit

    def through_lane_busy(self, through_lane_tuple):
        '''Check if a set part of another lane is occupied'''
        through_lane, through_travelled = through_lane_tuple
        through_index = through_lane.find_index(through_travelled) - 1

        return len(through_lane.vehicles) != 0 and \
        through_lane.vehicles[through_index].travelled <= through_travelled -1 and \
        through_lane.vehicles[through_index].travelled >= through_travelled - through_lane.vehicles[through_index].size["length"] - 2

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
            if self.vehicles[index].travelled > self.length + self.vehicles[index].size["length"]:
                self.vehicles.pop(index)
                index -= 1
                self.went_through += 1
            index += 1

    def spawn(self):
        '''With set probability spawn new car at the beginning of the lane'''
        if random.random() < self.spawn_probability:
            self.add_vehicle()
        self.vehicles.sort(key=lambda car: car.travelled)

    def add_vehicle(self, length=4, width=2,
                    v_change=config.car_v_change, current=-1,
                    travelled=0, slow_duration=config.car_slow_duration,
                    slowdown_probability=None):
        '''Add a new vehicle to the lane'''
        index = self.find_index(travelled)

        if slowdown_probability is None:
            slowdown_probability = config.car_slow_prob

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

    def update_lights(self):
        '''Update traffic lights on this lane'''
        if config.traffic_lights[self.number] is None:
            return

        self.yellow_lit = False
        if self.red_lit:
            self.red_light_elapsed += 1
        else:
            self.green_light_elapsed += 1
        self.change_lights()


    def change_lights(self):
        '''Change the traffic lights if suitable time has passed'''
        distance = config.traffic_lights[self.number][0]
        green_lit_time = config.traffic_lights[self.number][1] * self.ticks_per_second
        red_lit_time = config.traffic_lights[self.number][2] * self.ticks_per_second

        if (green_lit_time > self.green_light_elapsed >= green_lit_time - 75) or (red_lit_time > self.red_light_elapsed >= red_lit_time - 75):
            self.yellow_lit = True
        if self.green_light_elapsed >= green_lit_time:
            self.add_traffic_lights(distance)
        if self.red_light_elapsed >= red_lit_time:
            self.delete_traffic_lights()
        
        #elif self.red_light_elapsed >= red_lit_time - 75:
         #   self.yellow_lit = True


    def add_traffic_lights(self, distance):
        '''Add traffic lights that are `distance` away from the beggining of
        the lane'''

        if self.red_lit:
            return

        index = self.find_index(distance)
        traffic_lights = vehicle.Vehicle(1, 2, -10, -10, 0, 0, distance, 0, 0)
        self.vehicles.insert(index, traffic_lights)
        self.red_lit = True
        self.red_light_elapsed = 0

    def delete_traffic_lights(self):
        '''Delete traffic lights from the lane'''
        if not self.red_lit:
            return

        for index, veh in enumerate(self.vehicles):
            if veh.max_velocity < 0  and veh.velocity_change < 0:
                self.vehicles.pop(index)
        self.red_lit = False
        self.green_light_elapsed = 0

    def turn_into(self, other_lane, params):
        '''Turn into other lane at a place described in params'''
        turn_at = params[0]
        turn_untill = params[1]
        join_at = params[2]

        for index, car in enumerate(self.vehicles):
            if car.travelled >= turn_at and car.travelled <= turn_untill:
                self.transfer_car(car, index, other_lane, join_at)

    def transfer_car(self, car, index, other_lane, join_at):
        '''Transfer the car onto another lane'''
        velocity = car.velocity
        new_index = other_lane.find_index(join_at) - 1

        if len(other_lane.vehicles) == 0 or \
        other_lane.vehicles[new_index].travelled >= join_at + car.size["length"] or\
        other_lane.vehicles[new_index].travelled < join_at - 10:
            self.vehicles.pop(index)
            other_lane.add_vehicle(current=velocity, travelled=join_at)
            other_lane.vehicles.sort(key=lambda car: car.travelled)
        else:
            car.max_velocity = 0


class TramLane(Lane):
    '''Class for tram lanes - with changes in traffic lights (more than one set
    on lane) and spawning vehicles'''
    def __init__(self, number=1, length=100, spawn_interval=config.tram_spawn_interval,
                 speed_limit=config.tram_speed_limit, ticks_per_second=config.tps):
        Lane.__init__(self, number, length, 0,
                      speed_limit, ticks_per_second)

        self.spawn_interval = spawn_interval
        self.spawn_elapsed = 0

        self.__init_lights()

    def __init_lights(self):
        '''Initialize traffic lights on tram lane'''
        if config.tram_traffic_lights[self.number] is not None:
            self.yellow_lit = False
            self.lights_count = len(config.tram_traffic_lights[self.number][0])
            self.current_lights = 0
            self.red_lit = config.tram_traffic_lights[self.number][3]

            if self.red_lit:
                self.red_lit = False # change it to false to allow adding the traffic lights
                for dist in config.tram_traffic_lights[self.number][0]:
                    self.add_traffic_lights(dist)

            self.green_light_elapsed = 0
            self.red_light_elapsed = 0
            self.yellow_lit = 0

    def update_lights(self):
        '''Update traffic lights on this lane'''
        if config.tram_traffic_lights[self.number] is None:
            return

        self.yellow_lit = False
        if self.red_lit:
            self.red_light_elapsed += 1
        else:
            self.green_light_elapsed += 1
        self.change_lights()

    def change_lights(self):
        '''Change the traffic lights if suitable time has passed'''
        distance = config.tram_traffic_lights[self.number][0]
        green_lit_time = config.tram_traffic_lights[self.number][1] * self.ticks_per_second
        red_lit_time = config.tram_traffic_lights[self.number][2] * self.ticks_per_second

        if green_lit_time > self.green_light_elapsed >= green_lit_time - 75 or red_lit_time > self.red_light_elapsed >= red_lit_time - 75:
            self.yellow_lit = True
        if self.green_light_elapsed >= green_lit_time:
            for dist in distance:
                self.add_traffic_lights(dist)
        if self.red_light_elapsed >= red_lit_time:
            self.delete_traffic_lights()

    def add_traffic_lights(self, distance):
        '''Add traffic lights that are `distance` away from the beggining of
        the lane'''

        if self.red_lit and self.current_lights >= self.lights_count:
            return

        index = self.find_index(distance)
        
        if len(self.vehicles) != 0 and self.vehicles[index-1].travelled >= distance and \
        self.vehicles[index-1].travelled - self.vehicles[index-1].size['length'] <= distance:
            return
        
        tram_traffic_lights = vehicle.Vehicle(1, 2, -10, -10, 0, 0, distance, 0, 0)
        self.vehicles.insert(index, tram_traffic_lights)
        self.red_lit = True
        self.red_light_elapsed = 0
        self.current_lights += 1

    def delete_traffic_lights(self):
        '''Delete traffic lights from the lane'''

        if not self.red_lit:
            return

        index = 0
        while index < len(self.vehicles):
            veh = self.vehicles[index]
            if index + 1 > len(self.vehicles) and self.vehicles[index+1].travelled >= veh.travelled and \
            self.vehicles[index+1].travelled - self.vehicles[index+1].size['length'] <= veh.travelled:
                continue
            if veh.max_velocity < 0 and veh.velocity_change < 0:
                self.vehicles.pop(index)
                index -= 1
            index += 1

        self.red_lit = False
        self.green_light_elapsed = 0

    def spawn(self):
        '''After set interval spawn new tram at the beginning of the lane'''
        self.spawn_elapsed += 1
        if self.spawn_elapsed >= self.spawn_interval:
            self.add_vehicle()
            self.spawn_elapsed = 0
        self.vehicles.sort(key=lambda tram: tram.travelled)

    def add_vehicle(self, length=20, width=2,
                    v_change=config.tram_v_change, current=-1,
                    travelled=0, slow_duration=config.car_slow_duration,
                    slowdown_probability=config.tram_slow_prob):
        '''Add a tram to the lane'''
        Lane.add_vehicle(self, length, width, v_change, current, travelled,
                         slow_duration, slowdown_probability)
