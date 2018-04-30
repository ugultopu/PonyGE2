import itertools

with open('test.txt') as file:
  phenotypes = file.read().splitlines()

# print(phenotypes)

combinations = itertools.combinations(phenotypes, 2)

# print(list(combinations))

for combo in combinations:
    for i, (a, b) in enumerate(zip(combo[0], combo[1])):
        print('index: ' + str(i))
        print('first element: ' + str(a))
        print('second element: ' + str(b))
