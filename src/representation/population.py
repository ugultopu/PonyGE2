from random import choices

from algorithm.parameters import params
from fitness.evaluation import evaluate_fitness
from operators.crossover import crossover_inds
from operators.initialisation import initialisation
from operators.mutation import mutation


class Population:
    def __init__(self, selection_proportion):
        self.current_generation = 0
        self.individuals = sorted(evaluate_fitness(initialisation(params['POPULATION_SIZE']), current_generation=self.current_generation))
        self.cut_off_count = int(len(self) * (1 - selection_proportion))

        self.update_fittest_individuals()
        self.update_probabilities()


    def __len__(self):
        return len(self.individuals)


    def __str__(self):
        return '--------' + '\n' + '\n'.join( [str(individual) for individual in self.individuals] ) + '--------' + '\n'


    def update_fittest_individuals(self):
        self.fittest_individuals = self.individuals[self.cut_off_count:]


    def normalized_compression_distance_sums(self):
        """For each fittest individual, compute the sum of Normalized
        Compression Distances between each pair of fittest individual."""
        return [sum([i.normalized_compression_distance(j) for j in self.fittest_individuals]) for i in self.fittest_individuals]


    def update_probabilities(self):
        """Compute the probability of each fittest individual w.r.t sum of their
        Normalized Compression Distances and store the probabilities."""
        sums = self.normalized_compression_distance_sums()
        total_sum = sum(sums)
        self.probabilities = [individual_sum / total_sum for individual_sum in sums]


    def _get_parents_for_crossover(self):
        """Return two individuals according to their probabilities."""
        return choices(self.fittest_individuals, weights=self.probabilities, k=2)


    def children(self):
        """Return a list of children from this population."""
        children = []
        while len(children) < self.cut_off_count: children.extend(crossover_inds(*self._get_parents_for_crossover()))
        return evaluate_fitness(mutation(children), current_generation=self.current_generation)


    def update_normalized_compression_distance_cache_of_fittest_individuals(self, old_fittest_individuals):
        """Remove the normalized compression distances between the current
        fittest elements and the elements that have been removed from the
        fittest individuals."""
        removed_elements = set(old_fittest_individuals) - set(self.fittest_individuals)
        for individual in self.fittest_individuals: individual.remove_obsolete_elements_from_normalized_compression_distances(removed_elements)


    def evolve(self):
        """Evolve and go to the next generation. Also perform necessary
        computations upon going to the next generation."""
        self.current_generation += 1
        self.individuals = sorted(self.fittest_individuals + self.children())
        old_fittest_individuals = self.fittest_individuals
        self.update_fittest_individuals()
        self.update_normalized_compression_distance_cache_of_fittest_individuals(old_fittest_individuals)
        self.update_probabilities()


    def plot_and_save_the_best_individual(self):
        """Plot the most fit individual of the population and save the plot."""
        max(self.individuals).save_positions_plot(f'generation_{self.current_generation}-best')
