import random
import itertools

from os import path
from math import hypot
from sklearn.cluster import KMeans

from algorithm.parameters import params
from utilities.population import get_valid_individuals
from utilities.population import get_fittest_population
from utilities.algorithm.NSGA2 import compute_pareto_metrics, \
    crowded_comparison_operator

def selection(population):
    """
    Perform selection on a population in order to select a population of
    individuals for variation.

    :param population: input population
    :return: selected population
    """

    return params['SELECTION'](population)

def clustering(population):
    population = get_fittest_population(population)

    # Get 2-combination of the population
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

    k_means = KMeans(n_clusters=params['NUMBER_OF_CLUSTERS'])

    clusters = k_means.fit_predict(differences_in_combinations)

    # Save the phenotypes that are closest to the center of the clusters.
    with open(path.join(params['FILE_PATH'], 'cluster_center_phenotypes.txt'), 'a') as f:
        for cluster_center in k_means.cluster_centers_:
            closest_combo = min(differences_in_combinations, key=lambda diff:hypot(diff[0] - cluster_center[0], diff[1] - cluster_center[1]))
            closest_individuals = combinations[differences_in_combinations.index(closest_combo)]
            f.write(closest_individuals[0].phenotype + '\n')
            f.write(closest_individuals[1].phenotype + '\n')

    # Put the combination indices of every cluster to a seperate array.
    partitioned_clusters = [ [i for i, e in enumerate(clusters) if e == n] for n in range(params['NUMBER_OF_CLUSTERS']) ]

    parents = []

    # Select a random cluster and a random combo from that cluster and add the
    # two phenotypes to the parents list.
    for _ in range(int((params['GENERATION_SIZE'] * params['CLUSTERING_RATIO']) / 2)):
        selected_cluster_index = random.randrange(0, params['NUMBER_OF_CLUSTERS'])
        # FIXME Consider using a dictionary instead of a tuple to express the
        # cluster indices of the parents. If you do this, you need to edit the
        # code about clustering in 'src/operators/crossover.py' as well.
        while len(partitioned_clusters[selected_cluster_index]) == 0:
            selected_cluster_index = random.randrange(0, params['NUMBER_OF_CLUSTERS'])
        parents.extend(
            [ (i, selected_cluster_index) for i in combinations[random.choice(partitioned_clusters[selected_cluster_index])] ]
        )

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
