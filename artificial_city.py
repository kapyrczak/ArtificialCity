import pygame
import lane as l
import config
from visualisation import Visualisation

pygame.init()
win = pygame.display.set_mode(config.screen_size)
pygame.display.set_caption("Artificial City")
clock = pygame.time.Clock()

visualisation = Visualisation(win, config.lane_width, config.cell_size, config.c_lanes_coordinates,
                              config.z_lanes_coordinates, config.t_lanes_coordinates)


TRAM_LANES = {
    1: l.Lane(),
    2: l.Lane()
}

CAR_LANES = {
    1: l.Lane(number=1, length=25, spawn_probability=0),
    2: l.Lane(number=2, length=35),
    3: l.Lane(number=3, length=30),
    4: l.Lane(number=4, length=30),
    5: l.Lane(number=5, spawn_probability=0),
    6: l.Lane(number=6),
    7: l.Lane(number=7),
    8: l.Lane(number=8),
    9: l.Lane(number=9),
    10: l.Lane(number=10),
    11: l.Lane(number=11)
}

PEDESTRIAN_LANES = {}

lights_test = CAR_LANES[6]

# main loop
running = True
while running:
    # pygame.time.delay(50)
    clock.tick(config.tps)

    for event in pygame.event.get():  # event - wszystko co zrobi użytkownik, np kliknięcie, nacisniecie klawisza itd
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if lights_test.lit:
                    CAR_LANES[11].delete_traffic_lights()
                    lights_test.delete_traffic_lights()
                else:
                    # TODO: specify trafic lights distance in config.py
                    # (for each lane)
                    CAR_LANES[11].add_traffic_lights(45)
                    lights_test.add_traffic_lights(50)

    for lane in CAR_LANES.values():
        lane.update()
        if config.turns[lane.number] is not None:
            lane.turn_into(CAR_LANES[config.turns[lane.number][0]],
                           config.turns[lane.number][1:])

    # for lane in PEDESTRIAN_LANES.values():
    #     lane.update()

    visualisation.draw(CAR_LANES, PEDESTRIAN_LANES, TRAM_LANES)
    pygame.display.update()

pygame.quit()
