import turtle

from multiprocessing import Pool
from os import path

from algorithm.parameters import params
from fitness.evaluation import evaluate_fitness
from operators.initialisation import initialisation
from representation.population import Population
from stats.stats import stats, get_stats
from utilities.algorithm.initialise_run import pool_init
from utilities.stats import trackers

def search_loop():
    """
    This is a standard search process for an evolutionary algorithm. Loop over
    a given number of generations.

    :return: The final population after the evolutionary process has run for
    the specified number of generations.
    """

    if params['MULTICORE']:
        # initialize pool once, if mutlicore is enabled
        params['POOL'] = Pool(processes=params['CORES'], initializer=pool_init,
                              initargs=(params,))  # , maxtasksperchild=1)

    # Initialise population
    individuals = initialisation(params['POPULATION_SIZE'])

    # Evaluate initial population
    individuals = evaluate_fitness(individuals)

    # Generate statistics for run so far
    get_stats(individuals)

    # Traditional GE
    for generation in range(1, (params['GENERATIONS']+1)):
        trackers.current_generation = generation
        stats['gen'] = generation

        # New generation
        individuals = params['STEP'](individuals)

        # Save the phenotypes of the last generation
        if generation == params['GENERATIONS']:
            with open(path.join(params['FILE_PATH'], 'last_generation_phenotypes.txt'), 'a') as f:
                for individual in individuals:
                    if individual.phenotype is not None: f.write(individual.phenotype + '\n')

    if params['DRAW_LAST_GEN_CLS_BEST']:
        for idx, cluster in enumerate(Population(individuals, params['CUT_OFF_RATIO'], params['NUMBER_OF_CLUSTERS']).cluster_individuals()):
            draw_phenotype(max(cluster).phenotype, idx)

    if params['MULTICORE']:
        # Close the workers pool (otherwise they'll live on forever).
        params['POOL'].close()

    return individuals


def search_loop_from_state():
    """
    Run the evolutionary search process from a loaded state. Pick up where
    it left off previously.

    :return: The final population after the evolutionary process has run for
    the specified number of generations.
    """

    individuals = trackers.state_individuals

    if params['MULTICORE']:
        # initialize pool once, if mutlicore is enabled
        params['POOL'] = Pool(processes=params['CORES'], initializer=pool_init,
                              initargs=(params,))  # , maxtasksperchild=1)

    # Traditional GE
    for generation in range(stats['gen'] + 1, (params['GENERATIONS'] + 1)):
        stats['gen'] = generation

        # New generation
        individuals = params['STEP'](individuals)

    if params['MULTICORE']:
        # Close the workers pool (otherwise they'll live on forever).
        params['POOL'].close()

    return individuals

def draw_phenotype(phenotype, idx):
    turtle.resetscreen()
    for move in phenotype:
        if move == 'F':
            turtle.forward(2)
        elif move == 'B':
            turtle.backward(2)
        elif move == '+':
            turtle.left(90)
        elif move == '-':
            turtle.right(90)
    turtle.getscreen().getcanvas().postscript(file=path.join(params['FILE_PATH'], 'phenotype_plot-' + str(idx) + '.eps'))
