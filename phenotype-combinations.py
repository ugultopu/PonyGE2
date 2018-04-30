import itertools

phenotypes = []

with open('test.txt') as file:
  phenotypes = file.read().splitlines()

# print(phenotypes)

combinations = itertools.combinations(phenotypes, 2)

print(list(combinations))
