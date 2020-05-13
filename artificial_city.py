import pygame
import config
from visualisation import Visualisation

pygame.init()
win = pygame.display.set_mode(config.screen_size)
pygame.display.set_caption("Artificial City")
clock = pygame.time.Clock()


grid = [None] *100
grid[0] = 1
visualisation = Visualisation(win, config.lane_width, config.cell_size, grid)


def gridUpdate(grid, r):
    if r % 2 == 0:
        grid = [1] + grid
    else:
        grid = [None] + grid
    grid.pop()
    return grid
r = 0
# main loop
running = True
while running:
    # pygame.time.delay(50)
    clock.tick(10)

    for event in pygame.event.get():  # event - wszystko co zrobi użytkownik, np kliknięcie, nacisniecie klawisza itd
        if event.type == pygame.QUIT:
            running = False

    #visualisation.draw()
    r = r + 1
    visualisation.drawLane(grid, 100)
    for i in range(len(grid)):
        if grid[i] == 1:
            visualisation.drawCar(i*config.cell_size*4)
    grid = gridUpdate(grid, r)
    pygame.display.update()

pygame.quit()
