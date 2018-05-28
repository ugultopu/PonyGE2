import turtle

def draw_phenotype(phenotype):
    turtle.resetscreen()
    for move in phenotype:
        if move == 'F':
            turtle.forward(2)
        elif move == 'B':
            turtle.backward(2)
        elif move == '+':
            turtle.left(90)
        elif move == '-':
            turtle.right(90)
    turtle.getscreen().getcanvas().postscript(file='phenotype_plot.eps')

phenotype = '+F-+F-FFF+F-F+F-+F-F+F-FF+F-FF+F-FFF+F-FFF+F-FF+F-F+F-FF+F-F+F-FFF+F-FF+F-FF+F-FF+F-FF-+F-FFF+F-FF+F-F+F-FFF+F-+F-++F-FFF+F-FFF+F-+F-FF+F-+F-FF-+F-F+F-FF+F-+F-FFF++F-+F-FF+F-F+F-FFF+F-F+F-FFF+F-FF-+F-FF+F-FF+F-FF+F-++F-FF+F-FF+F-FFF+F-FFF+F-FFF+F-F+F-+F-FF-+F-FFF+F-FFF+F-FF+F-F+F-FF+F-+F-++F-FF+F-FF+F-FF+F-FFF+F-F+F-FFF+F-FF+F-FF+F-+F-FF-+F-+F-F+F-FF+F-FF+F-FF+F-FFF+F-++F-FF+F-F+F-FFF+F-FFF+F-FFF-+F-F+F-FFF+F-+F-FF+F-FF+F-F++F-FFF+F-FFF+F-FF+F-FFF+F-FF+F-+F-F+F-+F-FF+F-F+F-FF+F-F+F-+F-+F--+F-F+F-FFF+F-FF+F-FF+F-F+F-FFF+F-FF++F-+F-FF+F-F+F-F+F-FFF+F-+F-FFF+F-+F-FFF+F-FFF+F--+F-+F-FFF+F-F+F-FFF+F-++F-FFF+F-+F-FFF+F-FF+F-F+F-+F-FFF-+F-F+F-FFF+F-FF+F-F+F-FFF+F-FF+F-FFF++F-F+F-FF+F-FF+F-FFF+F-FFF+F-FFF+F-FFF+F-FFF-+F-F+F-F+F-FF+F-++F-FFF+F-+F-+F-FFF+F-FFF-+F-+F-+F-F+F-FFF+F-FFF+F-FF+F-FF++F-F+F-F+F--+F-FF+F-FFF+F-FFF+F-FF+F--+F-+F-FFF+F-FF+F-FFF+F-++F-F+F-FFF+F-FFF+F-F+F-F++F-FFF+F-FF+F-+F-+F-+F-FF+F-F+F-+F-+F-F'

draw_phenotype(phenotype);
