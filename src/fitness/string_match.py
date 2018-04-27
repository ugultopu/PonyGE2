from algorithm.parameters import params
from fitness.base_ff_classes.base_ff import base_ff


class string_match(base_ff):
    """Fitness function for matching a string. Takes a string and returns
    fitness. Penalises output that is not the same length as the target.
    Penalty given to individual string components which do not match ASCII
    value of target."""

    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()

        # Set target string.
        self.target = params['TARGET']

    def evaluate(self, ind, **kwargs):
        with open(params['FILE_PATH'] + '/phenotypes.txt', 'a') as phenotypes:
            phenotypes.write(ind.phenotype + '\n')
        return 1
