import pygame
import time
import lane as l
import config
from visualisation import Visualisation
from button_functions import *
from button import Button
import path as p

pygame.init()
win = pygame.display.set_mode(config.screen_size)
pygame.display.set_caption("Artificial City")
clock = pygame.time.Clock()

visualisation = Visualisation(win, config.lane_width, config.cell_size, config.c_lanes_coordinates,
                              config.z_lanes_coordinates, config.t_lanes_coordinates)

TRAM_LANES = {
    1: l.TramLane(number=1),
    2: l.TramLane(number=2)
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

PEDESTRIAN_LANES = {
    1: p.Path(number=1, length=20),
    2: p.Path(number=2, length=20),
    3: p.Path(number=3, length=16),
    4: p.Path(number=4, length=16),
    5: p.Path(number=5, length=12),
    6: p.Path(number=6, length=12),
    7: p.Path(number=7, length=12),
    8: p.Path(number=8, length=12),
    9: p.Path(number=9, length=12),
    10: p.Path(number=10, length=12),
    11: p.Path(number=11, length=12),
    12: p.Path(number=10, length=12)
}


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
            going_through = []
            for tuple_ in config.car_lanes_going_through[lane.number]['tram']:
                # the `*` operator unpacks a tuple
                going_through.append([TRAM_LANES[tuple_[0]], *tuple_[1:]])

            lane.update(going_through)

            if config.turns[lane.number] is not None:
                lane.turn_into(CAR_LANES[config.turns[lane.number][0]],
                               config.turns[lane.number][1:])

        for lane in TRAM_LANES.values():
            going_through = []
            for tuple_ in config.tram_lanes_going_through[lane.number]['car']:
                # the `*` operator unpacks a tuple
                going_through.append([CAR_LANES[tuple_[0]], *tuple_[1:]])

            lane.update(going_through)
    
        for lane in PEDESTRIAN_LANES.values():
            lane.update()
    
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

car_counter = 0
for lane in CAR_LANES.values():
    car_counter += lane.went_through

tram_counter = 0
for lane in TRAM_LANES.values():
    tram_counter += lane.went_through

pedestrian_counter = 0
for lane in PEDESTRIAN_LANES.values():
    pedestrian_counter += lane.numberOfPedestrians    
    
print("-------------------------------------------------------------")
print("Simulation duration: %.3f" % elapsed_time)
print('Number of cars that went through the intersection: ' + str(car_counter))
print("Average number of cars exiting the intersection per second: %.3f" % (car_counter / elapsed_time))
print("Number of trams that went through the intersection: " + str(tram_counter))
print("Average number of trams exiting the intersection per second: %.3f" % (tram_counter / elapsed_time))
print('Number of pedestrians that went through the intersection: ' + str(pedestrian_counter))
print("Average number of pedestrians exiting the intersection per second: %.3f" % (pedestrian_counter / elapsed_time))
