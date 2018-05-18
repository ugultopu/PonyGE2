from algorithm.parameters import params
from fitness.base_ff_classes.base_ff import base_ff

DIRECTIONS = ['EAST', 'NORTH', 'WEST', 'SOUTH']

def get_position_difference_for_direction(direction):
    if direction == 'EAST':
        return [1, 0]
    elif direction == 'NORTH':
        return [0, 1]
    elif direction == 'WEST':
        return [-1, 0]
    elif direction == 'SOUTH':
        return [0, -1]
    else:
        raise ValueError('Unknown direction', direction)

def get_next_direction(direction, turn_direction):
    if turn_direction == '+':
        return DIRECTIONS[(DIRECTIONS.index(direction) + 1) % len(DIRECTIONS)]
    elif turn_direction == '-':
        return DIRECTIONS[(DIRECTIONS.index(direction) - 1) % len(DIRECTIONS)]
    else:
        raise ValueError('Unknown turn direction', turn_direction)

class l_systems(base_ff):
    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()

    def evaluate(self, ind, **kwargs):
        # X and Y position
        position = [0, 0]
        direction = 'EAST'
        latest_forward_direction = 'EAST'
        area = 0
        number_of_corners = 0
        for move in ind.phenotype:
            if move == 'F':
                # If we start going west, don't evaluate the rest.
                if direction == 'WEST': break
                # Get the new position
                position = [a + b for a, b in zip(position, get_position_difference_for_direction(direction))]
                # If we end up below the ground or left of the origin, stop.
                if position[0] < 0 or position[1] < 0: break
                # If we're going east, we increase the area as much as the
                # current Y value.
                if direction == 'EAST': area += position[1]
                # Increase the number of corners if we started facing another
                # direction.
                if DIRECTIONS.index(direction) % 2 != DIRECTIONS.index(latest_forward_direction) % 2: number_of_corners += 1
                # Update the latest forward direction.
                latest_forward_direction = direction
            # If we're not moving forward, this means that we're rotating, since
            # the only other options apart from 'F' are '+' and '-', which
            # correspond to rotating counter-clockwise and clockwise.
            else:
                direction = get_next_direction(direction, move)

        return 1 / ( (area + 1) + (number_of_corners * 10) )
