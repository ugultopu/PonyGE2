import numpy
import itertools
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

NUMBER_OF_CLUSTERS = 5

with open('test.txt') as file:
  phenotypes = file.read().splitlines()

combinations = []

for combo in itertools.combinations(phenotypes, 2):
    phenotype_0_length = len(combo[0])
    phenotype_1_length = len(combo[1])
    if phenotype_0_length < phenotype_1_length:
        short_phenotype_length = phenotype_0_length
        long_phenotype_length = phenotype_1_length
    else:
        short_phenotype_length = phenotype_1_length
        long_phenotype_length = phenotype_0_length

    for i, (unit_0, unit_1) in enumerate(zip(combo[0], combo[1])):
        if unit_0 != unit_1:
            combinations.append([i, short_phenotype_length + long_phenotype_length - 2 * i])
            break
        if i == short_phenotype_length - 1:
            combinations.append([short_phenotype_length, long_phenotype_length - short_phenotype_length])

combinations = numpy.array(combinations)

clusters = KMeans(n_clusters=NUMBER_OF_CLUSTERS).fit_predict(combinations)

plt.scatter(combinations[:, 0], combinations[:, 1], c=clusters)
plt.show()
