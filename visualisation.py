import pygame

# colors
blue, darkblue = (51, 153, 255, 150), (0, 77, 128)
white, black = (255, 255, 255), (0, 0, 0)
grey, darkgrey = (153, 153, 153), (77, 77, 77)
red = (255, 0, 0, 150)


class Visualisation():
    def __init__(self, win, lane, cell_size, grid):
        self.win = win
        self.width, self.height = win.get_width(), win.get_height()
        self.lane = lane
        self.px = cell_size
        self.grid = grid

    def drawLane(self, grid, grid_len):
        car_lane_vertical = pygame.Surface(( self.width,self.lane), pygame.SRCALPHA)
        car_lane_vertical.fill(grey)
        self.win.blit(car_lane_vertical, (0,self.height/2 - self.lane/2))

    def drawCar(self, x):
        car = pygame.Surface((4*self.px, 2*self.px), pygame.SRCALPHA)
        car.fill(red)
        self.win.blit(car, (x, self.height/2 - self.px))

    def draw(self):
        self.win.fill(white)
        self.__drawIntersection(self.win, self.lane, self.px, self.width, self.height)

    def drawGrid(self):
        for x in range(self.width // self.px):
            for y in range(self.width // self.px):
                rect = pygame.Rect(x * self.px, y * self.px, self.px, self.px)
                pygame.draw.rect(self.win, black, rect, 1)


    def __drawIntersection(self, win, lane, px, win_x, win_y):

        # car
        car_lane_vertical = pygame.Surface((lane, win_y), pygame.SRCALPHA)
        car_lane_vertical.fill(grey)
        car_lane_horizontal = pygame.Surface(((win_x - lane * 6 - 26 * px) / 2, lane), pygame.SRCALPHA)
        car_lane_horizontal.fill(grey)

        # horizontal
        for i in range(0, 4):
            win.blit(car_lane_horizontal, (0, (win_y - lane * 4) / 2 + i * lane))
            win.blit(car_lane_horizontal, (
                (win_x - lane * 6 - 26 * px) / 2 + 26 * px + 6 * lane, (win_y - lane * 4) / 2 + i * lane))

        win.blit(car_lane_horizontal, (0, (win_y - lane * 4) / 2 + 4 * lane))

        # vertical
        for i in range(0, 3):
            win.blit(car_lane_vertical, ((win_x - lane * 6 - 26 * px) / 2 + i * lane, 0))
            win.blit(car_lane_vertical, ((win_x - lane * 6 - 26 * px) / 2 + 26 * px + (3 + i) * lane, 0))

        # tram
        tramlanes = pygame.Surface((win_x, lane), pygame.SRCALPHA)
        tramlanes.fill(blue)
        for i in range(0, 2):
            win.blit(tramlanes, (0, (win_y - lane * 4) / 2 + lane + i * lane))

        # pedestrians
        zebra_vlong = pygame.Surface((lane * 0.5, lane * 5), pygame.SRCALPHA)
        zebra_vshort = pygame.Surface((lane * 0.5, lane * 4), pygame.SRCALPHA)
        zebra_h = pygame.Surface((lane * 3, lane * 0.5), pygame.SRCALPHA)

        zebra_vlong.fill(red)
        zebra_vshort.fill(red)
        zebra_h.fill(red)

        win.blit(zebra_vlong, ((win_x - lane * 6 - 26 * px) / 2 - lane, (win_y - lane * 4) / 2))
        win.blit(zebra_vshort, (
            (win_x - lane * 6 - 26 * px) / 2 + 6 * lane + 26 * px + lane * 0.5, (win_y - lane * 4) / 2))
        win.blit(zebra_h, ((win_x - lane * 6 - 26 * px) / 2, (win_y - lane * 4) / 2 - lane))
        win.blit(zebra_h, ((win_x - lane * 6 - 26 * px) / 2, (win_y - lane * 4) / 2 + 5.5 * lane))
        win.blit(zebra_h,
                 ((win_x - lane * 6 - 26 * px) / 2 + 3 * lane + 26 * px, (win_y - lane * 4) / 2 - lane))
        win.blit(zebra_h, (
            (win_x - lane * 6 - 26 * px) / 2 + 3 * lane + 26 * px, (win_y - lane * 4) / 2 + 4.5 * lane))

        # lines

        # self.drawGrid()

        for i in range(0, 5):
            pygame.draw.line(win, darkgrey, (0, (win_y - lane * 4) / 2 + i * lane),
                             ((win_x - lane * 6 - 26 * px) / 2, (win_y - lane * 4) / 2 + i * lane), 1)
            pygame.draw.line(win, darkgrey,
                             (((win_x - lane * 6 - 26 * px) / 2 + 6 * lane + 26 * px),
                              ((win_y - lane * 4) / 2 + i * lane)),
                             (win_x, ((win_y - lane * 4) / 2 + i * lane)), 1)

        pygame.draw.line(win, darkgrey, (0, (win_y - lane * 4) / 2 + 5 * lane),
                         ((win_x - lane * 6 - 26 * px) / 2, (win_y - lane * 4) / 2 + 5 * lane), 1)

        for i in range(0, 3):
            pygame.draw.line(win, darkgrey, ((win_x - lane * 6 - 26 * px) / 2 + (i + 1) * lane, 0),
                             ((win_x - lane * 6 - 26 * px) / 2 + (i + 1) * lane, win_y), 1)
            pygame.draw.line(win, darkgrey, ((win_x - lane * 6 - 26 * px) / 2 + (i + 3) * lane + 26 * px, 0),
                             ((win_x - lane * 6 - 26 * px) / 2 + (i + 3) * lane + 26 * px, win_y), 1)

        pygame.draw.line(win, darkgrey, ((win_x - lane * 6 - 26 * px) / 2, 0),
                         ((win_x - lane * 6 - 26 * px) / 2, (win_y - lane * 4) / 2), 1)
        pygame.draw.line(win, darkgrey, ((win_x - lane * 6 - 26 * px) / 2 + 6 * lane + 26 * px, 0),
                         ((win_x - lane * 6 - 26 * px) / 2 + 6 * lane + 26 * px, (win_y - lane * 4) / 2), 1)
        pygame.draw.line(win, darkgrey, ((win_x - lane * 6 - 26 * px) / 2, (win_y - lane * 4) / 2 + 5 * lane),
                         ((win_x - lane * 6 - 26 * px) / 2, win_y), 1)
        pygame.draw.line(win, darkgrey, (
            (win_x - lane * 6 - 26 * px) / 2 + 6 * lane + 26 * px, (win_y - lane * 4) / 2 + 4 * lane),
                         ((win_x - lane * 6 - 26 * px) / 2 + 6 * lane + 26 * px, win_y), 1)

        for i in range(1, 4):
            pygame.draw.line(win, darkblue, (0, (win_y - lane * 4) / 2 + i * lane),
                             (win_y, (win_y - lane * 4) / 2 + i * lane), 1)

        pygame.draw.line(win, darkgrey, (0, (win_y - lane * 4) / 2 + 4 * lane),
                         ((win_x - lane * 6 - 26 * px) / 2 + lane, (win_y - lane * 4) / 2 + 4 * lane), 1)
