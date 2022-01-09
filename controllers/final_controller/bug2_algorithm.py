from enum import Enum
from initialization import *
from motion import *
from sense import *
from wall_follow import wall_follow


class State(Enum):
    init = 1
    line_follow = 2
    get_parallel_to_wall = 3
    wall_follow = 4
    reached_destination = 5
    cannot_reach_destination = 6


goal_position = np.array([1.3, 6.15])  # <x,y>
initial_position = np.array([1.3, -9.74])

threshold = 0.08
# head: sonar[1], ir[0], ir[3]

robot_heading = None

wall_in_front = False

gps_values = None
compass_val = None
sonar_value = None
encoder_value = None
ir_value = None

rotate_final_degree = None
rotation_dir = None


def set_state():
    global wall_in_front
    wall_in_front = avoid_wall_in_front(sonar_value[1])

    global rotation_dir
    global rotate_final_degree

    if bug2.state == State.line_follow and wall_in_front:
        bug2.prev_state = bug2.state
        bug2.state = State.get_parallel_to_wall

        # set rotate_final_degree
        rotation_dir = choice(['left', 'right'])
        if rotation_dir == 'left':
            rotate_final_degree = (robot_heading - 90) % 360
            wall_to_right = False
            wall_to_left = True
        else:
            rotate_final_degree = (robot_heading + 90) % 360
            wall_to_right = True
            wall_to_left = False


def bug2():
    global wall_in_front
    global wall_to_right
    global wall_to_left

    global gps_values
    global compass_val
    global sonar_value
    global encoder_value
    global ir_value

    if bug2.state == State.reached_destination or bug2.state == State.cannot_reach_destination:
        return

    gps_values, compass_val, sonar_value, encoder_value, ir_value = read_sensors_values()

    print('sonar: ', sonar_value)
    print('ir: ', ir_value)
    print('-----')

    global robot_heading
    robot_heading = get_bearing_in_degrees(compass_val)

    if not bug2.state == State.init:
        set_state()

    if bug2.state == State.init:
        if head_to_destination(robot_heading, gps_values, goal_position):
            bug2.prev_state = bug2.state
            bug2.state = State.line_follow
    elif bug2.state == State.line_follow:
        move_forward()
    elif bug2.state == State.get_parallel_to_wall:
        if rotation_dir == 'left':
            done = inplace_rotate(robot_heading, rotate_final_degree)
        else:
            done = inplace_rotate(robot_heading, rotate_final_degree, -1)
        if done:
            bug2.prev_state = bug2.state
            bug2.state = State.wall_follow
            wall_in_front = False
    elif bug2.state == State.wall_follow:
        wall_follow()


bug2.state = State.init
bug2.prev_state = State.init
