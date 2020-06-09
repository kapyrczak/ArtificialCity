#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 20:24:25 2020

@author: jakub
"""

import config


def switch_simulation(flag):
    flag[0] = not flag[0]
    print("Simulation running: " + str(flag[0]))


def increase_fps():
    old = config.fps

    config.fps = min(config.fps + 5, 200)

    if old != config.fps:
        print("Current fps: " + str(config.fps))


def decrease_fps():
    old = config.fps

    config.fps = max(config.fps - 5, 5)

    if old != config.fps:
        print("Current fps: " + str(config.fps))


def increase_slowdown_prob(CAR_LANES):
    old = config.car_slow_prob

    config.car_slow_prob = min(round(config.car_slow_prob + 0.01, 2), 1)
    for lane in CAR_LANES.values():
        for car in lane.vehicles:
            if car.max_velocity >= 0 and car.velocity_change >= 0:
                car.slowdown_probability = config.car_slow_prob

    if old != config.car_slow_prob:
        print("Current car slowdown probability: " + str(config.car_slow_prob))


def decrease_slowdown_prob(CAR_LANES):
    old = config.car_slow_prob

    config.car_slow_prob = max(round(config.car_slow_prob - 0.01, 2), 0)
    for lane in CAR_LANES.values():
        for car in lane.vehicles:
            if car.max_velocity >= 0 and car.velocity_change >= 0:
                car.slowdown_probability = config.car_slow_prob

    if old != config.car_slow_prob:
        print("Current car slowdown probability: " + str(config.car_slow_prob))


def increase_green_light_time_horizontal():
    h_lane_numbers = [2, 3, 4]
    v_lane_numbers = [6, 7, 8, 9, 10, 11]
    old = config.traffic_lights[h_lane_numbers[0]][1]

    for lane_number in h_lane_numbers:
        config.traffic_lights[lane_number][1] += 0.5
    for lane_number in v_lane_numbers:
        config.traffic_lights[lane_number][2] += 0.5

    for lane in config.tram_traffic_lights.values():
        lane[1] += 0.5

    if old != config.traffic_lights[h_lane_numbers[0]][1]:
        print("Current green light time for HORIZONTAL lanes: %.2f s." % config.traffic_lights[h_lane_numbers[0]][1])


def decrease_green_light_time_horizontal():
    h_lane_numbers = [2, 3, 4]
    v_lane_numbers = [6, 7, 8, 9, 10, 11]
    old = config.traffic_lights[h_lane_numbers[0]][1]

    for lane_number in h_lane_numbers:
        config.traffic_lights[lane_number][1] = max(config.traffic_lights[lane_number][1] - 0.5, 0.5)
    for lane_number in v_lane_numbers:
        config.traffic_lights[lane_number][2] = max(config.traffic_lights[lane_number][2] - 0.5, 0.5)

    for lane in config.tram_traffic_lights.values():
        lane[1] = max(lane[1] - 0.5, 0.5)

    if old != config.traffic_lights[h_lane_numbers[0]][1]:
        print("Current green light time for HORIZONTAL lanes: %.2f s." % config.traffic_lights[h_lane_numbers[0]][1])


def increase_green_light_time_vertical():
    h_lane_numbers = [2, 3, 4]
    v_lane_numbers = [6, 7, 8, 9, 10, 11]
    old = config.traffic_lights[v_lane_numbers[0]][1]

    for lane_number in v_lane_numbers:
        config.traffic_lights[lane_number][1] += 0.5
    for lane_number in h_lane_numbers:
        config.traffic_lights[lane_number][2] += 0.5

    if old != config.traffic_lights[v_lane_numbers[0]][1]:
        print("Current green light time for VERTICAL lanes: %.2f s." % config.traffic_lights[v_lane_numbers[0]][1])


def decrease_green_light_time_vertical():
    h_lane_numbers = [2, 3, 4]
    v_lane_numbers = [6, 7, 8, 9, 10, 11]
    old = config.traffic_lights[v_lane_numbers[0]][1]

    for lane_number in v_lane_numbers:
        config.traffic_lights[lane_number][1] = max(config.traffic_lights[lane_number][1] - 0.5, 0.5)
    for lane_number in h_lane_numbers:
        config.traffic_lights[lane_number][2] = max(config.traffic_lights[lane_number][2] - 0.5, 0.5)

    if old != config.traffic_lights[v_lane_numbers[0]][1]:
        print("Current green light time for VERTICAL lanes: %.2f s." % config.traffic_lights[v_lane_numbers[0]][1])
