from algorithm.parameters import params
from fitness.base_ff_classes.base_ff import base_ff
from utilities.stats import trackers

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

class structure_silhouette(base_ff):
    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()

    def evaluate(self, ind, **kwargs):
        if not hasattr(ind, 'max_x'):
            # X and Y position
            position = [0, 0]
            direction = 'EAST'
            max_x = 0
            max_y = 0
            for move in ind.phenotype:
                if move == 'F':
                    # Get the new position
                    position = [cc + nc for cc, nc in zip(position, get_position_difference_for_direction(direction))]
                    # If we end up below the ground or left of the origin, stop.
                    if position[0] < 0 or position[1] < 0: break
                    # Update the max X and Y values.
                    max_x = position[0] if position[0] > max_x else max_x
                    max_y = position[1] if position[1] > max_y else max_y
                # If we're not moving forward, this means that we're rotating, since
                # the only other options apart from 'F' are '+', '-' or 'T', which
                # correspond to rotating counter-clockwise, rotating clockwise
                # or finishing.
                else:
                    try:
                        direction = get_next_direction(direction, move)
                    except ValueError as e:
                        # 'T' means end of phenotype.
                        if e.args[1] == 'T': break
                        else: raise
            ind.max_x = max_x
            ind.max_y = max_y

        if trackers.current_generation < params['GENERATIONS'] * .4: return 1 / ( ind.max_y + 1 )
        elif trackers.current_generation < params['GENERATIONS'] * .6: return 1 / ( ind.max_x + 1 )
        elif trackers.current_generation < params['GENERATIONS'] * .8: return 1 / ( ind.max_y + 1 )
        else: return 1 / ( ind.max_x + 1 )
