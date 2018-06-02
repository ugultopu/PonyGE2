import numpy as np

from itertools import combinations
from random import choice

from sklearn.cluster import KMeans

from algorithm.parameters import params


class Population:
    def __init__(self, individuals, cut_off_ratio, number_of_clusters):
        self.individuals = sorted(individuals)
        self.cut_off_ratio = cut_off_ratio
        self.number_of_clusters = number_of_clusters
        self.k_means = KMeans(n_clusters=number_of_clusters)


    def __len__(self):
        return len(self.individuals)


    def fittest_individuals(self):
        try: return self._fittest_individuals
        except AttributeError:
            self._fittest_individuals = self.individuals[int(len(self) * self.cut_off_ratio):]
            return self.fittest_individuals()


    def clusters(self):
        """Clusterize the population"""
        try: return self._clusters
        except AttributeError:
            self._clusters = self.k_means.fit_predict(self.normalized_compression_distances())
            return self.clusters()


    def cluster_individuals(self):
        """Return a list of set of individuals. Each set in the list contains
        the individuals of the respective cluster index."""
        try: return self._cluster_individuals
        except AttributeError:
            fittest_individuals = self.fittest_individuals()
            self._cluster_individuals = [ { fittest_individuals[individual_index] for individual_index, individual_cluster in enumerate(self.clusters()) if individual_cluster == current_cluster } for current_cluster in range(self.number_of_clusters) ]
            return self.cluster_individuals()


    def parents(self):
        """Get a set of parents from this population"""
        try: return self._parents
        except AttributeError:
            self._parents = set()
            while len(self._parents) < int(len(self.individuals) * self.cut_off_ratio):
                selected_cluster = choice(self.cluster_individuals())
                while not selected_cluster: selected_cluster = choice(self.cluster_individuals())
                self._parents.add( (choice(tuple(selected_cluster)), self.cluster_individuals().index(selected_cluster)) )
            return self.parents()


    def normalized_compression_distances(self):
        try: return self._normalized_compression_distances
        except AttributeError:
            fittest_individuals = self.fittest_individuals()
            # FIXME Compute only the values that are above the diagonal and take
            # the symmetric of them w.r.t the diagonal to compute the rest.
            self._normalized_compression_distances = np.matrix( [[i.normalized_compression_distance(j) for j in fittest_individuals] for i in fittest_individuals] )
            return self.normalized_compression_distances()
