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
#    1: l.Lane(),
#    2: l.Lane(),
#    3: l.Lane(),
#    4: l.Lane(),
#    5: l.Lane(),
    6: l.Lane(),
    7: l.Lane(),
    8: l.Lane(),
    9: l.Lane(),
    10: l.Lane(),
    11: l.Lane(),
}

lights_test = CAR_LANES[6]

PEDESTRIAN_LANES = {}

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
                    lights_test.delete_traffic_lights()
                else:
                    # TODO: specify trafic lights distance in config.py
                    # (for each lane)
                    lights_test.add_traffic_lights(50)

    for lane in CAR_LANES.values():
        lane.update()

    # for lane in PEDESTRIAN_LANES.values():
    #     lane.update()

    visualisation.draw(CAR_LANES, PEDESTRIAN_LANES, TRAM_LANES)
    pygame.display.update()

pygame.quit()
