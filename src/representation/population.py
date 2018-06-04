from random import choice

from numpy import array
from sklearn.cluster import KMeans

from algorithm.parameters import params
from fitness.evaluation import evaluate_fitness
from operators.crossover import crossover_inds
from operators.mutation import mutation


class Population:
    def __init__(self, individuals, cut_off_ratio, number_of_clusters):
        self.individuals = sorted(individuals)
        self.cut_off_ratio = cut_off_ratio
        self.cut_off_count = int(len(self) * self.cut_off_ratio)
        self.number_of_clusters = number_of_clusters
        self.k_means = KMeans(n_clusters=number_of_clusters)

        self.update_fittest_individuals()
        self.update_cluster_individuals()


    def __len__(self):
        return len(self.individuals)


    def __repr__(self):
        return '--------' + '\n' + '\n'.join( [str(individual) for individual in self.individuals] ) + '--------' + '\n'


    def update_fittest_individuals(self):
        self.fittest_individuals = self.individuals[self.cut_off_count:]


    def normalized_compression_distances(self):
        """Compute the Normalized Compression Distances between each pair of
        individuals."""
        return array( [[i.normalized_compression_distance(j) for j in self.fittest_individuals] for i in self.fittest_individuals] )


    def clusters(self):
        """Clusterize the population."""
        return self.k_means.fit_predict(self.normalized_compression_distances())


    def update_cluster_individuals(self):
        """Return a list of list of individuals. Each set in the list contains
        the individuals of the respective cluster index."""
        clusters = self.clusters()
        self.cluster_individuals = [ [ self.fittest_individuals[individual_index] for individual_index, individual_cluster in enumerate(clusters) if individual_cluster == current_cluster ] for current_cluster in range(self.number_of_clusters) ]


    def _get_parents_for_crossover(self):
        """Returns two individuals from different clusters."""
        cluster_individuals = self.cluster_individuals
        parent_0_cluster = choice(cluster_individuals)
        parent_1_cluster = choice(cluster_individuals)
        while parent_0_cluster == parent_1_cluster or not parent_0_cluster or not parent_1_cluster:
            parent_0_cluster = choice(cluster_individuals)
            parent_1_cluster = choice(cluster_individuals)
        return ( choice(tuple(parent_0_cluster)), choice(tuple(parent_1_cluster)) )


    def children(self):
        """Return a list of children from this population."""
        children = []
        while len(children) < self.cut_off_count:
            parents = self._get_parents_for_crossover()
            new_children = crossover_inds(parents[0], parents[1])
            if new_children is not None: children.extend(new_children)
        return evaluate_fitness(mutation(children))


    def update_normalized_compression_distance_cache_of_fittest_individuals(self, old_fittest_individuals):
        """Remove the normalized compression distances between the current
        fittest elements and the elements that have been removed from the
        fittest individuals."""
        removed_elements = set(old_fittest_individuals) - set(self.fittest_individuals)
        for individual in self.fittest_individuals: individual.remove_obsolete_elements_from_normalized_compression_distances(removed_elements)


    def evolve(self):
        """Evolve and go to the next generation. Also perform necessary
        computations upon going to the next generation."""
        self.individuals = sorted(self.fittest_individuals + self.children())
        old_fittest_individuals = self.fittest_individuals
        self.update_fittest_individuals()
        self.update_normalized_compression_distance_cache_of_fittest_individuals(old_fittest_individuals)
        self.update_cluster_individuals()
