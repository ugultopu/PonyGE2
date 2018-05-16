from algorithm.parameters import params

def get_valid_individuals(population):
    return [i for i in population if not i.invalid]

# Gets the most fit part of the population by removing the least fit
# params['CLUSTERING_RATIO'] part of the population.
def get_fittest_population(population):
    return sorted(get_valid_individuals(population))[int(len(population) * params['CLUSTERING_RATIO']):]
