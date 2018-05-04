def get_valid_individuals(population):
    return [i for i in population if not i.invalid]
