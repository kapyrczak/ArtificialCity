import pygame
import time
import lane as l
import config
from visualisation import Visualisation
from button_functions import *
from button import Button

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

black = (0, 0, 0)
blue = (152, 203, 222, 255)
white = (255, 255, 255)

# a workaround so the value referenced here can be changed in a function elsewhere
running = [False]

on = True

on_off = Button("URUCHOM/ZATRZYMAJ", 0, 0, 200, 50, white, blue, lambda: switch_simulation(running))
faster = Button("PRZYŚPIESZ SYMULACJĘ", config.width / 2 - 100, 4 * config.cell_size, 200, 50, white, blue, increase_fps)
slower = Button("SPOWOLNIJ SYMULACJĘ", config.width / 2 - 100, 14 * config.cell_size, 200, 50, white, blue, decrease_fps)
longer_h = Button("WYDŁUŻ POZIOME ŚWIATŁA", config.width / 2 - 100, 24 * config.cell_size, 200, 50, white, blue, increase_green_light_time_horizontal)
shorter_h = Button("SKRÓĆ POZIOME ŚWIATŁA", config.width / 2 - 100, 34 * config.cell_size, 200, 50, white, blue, decrease_green_light_time_horizontal)
longer_v = Button("WYDŁUŻ PIONOWE ŚWIATŁA", config.width / 2 - 100, 60 * config.cell_size, 200, 50, white, blue, increase_green_light_time_vertical)
shorter_v = Button("SKRÓĆ PIONOWE ŚWIATŁA", config.width / 2 - 100, 70 * config.cell_size, 200, 50, white, blue, decrease_green_light_time_vertical)
prob_up = Button("ZWIĘKSZ PRAW. ZWALNIANIA", config.width / 2 - 100, 80 * config.cell_size, 200, 50, white, blue, lambda: increase_slowdown_prob(CAR_LANES))
prob_down = Button("ZMNIEJSZ PRAW. ZWALNIANIA", config.width / 2 - 100, 90 * config.cell_size, 200, 50, white, blue, lambda: decrease_slowdown_prob(CAR_LANES))


start_time = time.time()

# main loop
while on:
    # pygame.time.delay(50)
    clock.tick(config.fps)

    for event in pygame.event.get():  # event - wszystko co zrobi użytkownik, np kliknięcie, nacisniecie klawisza itd
        if event.type == pygame.QUIT:
            on = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running[0] = not running[0]
                print("Simulation running: " + str(running[0]))

    if running[0]:
        for lane in CAR_LANES.values():
            lane.update()
            if config.turns[lane.number] is not None:
                lane.turn_into(CAR_LANES[config.turns[lane.number][0]],
                               config.turns[lane.number][1:])
    
        # for lane in PEDESTRIAN_LANES.values():
        #     lane.update()
    
    visualisation.draw(CAR_LANES, PEDESTRIAN_LANES, TRAM_LANES)

    on_off.draw(win)
    faster.draw(win)
    slower.draw(win)
    longer_h.draw(win)
    shorter_h.draw(win)
    longer_v.draw(win)
    shorter_v.draw(win)
    prob_up.draw(win)
    prob_down.draw(win)

    pygame.display.update()

pygame.quit()

end_time = time.time()
elapsed_time = end_time - start_time

counter = 0
for lane in CAR_LANES.values():
    counter += lane.went_through
print("-------------------------------------------------------------")
print('Number of cars that went through the intersection: ' + str(counter))
print("Simulation duration: %.3f" % elapsed_time)
print("Average number of cars exiting the intersection per second: %.3f" % (counter / elapsed_time))