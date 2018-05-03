import numpy
import random
import datetime
import itertools
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

NUMBER_OF_CLUSTERS = 5

with open('/Users/utku/src/python/PonyGE2/results/Utkus-MacBook-Air.local_18_5_1_220720_849389_48679_849389/phenotypes-summary.txt') as file:
  phenotypes = file.read().splitlines()

differences_in_combinations = []

combinations = itertools.combinations(phenotypes, 2)

for combo in combinations:
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

for _ in range(params['GENERATION_SIZE'] / 2):
    parents.append(*combinations[random.choice(partitioned_clusters[random.randrange(0, NUMBER_OF_CLUSTERS)])])

return parents

print('cluster_0_indices are:', cluster_0_indices)

print('type(clusters) are', type(clusters))
print('clusters are', clusters)

print('Computed which cluster would each point belong to')
print(datetime.datetime.now())

print('Finished the program')
print(datetime.datetime.now())

plt.scatter(differences_in_combinations[:, 0], differences_in_combinations[:, 1], c=clusters)
plt.show()
