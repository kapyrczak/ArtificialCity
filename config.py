cell_size = 9  # in px
screen_size = width, height = 100 * cell_size, 100 * cell_size
lane_width = 4 * cell_size  # in meters

tps = 100 # used to simulate cars and pedestrians
fps = 50 # used in visualization
car_speed_limit = 50
car_spawn_prob = 0.1
car_slow_prob = 0.45
car_v_change = 1
car_slow_duration = 2

tram_speed_limit = 35
tram_spawn_interval = 500
tram_slow_prob = 0.05
tram_v_change = 0.2



pedestrian_spawn_prob = 0.008


"""
dictionary: 
{lane_from_number: [lane_into, at_length, untill_length, appear_at_travelled]}
untill length is necesarry because it is not very probable that a car will
get self.travelled value that is exactly equal to the `at_length`
appear_at_travelled is distance on which the car should appear on `lane_into`
"""
turns = {1: None,
         2: [7, 25, 35, 58],
         3: [6, 21, 30, 62],
         4: [11, 21, 30, 58],
         5: None,
         6: [1, 38, 50, 0],
         7: None,
         8: None,
         9: None,
         10: None,
         11: [5, 38, 45, 0]
         }

"""
dictionary:
{lane_number: [distance_from_beggining, green_lit_time, red_lit_time, starting_red?]}
Times in SECONDS
"""
traffic_lights = {1: None, # horizontal, turn-into west
                  2: [18, 4, 5, True], # horizontal, east
                  3: [18, 4, 5, True],    
                  4: [18, 4, 5, True], # horizontal, west
                  5: None, # vertical, turn-into east
                  6: [35, 4, 5, False], # vertical, south
                  7: [35, 4, 5, False],
                  8: [35, 4, 5, False],
                  9: [35, 4, 5, False], # vertical, north
                  10: [35, 4, 5, False],
                  11: [35, 4, 5, False]
                  }

tram_traffic_lights = {1: [[18, 59], 4, 5, True],
                       2: [[2, 43], 4, 5, True]
                       }

'''Each value is a list of tuples: (number_of_other_lane, travelled_at_other, travelled_at_self'''
car_lanes_going_through = {1: {'tram': [], 'pedestrian': []}, # Dla tych pasów 'tram'
                           2: {'tram': [], 'pedestrian': []}, # nie ma znaczenia,
                           3: {'tram': [], 'pedestrian': []}, # bo samochody
                           4: {'tram': [], 'pedestrian': []}, # i tak nie będą
                           5: {'tram': [], 'pedestrian': []}, # przejeżdżać po
                           6: {'tram': [], 'pedestrian': []}, # innych pasach
                           7: {'tram': [(1, 83, 44), (2, 29, 48)], 'pedestrian': []},
                           8: {'tram': [(1, 79, 44), (2, 33, 48)], 'pedestrian': []},
                           9: {'tram': [(1, 49, 48), (2, 63, 44)], 'pedestrian': []},
                           10: {'tram': [(1, 45, 48), (2, 67, 44)], 'pedestrian': []},
                           11: {'tram': [], 'pedestrian': []}} # ten też

tram_lanes_going_through = {1: {'car': [(7, 49, 65), (8, 49, 61.5),
                                        (9, 53, 31), (10, 53, 27)], 'pedestrian': []},
                            2: {'car': [(7, 53, 11), (8, 53, 15),
                                        (9, 49, 45.5), (10, 49, 49)], 'pedestrian': []}}
'''
dictionaries:
-> car_lanes: [ lane_number : x or y initial position]
-> tram_lanes: [ lane_number : y initial position ]
-> zebra_lanes: [ lane_numer : (x initial position, y initial position) ]
'''

v_first_lane_x = (width - lane_width * 6 - 26 * cell_size) / 2
h_first_lane_x = (height - lane_width * 4) / 2

car_lanes = [
    # horizontal lanes -> y
    (1, h_first_lane_x),
    (2, h_first_lane_x + 3 * lane_width),
    (3, h_first_lane_x + 4 * lane_width),
    (4, h_first_lane_x),
    (5, h_first_lane_x + 3 * lane_width),

    # vertical lanes -> x
    (6, v_first_lane_x),
    (7, v_first_lane_x + 1 * lane_width),
    (8, v_first_lane_x + 2 * lane_width),
    (9, v_first_lane_x + 26 * cell_size + 3 * lane_width),
    (10, v_first_lane_x + 26 * cell_size + 4 * lane_width),
    (11, v_first_lane_x + 26 * cell_size + 5 * lane_width),
]

tram_lanes = [
    (1, h_first_lane_x + 1 * lane_width),
    (2, h_first_lane_x + 2 * lane_width)
]

zebra_lanes = [
    # vertical
    (1, (v_first_lane_x - lane_width, h_first_lane_x)),
    (2, (v_first_lane_x - 0.75 * lane_width, h_first_lane_x + lane_width * 5)),
    (3, (v_first_lane_x + 26 * cell_size + 6.5 * lane_width, h_first_lane_x)),
    (4, (v_first_lane_x + 26 * cell_size + 6.75 * lane_width, h_first_lane_x + lane_width * 4)),

    # horizontal
    (5, (v_first_lane_x + 3 * lane_width, h_first_lane_x - lane_width)),
    (6, (v_first_lane_x, h_first_lane_x - 0.75 * lane_width)),

    (7, (v_first_lane_x + 6 * lane_width + 26 * cell_size, h_first_lane_x - lane_width)),
    (8, (v_first_lane_x + 3 * lane_width + 26 * cell_size, h_first_lane_x - 0.75 * lane_width)),

    (9, (v_first_lane_x + 3 * lane_width, h_first_lane_x + 5.5 * lane_width)),
    (10, (v_first_lane_x, h_first_lane_x + 5.75 * lane_width)),

    (11, (v_first_lane_x + 6 * lane_width + 26 * cell_size, h_first_lane_x + 4.5 * lane_width)),
    (12, (v_first_lane_x + 3 * lane_width + 26 * cell_size, h_first_lane_x + 4.75 * lane_width)),
]

c_lanes_coordinates = dict(car_lanes)
z_lanes_coordinates = dict(zebra_lanes)
t_lanes_coordinates = dict(tram_lanes)
