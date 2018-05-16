from algorithm.parameters import params

# Gets the most fit part of the population by removing the least fit
# params['CLUSTERING_RATIO'] part of the population.
def get_fittest_population(population):
    return sorted(population)[int(len(population) * params['CLUSTERING_RATIO']):]
