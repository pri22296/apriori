import random

import apriori
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

IND_INIT_SIZE = 2
MAX_ITEM = 50
MAX_WEIGHT = 50
NBR_ITEMS = 20

# To assure reproductibility, the RNG seed is set prior to the items
# dict initialization. It is also seeded in main().
random.seed(64)

# Create the item dictionary: item name is an integer, and value is 
# a (weight, value) 2-uple.
items = {}
# Create random items and store them in the items' dictionary.
for i in range(NBR_ITEMS):
    items[i] = (random.randint(1, 10), random.uniform(0, 100))

creator.create("Fitness", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.Fitness)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("attr_item", random.uniform, 0, 1)

def random_support():
    return random.uniform(0.05,0.4)
    
def random_confidence():
    return random.uniform(0.05,0.9)

# Structure initializers
toolbox.register("individual", tools.initCycle, creator.Individual, 
    [random_support, random_confidence])
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalKnapsack(individual):
    weight = 0.0
    value = 0.0
    for item in individual:
        weight += items[item][0]
        value += items[item][1]
    if len(individual) > MAX_ITEM or weight > MAX_WEIGHT:
        return 10000, 0             # Ensure overweighted bags are dominated
    return weight, value
    
def evalAccuracy(individual):
    #print(individual)
    accuracy = apriori.test(apriori.learn(*individual,5), 20)
    #print("accuracy for support_threshold {} is {}".format(sup_th, accuracy))
    return accuracy,

def cxSet(ind1, ind2):
    """Apply a crossover operation on input sets. The first child is the
    intersection of the two sets, the second child is the difference of the
    two sets.
    """
    temp = set(ind1)                # Used in order to keep type
    ind1 &= ind2                    # Intersection (inplace)
    ind2 ^= temp                    # Symmetric Difference (inplace)
    return ind1, ind2
    
def mutSet(individual):
    """Mutation that pops or add an element."""
    if random.random() < 0.5:
        if len(individual) > 0:     # We cannot pop from an empty set
            individual.remove(random.choice(sorted(tuple(individual))))
    else:
        individual.add(random.randrange(NBR_ITEMS))
    return individual,
    
def clamp(value, minimum, maximum):
    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value
    
def decoy_cxSim(ind1, ind2):
    ind1, ind2 = tools.cxBlend(ind1, ind2, 0.5)
    ind1[0], ind2[0] = clamp(ind1[0],0.05,0.4), clamp(ind2[0],0.05,0.4)
    ind1[1], ind2[1] = clamp(ind1[1],0.1,0.9), clamp(ind2[1],0.1,0.9)
    return ind1,ind2
    
def decoy_mutPoly(individual):
    individual, = tools.mutPolynomialBounded(individual, 0, 0.4, 0.95, 0.4)
    individual[0] = clamp(individual[0],0.05,0.4)
    individual[1] = clamp(individual[1],0.05,0.9)
    return individual,

toolbox.register("evaluate", evalAccuracy)
toolbox.register("mate", decoy_cxSim)
toolbox.register("mutate", decoy_mutPoly)
toolbox.register("select", tools.selRoulette)
                 
def main1():
    random.seed(60)

    # create an initial population of 300 individuals (where
    # each individual is a list of integers)
    pop = toolbox.population(n=25)

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    #
    # NGEN  is the number of generations for which the
    #       evolution runs
    CXPB, MUTPB, NGEN = 0.7, 0.2, 10
    
    print("Start of evolution")
    
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    
    print("  Evaluated %i individuals" % len(pop))
    
    gen_list, avg_list, min_list, max_list = [], [], [], []
    
    
    # Begin the evolution
    for g in range(NGEN):
        print("-- Generation %i --" % g)
        
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
    
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                #print(child1, child2)
                toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
    
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        print("  Evaluated %i individuals" % len(invalid_ind))
        
        # The population is entirely replaced by the offspring
        pop[:] = offspring
        
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        
        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)

        gen_list.append(g)
        avg_list.append(mean)
        min_list.append(min(fits))
        max_list.append(max(fits))        
        
    
    print("-- End of (successful) evolution --")
    
    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    
    return gen_list, avg_list, min_list, max_list
    
def main2():
    NGEN = 10
    MU = 25
    LAMBDA = 25
    CXPB = 0.7
    MUTPB = 0.2
    
    random.seed(60)
    
    pop = toolbox.population(n=MU)
    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)
    
    result = algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats,
                              halloffame=hof)
    
    
    best_ind = tools.selBest(pop, 1)[0]

    logbook = result[1]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    return logbook.select("gen", "avg", "min", "max")

if __name__ == "__main__":
    main1()
