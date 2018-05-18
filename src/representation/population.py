from itertools import combinations
from random import choice

from sklearn.cluster import KMeans


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
        if self._clusters is not None: return self._clusters


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
        # FIXME We might need to make 'combo_diffs' an instance variable in
        # order to calculate the cluster centers.
        combo_diffs = [combo_diffs(combo) for combo in self.combinations]
        self._clusters = self.k_means.fit_predict(combo_diffs)
        self.clusters()


    def cluster_individuals(self):
        """Return a set of individuals that belong to the specified cluster"""
        if self._cluster_individuals is not None: return self._cluster_individuals

        combo_indices_by_cluster = [ [i for i, e in enumerate(self.clusters()) if e == n] for n in range(self.number_of_clusters) ]
        self._cluster_individuals = [ {i for i in self.combinations[combo_index] for combo_index in combo_indices} for combo_indices in combo_indices_by_cluster ]
        self.cluster_individuals()


    def parents(self):
        """Get a set of parents from this population"""
        if self._parents is not None: return self._parents

        self._parents = {}
        while len(self._parents) < int(len(population) * cut_off_ratio):
            self._parents.add( choice(choice(self.cluster_individuals())) )
        self.parents()
