import turtle

def draw_phenotype(phenotype):
    for idx, move in enumerate(phenotype):
        if move == 'F':
            turtle.forward(100)
        elif move == 'B':
            turtle.backward(100)
        elif move == '+':
            turtle.left(90)
        elif move == '-':
            turtle.right(90)
    turtle.getscreen().getcanvas().postscript(file='phenotype'+str(idx)+'.eps')
    turtle.clear()

MAX_PHENOTYPE_LENGTH = 20

phenotypes = []

with open('/Users/utku/src/python/PonyGE2/results/TA3E3.WPA.Dal.Ca_18_4_27_173120_704234_35698_704234/phenotypes.txt') as file:
    phenotypes.append(file.readline().rstrip())
    shortest_phenotype = phenotypes[0]

    for line in file:
        line = line.rstrip()
        if len(phenotypes) < MAX_PHENOTYPE_LENGTH:
            phenotypes.append(line)
        else:
            if len(shortest_phenotype) < len(line):
                phenotypes.remove(shortest_phenotype)
                phenotypes.append(line)
        shortest_phenotype = min(phenotypes, key=len)

print(phenotypes)

draw_phenotype(phenotypes[0])
draw_phenotype(phenotypes[1])

# for phenotype in phenotypes:
#     draw_phenotype(phenotype)
