import numpy as np
import operator as op
import math
import random

class Solution(object) :
    def __init__(self, dim) :
        self.dim = dim
        self.f = 1e10
        self.x = np.zeros(dim)

    def randomize(self, minimum, maximum) :
        arr = [(maximum[i] - minimum[i]) * random.random() + minimum[i] for i in range(len(minimum))]
        self.x = np.array(arr)

    def mutate(self):
        ind = random.randint(0, self.dim - 1)
        self.x[ind] += self.x[ind] * random.random()

    def __repr__(self) :
        return "f(x)=%s x=%s" % (str(self.f), str(self.x))

class GenAlgo(object) :
    def __init__(self, dim, n_pop, n_parent, n_child) :
        np.random.seed(2)
        random.seed(2)
        self.dim = dim
        self.n_pop = n_pop
        self.n_parent = n_parent
        self.n_child = n_child
        self.pop = [Solution(dim) for i in range(n_pop)]

    def select_parents(self) :
        np.random.shuffle(self.pop)
        return self.pop[:self.n_parent]

    def crossover(self, parents) :
        barycenter = sum(parents[i].x for i in range(self.n_parent)) * (1.0 / self.n_parent)
        children = [Solution(self.dim) for i in range(self.n_child)]
        for i in range(self.n_child) :
            eps = np.random.normal(0, np.sqrt(1.0 / (self.n_parent - 1.0)), self.n_parent)
            sum_ = 0
            for j in range(self.n_parent):
                m = eps[j] * (parents[j].x - barycenter)
                sum_ += m
            children[i].x = barycenter + sum_
        return children

    def survival_selection(self, children) :
        children.sort(key=op.attrgetter('f'))
        self.pop[:self.n_parent] = children[:self.n_parent]

    def iterate(self, f) :
        parents = self.select_parents()
        for parent in parents:
            if random.random() < 0.02:
                parent.mutate()
        children = self.crossover(parents)
        for i in range(self.n_child) :
            children[i].f = f(children[i].x)
        self.survival_selection(children)

    def execute(self, minimum, maximum, f, threshold, tol, max_evals) :
        for i in range(self.n_pop) :
            self.pop[i].randomize(minimum, maximum)
            self.pop[i].f = f(self.pop[i].x)
        n_evals = self.n_pop
        last_sol = None
        while n_evals < max_evals:
            self.iterate(f)
            n_evals += self.n_child
            best_sol = min(self.pop, key=lambda sol : sol.f)
            if best_sol.f < threshold:
                break
            last_sol = best_sol
        return best_sol
