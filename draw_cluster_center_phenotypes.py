import turtle

FILE_PATH = '/Users/utku/src/python/PonyGE2/results/TA3E3.WPA.Dal.Ca_18_5_5_190218_71581_10883_71581/cluster_center_phenotypes.txt'
NUMBER_OF_CLUSTERS = 5
EVERY_Nth_GENERATION = 10

def move_turtle_to_origin():
    turtle.penup()
    turtle.home()
    turtle.pendown()

def get_count_for_line_segment(line_segments, line_segment_counts, first_position, second_position):
    if (first_position, second_position) in line_segments:
        return line_segment_counts[line_segments.index((first_position, second_position))]
    elif (second_position, first_position) in line_segments:
        return line_segment_counts[line_segments.index((second_position, first_position))]
    else:
        return 0

def set_line_width(line_segments, line_segment_counts, first_position, second_position):
    turtle.width(1 + get_count_for_line_segment(line_segments, line_segment_counts, first_position, second_position))

def increment_count_for_line_segment(line_segments, line_segment_counts, first_position, second_position):
    line_segment_counts[line_segments.index((first_position, second_position))] += 1

def add_to_line_segments(line_segments, line_segment_counts, current_position, next_position):
    if (current_position, next_position) in line_segments:
        increment_count_for_line_segment(line_segments, line_segment_counts, current_position, next_position)
    elif (next_position, current_position) in line_segments:
        increment_count_for_line_segment(line_segments, line_segment_counts, next_position, current_position)
    else:
        line_segments.append((current_position, next_position))
        line_segment_counts.append(1)

def get_next_position_for_direction(direction):
    if direction == 'FORWARD':
        direction_multiplier = 1
    elif direction == 'BACKWARD':
        direction_multiplier = -1
    else:
        raise ValueError('Unexpected direction:', direction)

    current_position = turtle.pos()

    turtle_heading = turtle.heading()
    if turtle_heading == 0:
        return turtle.Vec2D(current_position[0] + 100 * direction_multiplier, current_position[1])
    elif turtle_heading == 90:
        return turtle.Vec2D(current_position[0], current_position[1] + 100 * direction_multiplier)
    elif turtle_heading == 180:
        return turtle.Vec2D(current_position[0] - 100 * direction_multiplier, current_position[1])
    elif turtle_heading == 270:
        return turtle.Vec2D(current_position[0], current_position[1] - 100 * direction_multiplier)
    else:
        raise ValueError('Unexpected turtle heading (turtle angle):', turtle_heading)

def draw_phenotypes(cluster_idx, phenotype_list):
    turtle.reset()
    line_segments = []
    line_segment_counts = []
    for phenotype in phenotype_list:
        move_turtle_to_origin()
        current_position = turtle.pos()
        for move in phenotype:
            if move == 'F':
                next_position = get_next_position_for_direction('FORWARD')
                add_to_line_segments(line_segments, line_segment_counts, current_position, next_position)
                set_line_width(line_segments, line_segment_counts, current_position, next_position)
                turtle.forward(100)
            elif move == 'B':
                next_position = get_next_position_for_direction('BACKWARD')
                add_to_line_segments(line_segments, line_segment_counts, current_position, next_position)
                set_line_width(line_segments, line_segment_counts, current_position, next_position)
                turtle.backward(100)
            elif move == '+':
                turtle.left(90)
            elif move == '-':
                turtle.right(90)
            current_position = turtle.pos()
    turtle.getscreen().getcanvas().postscript(file='phenotype_'+str(cluster_idx)+'.eps')

with open(FILE_PATH) as f:
    phenotypes = f.read().splitlines()

# Times 2, because we save two phenotypes for every cluster.
phenotypes_for_clusters = [ phenotypes[2*n::2*NUMBER_OF_CLUSTERS][::EVERY_Nth_GENERATION] for n in range(NUMBER_OF_CLUSTERS) ]

for cluster_idx, phenotype_list in enumerate(phenotypes_for_clusters):
    draw_phenotypes(cluster_idx, phenotype_list)
