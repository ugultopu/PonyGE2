import itertools

with open('test.txt') as file:
  phenotypes = file.read().splitlines()

# print(phenotypes)

combinations = itertools.combinations(phenotypes, 2)

# print(list(combinations))

for combo in combinations:
    if len(combo[0]) < len(combo[1]):
        shorter_phenotype = combo[0]
        longer_phenotype = combo[1]
    else:
        shorter_phenotype = combo[1]
        longer_phenotype = combo[0]

    print(shorter_phenotype)
    print(longer_phenotype)
