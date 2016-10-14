import operator
import random

import numpy
import apriori

from deap import base
from deap import benchmarks
from deap import creator
from deap import tools

MIN_SUPPORT_THRESHOLD = 0.1
MAX_SUPPORT_THRESHOLD = 0.4
MIN_CONF_THRESHOLD = 0.1
MAX_CONF_THRESHOLD = 0.9

DEFAULT_COVERAGE_THRESHOLD = 5
DEFAULT_TOP_K_RULES = 25

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Particle", list, fitness=creator.FitnessMax, speed=list, 
    smin=None, smax=None, best=None)

def clamp(value, minimum, maximum):
    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value

def my_rule_filter(rule):
    if rule.support >= my_rule_filter.particle[0]:
        return True
    if rule.confidence >= my_rule_filter.particle[1]:
        return True
    return False

def evalAccuracy(particle):
    my_rule_filter.particle = particle
    dataset = apriori.get_dataset_from_file('Itemset_train.txt')
    classes = apriori.get_classes_from_file('Classes_train.txt')
    #dataset, classes = apriori.get_dataset_and_classes("Itemset_train.txt", "Classes_train.txt")
    default_class = apriori.get_default_class(dataset, classes, my_rule_filter)
    accuracy = apriori.test(default_class, DEFAULT_TOP_K_RULES, my_rule_filter)
    return accuracy,

def generate(size, pmin, pmax, smin, smax):
    part = creator.Particle(random.uniform(pmin, pmax) for _ in range(size)) 
    part.speed = [random.uniform(smin, smax) for _ in range(size)]
    part.smin = smin
    part.smax = smax
    return part

def updateParticle(part, best, phi1, phi2):
    u1 = (random.uniform(0, phi1) for _ in range(len(part)))
    u2 = (random.uniform(0, phi2) for _ in range(len(part)))
    v_u1 = map(operator.mul, u1, map(operator.sub, part.best, part))
    v_u2 = map(operator.mul, u2, map(operator.sub, best, part))
    part.speed = list(map(operator.add, part.speed, map(operator.add, v_u1, v_u2)))
    for i, speed in enumerate(part.speed):
        if speed < part.smin:
            part.speed[i] = part.smin
        elif speed > part.smax:
            part.speed[i] = part.smax
    part[:] = list(map(operator.add, part, part.speed))
    part[:] = [clamp(part[0], MIN_SUPPORT_THRESHOLD, MAX_SUPPORT_THRESHOLD),
               clamp(part[1], MIN_CONF_THRESHOLD, MAX_CONF_THRESHOLD)]

toolbox = base.Toolbox()
toolbox.register("particle", generate, size=2, pmin=0, pmax=1, smin=-3, smax=3)
toolbox.register("population", tools.initRepeat, list, toolbox.particle)
toolbox.register("update", updateParticle, phi1=2.0, phi2=2.0)
toolbox.register("evaluate", evalAccuracy)

def main():
    pop = toolbox.population(n=5)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    apriori.learn(MIN_SUPPORT_THRESHOLD, MIN_CONF_THRESHOLD, DEFAULT_COVERAGE_THRESHOLD)

    logbook = tools.Logbook()
    logbook.header = ["gen", "evals"] + stats.fields

    GEN = 20
    best = None

    random.seed(60)

    for g in range(GEN):
        for part in pop:
            part.fitness.values = toolbox.evaluate(part)
            if not part.best or part.best.fitness < part.fitness:
                part.best = creator.Particle(part)
                part.best.fitness.values = part.fitness.values
            if not best or best.fitness < part.fitness:
                best = creator.Particle(part)
                best.fitness.values = part.fitness.values
        for part in pop:
            toolbox.update(part, best)

        # Gather all the fitnesses in one list and print the stats
        logbook.record(gen=g, evals=len(pop), **stats.compile(pop))
        print(logbook.stream)

    return logbook.select("gen", "avg", "min", "max")
    #return pop, logbook, best

if __name__ == "__main__":
    main()
