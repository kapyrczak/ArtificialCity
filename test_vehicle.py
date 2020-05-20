#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 09:28:19 2020

@author: jakub
"""

import lane as l
import time

LANE_LEN = 100

def print_lanes(lanes):
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    for lane in lanes.values():
        lane.printl()
    print("-"*LANE_LEN + "--")

if __name__ == "__main__":
    LANES = {
        1: l.Lane(LANE_LEN, speed_limit=3),
        2: l.Lane(LANE_LEN, speed_limit=4),
        3: l.Lane(LANE_LEN, speed_limit=5),
        4: l.Lane(LANE_LEN, speed_limit=6),
        5: l.Lane(LANE_LEN, speed_limit=7)
        }

    LANES[1].add_vehicle(travelled=0)

    while True:
        print_lanes(LANES)
    
        for lane in LANES.values():
            lane.update()
        time.sleep(0.15)
