import numpy as np
import math

from initialization import update_motor_speed


def get_bearing_in_degrees(compass_val):
    rad = np.arctan2(compass_val[0], compass_val[1])
    bearing = (rad - 1.5708) / math.pi * 180.0

    return bearing + 270


def avoid_wall_in_front(front_sonar_val):
    # IR is no good here
    if front_sonar_val < 80:
        # stop
        update_motor_speed(input_omega=[0, 0, 0])
        return True
    return False
