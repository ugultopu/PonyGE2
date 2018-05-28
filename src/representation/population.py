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
        return self.individuals[int(len(self) * self.cut_off_ratio):]


    def clusters(self):
        """Clusterize the population"""
        try: return self._clusters
        except AttributeError:
            def combo_diffs(combo):
                """Calculate the length of the phenotypes that match from the
                beginning and the length that does not match"""
                phenotype_0 = combo[0].phenotype
                phenotype_1 = combo[1].phenotype
                for i, (t0, t1) in enumerate(zip(phenotype_0, phenotype_1)):
                    if t0 != t1:
                        return (i, len(phenotype_0) + len(phenotype_1) - 2 * i)
                return (i, abs(len(phenotype_0) - len(phenotype_1)))


            self.combinations = list(combinations(self.fittest_individuals(), 2))
            # FIXME We might need to make '_combo_diffs' an instance variable in
            # order to calculate the cluster centers.
            _combo_diffs = [combo_diffs(combo) for combo in self.combinations]
            self._clusters = self.k_means.fit_predict(_combo_diffs)
            return self.clusters()


    def cluster_individuals(self):
        """Return a list of set of individuals. Each set in the list contains
        the individuals of the respective cluster index."""
        try: return self._cluster_individuals
        except AttributeError:
            clusters = self.clusters()
            combo_indices_by_cluster = [ [i for i, e in enumerate(clusters) if e == n] for n in range(self.number_of_clusters) ]
            self._cluster_individuals = [ {i for combo_index in combo_indices for i in self.combinations[combo_index] } for combo_indices in combo_indices_by_cluster ]
            if params['PRINT_CLUSTER_BEST']:
                for cluster in self._cluster_individuals:
                    print(f"{len(cluster)} {max(cluster)}")
                print()
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
