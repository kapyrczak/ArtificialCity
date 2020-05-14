#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 09:28:19 2020

@author: jakub
"""

import vehicle
import lane as l

if __name__ == "__main__":
    LANES = {
        1: l.Lane(vehicles=[vehicle.Vehicle(), vehicle.Vehicle(travelled=4)]),
        2: l.Lane(),
        3: l.Lane(),
        4: l.Lane()
        }

    for lane in LANES.values():
        lane.update()
