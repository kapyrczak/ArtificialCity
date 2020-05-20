import pygame
import vehicle
import lane as l
import config
from visualisation import Visualisation

pygame.init()
win = pygame.display.set_mode(config.screen_size)
pygame.display.set_caption("Artificial City")
clock = pygame.time.Clock()

visualisation = Visualisation(win, config.lane_width, config.cell_size, config.c_lanes_coordinates,
                              config.z_lanes_coordinates, config.t_lanes_coordinates)

tps = 50

TRAM_LANES = {
    1: l.Lane(speed_limit=100, ticks_per_second=tps),
    2: l.Lane(speed_limit=20, ticks_per_second=tps)
}

car = vehicle.Vehicle()
myvehicles = [car]
CAR_LANES = {
    1: l.Lane(speed_limit=100, ticks_per_second=tps, vehicles=myvehicles),
    2: l.Lane(speed_limit=100, ticks_per_second=tps, vehicles=myvehicles),
    3: l.Lane(speed_limit=100, ticks_per_second=tps, vehicles=myvehicles),
    4: l.Lane(speed_limit=100, ticks_per_second=tps, vehicles=myvehicles),
    5: l.Lane(speed_limit=100, ticks_per_second=tps, vehicles=myvehicles),
    6: l.Lane(speed_limit=100, ticks_per_second=tps, vehicles=myvehicles),
    7: l.Lane(speed_limit=100, ticks_per_second=tps, vehicles=myvehicles),
    8: l.Lane(speed_limit=100, ticks_per_second=tps, vehicles=myvehicles),
    9: l.Lane(speed_limit=100, ticks_per_second=tps, vehicles=myvehicles),
    10: l.Lane(speed_limit=100, ticks_per_second=tps, vehicles=myvehicles),
    11: l.Lane(speed_limit=100, ticks_per_second=tps, vehicles=myvehicles),
}

PEDESTRIAN_LANES = {}

# main loop
running = True
while running:
    # pygame.time.delay(50)
    clock.tick(10)

    for event in pygame.event.get():  # event - wszystko co zrobi użytkownik, np kliknięcie, nacisniecie klawisza itd
        if event.type == pygame.QUIT:
            running = False

    for lane in TRAM_LANES.values():
        lane.update()
    for lane in CAR_LANES.values():
        lane.update()

    # for lane in PEDESTRIAN_LANES.values():
    #     lane.update()

    visualisation.draw(CAR_LANES, PEDESTRIAN_LANES, TRAM_LANES)
    pygame.display.update()

pygame.quit()
