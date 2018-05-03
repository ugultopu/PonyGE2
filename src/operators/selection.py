import numpy
import random
import itertools

from sklearn.cluster import KMeans

from algorithm.parameters import params
from utilities.algorithm.NSGA2 import compute_pareto_metrics, \
    crowded_comparison_operator

# FIXME Read this from 'params'
NUMBER_OF_CLUSTERS = 5

def selection(population):
    """
    Perform selection on a population in order to select a population of
    individuals for variation.

    :param population: input population
    :return: selected population
    """

    # FIXME Specify 'clustering' in 'params'
    return clustering(population)

def clustering(population):
    # Weed out the invalid individuals
    population = [i for i in population if not i.invalid]

    combinations = list(itertools.combinations(population, 2))
    differences_in_combinations = []

    for combo in combinations:
        phenotype_0_length = len(combo[0].phenotype)
        phenotype_1_length = len(combo[1].phenotype)
        if phenotype_0_length < phenotype_1_length:
            short_phenotype_length = phenotype_0_length
            long_phenotype_length = phenotype_1_length
        else:
            short_phenotype_length = phenotype_1_length
            long_phenotype_length = phenotype_0_length

        for i, (unit_0, unit_1) in enumerate(zip(combo[0].phenotype, combo[1].phenotype)):
            if unit_0 != unit_1:
                differences_in_combinations.append((i, short_phenotype_length + long_phenotype_length - 2 * i))
                break
            if i == short_phenotype_length - 1:
                differences_in_combinations.append((short_phenotype_length, long_phenotype_length - short_phenotype_length))

    differences_in_combinations = numpy.array(differences_in_combinations)

    clusters = KMeans(n_clusters=NUMBER_OF_CLUSTERS).fit_predict(differences_in_combinations)

    partitioned_clusters = []

    for n in range(NUMBER_OF_CLUSTERS):
        partitioned_clusters.append([i for i, e in enumerate(clusters) if e == n])

    parents = []

    for _ in range(int(params['GENERATION_SIZE'] / 2)):
        parents.extend(combinations[random.choice(partitioned_clusters[random.randrange(0, NUMBER_OF_CLUSTERS)])])

    return parents

def tournament(population):
    """
    Given an entire population, draw <tournament_size> competitors randomly and
    return the best. Only valid individuals can be selected for tournaments.

    :param population: A population from which to select individuals.
    :return: A population of the winners from tournaments.
    """

    # Initialise list of tournament winners.
    winners = []

    # The flag "INVALID_SELECTION" allows for selection of invalid individuals.
    if params['INVALID_SELECTION']:
        available = population
    else:
        available = [i for i in population if not i.invalid]

    while len(winners) < params['GENERATION_SIZE']:
        # Randomly choose TOURNAMENT_SIZE competitors from the given
        # population. Allows for re-sampling of individuals.
        competitors = random.sample(available, params['TOURNAMENT_SIZE'])

        # Return the single best competitor.
        winners.append(max(competitors))

    # Return the population of tournament winners.
    return winners


def truncation(population):
    """
    Given an entire population, return the best <proportion> of them.

    :param population: A population from which to select individuals.
    :return: The best <proportion> of the given population.
    """

    # Sort the original population.
    population.sort(reverse=True)

    # Find the cutoff point for truncation.
    cutoff = int(len(population) * float(params['SELECTION_PROPORTION']))

    # Return the best <proportion> of the given population.
    return population[:cutoff]


def nsga2_selection(population):
    """Apply NSGA-II selection operator on the *population*. Usually, the
    size of *population* will be larger than *k* because any individual
    present in *population* will appear in the returned list at most once.
    Having the size of *population* equals to *k* will have no effect other
    than sorting the population according to their front rank. The
    list returned contains references to the input *population*. For more
    details on the NSGA-II operator see [Deb2002]_.

    :param population: A population from which to select individuals.
    :returns: A list of selected individuals.
    .. [Deb2002] Deb, Pratab, Agarwal, and Meyarivan, "A fast elitist
       non-dominated sorting genetic algorithm for multi-objective
       optimization: NSGA-II", 2002.
    """

    selection_size = params['GENERATION_SIZE']
    tournament_size = params['TOURNAMENT_SIZE']

    # Initialise list of tournament winners.
    winners = []

    # The flag "INVALID_SELECTION" allows for selection of invalid individuals.
    if params['INVALID_SELECTION']:
        available = population
    else:
        available = [i for i in population if not i.invalid]

    # Compute pareto front metrics.
    pareto = compute_pareto_metrics(available)

    while len(winners) < selection_size:
        # Return the single best competitor.
        winners.append(pareto_tournament(available, pareto, tournament_size))

    return winners


def pareto_tournament(population, pareto, tournament_size):
    """
    The Pareto tournament selection uses both the pareto front of the
    individual and the crowding distance.

    :param population: A population from which to select individuals.
    :param pareto: The pareto front information.
    :param tournament_size: The size of the tournament.
    :return: The selected individuals.
    """

    # Initialise no best solution.
    best = None

    # Randomly sample *tournament_size* participants.
    participants = sample(population, tournament_size)

    for participant in participants:
        if best is None or crowded_comparison_operator(participant, best,
                                                       pareto):
            best = participant

    return best


# Set attributes for all operators to define multi-objective operators.
nsga2_selection.multi_objective = True
