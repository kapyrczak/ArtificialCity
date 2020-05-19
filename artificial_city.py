import pygame
# import vehicle
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

CAR_LANES = {
    1: l.Lane(speed_limit=100, ticks_per_second=tps),
    2: l.Lane(speed_limit=20, ticks_per_second=tps)
}

PEDESTRIAN_LANES = {}

# main loop
running = True
while running:
    # pygame.time.delay(50)
    clock.tick(tps)

    for event in pygame.event.get():  # event - wszystko co zrobi użytkownik, np kliknięcie, nacisniecie klawisza itd
        if event.type == pygame.QUIT:
            running = False

    for lane in CAR_LANES.values():
        lane.update()

    # for lane in PEDESTRIAN_LANES.values():
    #     lane.update()

    visualisation.draw(CAR_LANES, PEDESTRIAN_LANES)
    pygame.display.update()

pygame.quit()