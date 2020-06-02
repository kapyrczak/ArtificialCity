import pygame
import time
import lane as l
import config
from visualisation import Visualisation
from button_functions import *

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


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def button(msg, x, y, width, height, color, onhover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(win, onhover_color, (x, y, width, height))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(win, color, (x, y, width, height))

    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (width / 2)), (y + (height / 2)))
    win.blit(textSurf, textRect)

start_time = time.time()

# main loop
running = True
while running:
    # pygame.time.delay(50)
    clock.tick(config.fps)

    for event in pygame.event.get():  # event - wszystko co zrobi użytkownik, np kliknięcie, nacisniecie klawisza itd
        if event.type == pygame.QUIT:
            running = False

    for lane in CAR_LANES.values():
        lane.update()
        if config.turns[lane.number] is not None:
            lane.turn_into(CAR_LANES[config.turns[lane.number][0]],
                           config.turns[lane.number][1:])

    # for lane in PEDESTRIAN_LANES.values():
    #     lane.update()

    visualisation.draw(CAR_LANES, PEDESTRIAN_LANES, TRAM_LANES)
    button("PRZYŚPIESZ SYMULACJĘ", config.width / 2 - 100, 4 * config.cell_size, 200, 50, white, blue, increase_fps)
    button("SPOWOLNIJ SYMULACJĘ", config.width / 2 - 100, 14 * config.cell_size, 200, 50, white, blue, decrease_fps)
    button("WYDŁUŻ POZIOME ŚWIATŁA", config.width / 2 - 100, 24 * config.cell_size, 200, 50, white, blue, increase_green_light_time_horizontal)
    button("SKRÓĆ POZIOME ŚWIATŁA", config.width / 2 - 100, 34 * config.cell_size, 200, 50, white, blue, decrease_green_light_time_horizontal)
    button("WYDŁUŻ PIONOWE ŚWIATŁA", config.width / 2 - 100, 60 * config.cell_size, 200, 50, white, blue, increase_green_light_time_vertical)
    button("SKRÓĆ PIONOWE ŚWIATŁA", config.width / 2 - 100, 70 * config.cell_size, 200, 50, white, blue, decrease_green_light_time_vertical)
    button("ZWIĘKSZ PRAW. ZWALNIANIA", config.width / 2 - 100, 80 * config.cell_size, 200, 50, white, blue, lambda: increase_slowdown_prob(CAR_LANES))
    button("ZMNIEJSZ PRAW. ZWALNIANIA", config.width / 2 - 100, 90 * config.cell_size, 200, 50, white, blue, lambda: decrease_slowdown_prob(CAR_LANES))

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