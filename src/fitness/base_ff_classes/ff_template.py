from fitness.base_ff_classes.base_ff import base_ff


class ff_template(base_ff):
    """
    Basic fitness function template for writing new fitness functions. This
    basic template inherits from the base fitness function class,
    which contains various checks and balances.
    
    Important points to note about base fitness function class:
      - Default Fitness values (can be referenced as "self.default_fitness")
        are set to NaN in the base class. While this can be over-written,
        PonyGE2 works best when it can filter solutions by NaN values.
      - The standard fitness objective of the base fitness function class is
        to minimise fitness. If the objective is to maximise fitness,
        this can be over-written by setting the flag "maximise = True".
    """

    def __init__(self):
        """
        All fitness functions which inherit from the bass fitness function
        class must initialise the base class during their own initialisation.
        """
        
        # Initialise base fitness function class.
        super().__init__()
    
    def evaluate(self, ind, **kwargs):
        """
        Default fitness execution call for all fitness functions. When
        implementing a new fitness function, this is where code should be added
        to evaluate target phenotypes.
        
        There is no need to implement a __call__() method for new fitness
        functions which inherit from the base class; the "evaluate()" function
        provided here allows for this. Implementing a __call__() method for new
        fitness functions will over-write the __call__() method in the base
        class, removing much of the functionality and use of the base class.
                
        :param ind: An individual to be evaluated.
        :param kwargs: Optional extra arguments.
        :return: The fitness of the evaluated individual.
        """
        
        # Evaluate the fitness of the phenotype
        fitness = eval(ind.phenotype)
        
        return fitness