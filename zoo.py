import random
from math import sqrt
from scipy.spatial import distance

sheep_move_dist = 0.5
wolf_move_dist = 1
init_pos_limit = 10


def correct_location(loc):
    loc[0] = float('{:.3f}'.format(loc[0]))
    loc[1] = float('{:.3f}'.format(loc[1]))
    return loc


def correct_move(loc):
    if loc[0] > init_pos_limit:
        loc[0] = init_pos_limit

    if loc[0] < -init_pos_limit:
        loc[0] = -init_pos_limit

    if loc[1] > init_pos_limit:
        loc[1] = init_pos_limit

    if loc[1] < -init_pos_limit:
        loc[1] = -init_pos_limit

    return loc


class Sheep:
    def __init__(self, _id):
        self.location = correct_location([random.uniform(-init_pos_limit, init_pos_limit),
                                          random.uniform(-init_pos_limit, init_pos_limit)
                                          ])
        self._id = _id

    def move(self):
        if self.location[0] is not None:
            direction = random.randint(1, 4)
            if direction == 1:
                self.location[0] += sheep_move_dist
            if direction == 2:
                self.location[0] -= sheep_move_dist
            if direction == 3:
                self.location[1] += sheep_move_dist
            if direction == 4:
                self.location[1] -= sheep_move_dist

            correct_move(self.location)
            correct_location(self.location)


class Wolf:
    def __init__(self):
        self.location = [0.0, 0.0]

    def move(self, sheeps):
        target_sheep = self.check_around(sheeps)
        sheep_is_daed = False
        if target_sheep[1] < wolf_move_dist :
            self.location = sheeps[target_sheep[0]].location

            sheeps[target_sheep[0]].location = [None, None]
            sheep_is_daed = True    # Jesli wilk zjadl owce, zmieniamy status

        else:
            dist_x_y = [abs(self.location[0] - sheeps[target_sheep[0]].location[0]),
                        abs(self.location[1] - sheeps[target_sheep[0]].location[1])
                        ]
            if dist_x_y[0] > dist_x_y[1]:
                if sheeps[target_sheep[0]].location[0] > self.location[0]:
                    self.location[0] += wolf_move_dist
                else:
                    self.location[0] -= wolf_move_dist
            else:
                if sheeps[target_sheep[0]].location[1] > self.location[1]:
                    self.location[1] += wolf_move_dist
                else:
                    self.location[1] -= wolf_move_dist

        return sheeps, target_sheep[0], sheep_is_daed

    def check_around(self, sheeps: Sheep):
        alive_sheeps = []
        for i in sheeps:
            if i.location[0] is not None:
                alive_sheeps.append((i._id,
                                     distance.euclidean(i.location, self.location)  # metoda ktora oblicza odleglosc
                                     ))                                             # miedzy punktami

        min_distance_sheep = alive_sheeps[0]

        for i in range(len(alive_sheeps)):
            if min_distance_sheep[1] > alive_sheeps[i][1]:
                min_distance_sheep = alive_sheeps[i]

        return min_distance_sheep

    def wolf_math(self, target_sheep):
        pass

