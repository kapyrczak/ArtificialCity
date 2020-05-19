cell_size = 9  # in px
screen_size = width, height = 100 * cell_size, 100 * cell_size
lane_width = 4 * cell_size  # in meters

car_lanes = [
    # horizontal lanes -> y
    (1, (height - lane_width * 4) / 2 + 0.25 * lane_width),
    (2, (height - lane_width * 4) / 2 + 3.25 * lane_width),
    (3, (height - lane_width * 4) / 2 + 4.25 * lane_width),
    (4, (height - lane_width * 4) / 2 + 0.25 * lane_width),
    (5, (height - lane_width * 4) / 2 + 3.25 * lane_width),

    # vertical lanes -> x
    (6, (width - lane_width * 6 - 26 * cell_size) / 2 + 0.25 * lane_width),
    (7, (width - lane_width * 6 - 26 * cell_size) / 2 + 1.25 * lane_width),
    (8, (width - lane_width * 6 - 26 * cell_size) / 2 + 2.25 * lane_width),
    (9, (width - lane_width * 6 - 26 * cell_size) / 2 + 26 * cell_size + 3.25 * lane_width),
    (10, (width - lane_width * 6 - 26 * cell_size) / 2 + 26 * cell_size + 4.25 * lane_width),
    (11, (width - lane_width * 6 - 26 * cell_size) / 2 + 26 * cell_size + 5.25 * lane_width),
]

tram_lanes = [
    (1, (height - lane_width * 4) / 2 + 1.25 * lane_width),
    (2, (height - lane_width * 4) / 2 + 2.25 * lane_width)
]

zebra_lanes = [

]

c_lanes_coordinates = dict(car_lanes)
z_lanes_coordinates = dict(zebra_lanes)
t_lanes_coordinates = dict(tram_lanes)
