import itertools

with open('test.txt') as file:
  phenotypes = file.read().splitlines()

# print(phenotypes)

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
        # print('index: ' + str(i))
        # print('first element: ' + str(unit_0))
        # print('second element: ' + str(unit_1))
        if unit_0 != unit_1:
            combinations.append((*combo, i, short_phenotype_length + long_phenotype_length - 2 * i))
            break
        if i == short_phenotype_length - 1:
            combinations.append((*combo, short_phenotype_length, long_phenotype_length - short_phenotype_length))

for combination in combinations:
    print(combination)
