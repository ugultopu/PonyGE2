import turtle

FILE_PATH = '/Users/utku/src/python/PonyGE2/results/TA3E3.WPA.Dal.Ca_18_5_5_190218_71581_10883_71581/cluster_center_phenotypes.txt'
NUMBER_OF_CLUSTERS = 5
EVERY_Nth_GENERATION = 10

def draw_phenotypes(cluster_idx, phenotype_list):
    turtle.reset()
    for phenotype in phenotype_list:
        turtle.penup()
        turtle.home()
        turtle.pendown()
        for move in phenotype:
            if move == 'F':
                turtle.forward(100)
            elif move == 'B':
                turtle.backward(100)
            elif move == '+':
                turtle.left(90)
            elif move == '-':
                turtle.right(90)
    turtle.getscreen().getcanvas().postscript(file='phenotype_'+str(cluster_idx)+'.eps')

with open(FILE_PATH) as f:
    phenotypes = f.read().splitlines()

# Times 2, because we save two phenotypes for every cluster.
phenotypes_for_clusters = [ phenotypes[2*n::2*NUMBER_OF_CLUSTERS][::EVERY_Nth_GENERATION] for n in range(NUMBER_OF_CLUSTERS) ]

for cluster_idx, phenotype_list in enumerate(phenotypes_for_clusters):
    draw_phenotypes(cluster_idx, phenotype_list)
