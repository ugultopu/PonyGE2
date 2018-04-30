import itertools

with open('test.txt') as file:
  phenotypes = file.read().splitlines()

# print(phenotypes)

combinations = itertools.combinations(phenotypes, 2)

# print(list(combinations))

for combo in combinations:
    for a, b in zip(combo[0], combo[1]):
        print(a)
        print(b)
