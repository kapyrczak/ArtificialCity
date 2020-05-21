cell_size = 6  # in px
screen_size = width, height = 100 * cell_size, 100 * cell_size
lane_width = 4 * cell_size  # in meters

tps = 100
car_speed_limit = 50
car_spawn_prob = 0.01
car_slow_prob = 0.48
car_v_change = 1
car_slow_duration = 2

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
