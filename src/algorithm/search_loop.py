from multiprocessing import Pool
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

    population = Population(individuals, params['SELECTION_PROPORTION'], params['NUMBER_OF_CLUSTERS'])

    # Traditional GE
    for generation in range(1, (params['GENERATIONS']+1)):
        trackers.current_generation = generation

        stats['gen'] = generation

        # New generation
        population.evolve()
        # Generate statistics for run so far
        get_stats(population.individuals)

    if params['MULTICORE']:
        # Close the workers pool (otherwise they'll live on forever).
        params['POOL'].close()

    return population.individuals


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
