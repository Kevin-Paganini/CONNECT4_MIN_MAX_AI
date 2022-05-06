import numpy as np

from NeuralNetwork import NNProblem


def main():
    pass


def test_GA(x, y, verbose = True):
    layers = [42, 20, 7]

    pop_size = 100
    num_epochs = 200
    problem = NNProblem(x, y, layers)

    num_restarts = 5
    solve_rate = 0

    for i in range(num_restarts):
        initial = problem.create_population(pop_size)
        ans = train(problem, initial, num_epochs, verbose)
        print("Run ", i)
        examine_best(problem, ans)
        if problem.solved_problem(ans, 0.99):
            solve_rate += 1
    print("GA run " + str(num_restarts) + " times.")
    print("Number of successes: " + str(solve_rate))

def train(problem, initial, epochs = 10, elites = 2, verbose = True):
    population = initial

    if verbose:
        print("\nStarting GA\n")
    for i in range(epochs):
        weights = [problem.evaluate(i) for i in population]

        pairs = [(population[i], weights[i]) for i in range(len(population))]  # sorting based on fitness
        pairs = list(sorted(pairs, key=lambda x: x[1]))
        pairs.reverse()

        new_population = [pairs[i][0] for i in range(elites)]

        while len(new_population) < len(population):
            parent = problem.selection(population, weights, 2)
            child1 = problem.crossover(parent[0], parent[1])
            child1 = problem.mutate(child1, None, 0, 10)
            new_population.append(child1)
        population = new_population
        best = problem.found_solution(population)
        if best is not None:
            return best
        if verbose:
            print("Epoch " + str(i) + ".Fitness: ", np.max(weights))
    weights = [problem.evaluate(i) for i in population]
    return population[np.argmax(weights)]

def examine_best(problem, best):
    print("Final fitness")
    print(problem.evaluate(best))
    print("Target vs actual:")
    for i in range(len(problem._y)):
        print("\t",problem._y[i], best.step(problem._input[i])[0])
    print("Best weights ")
    for w in best._W:
        print(w)


if __name__ == '__main__':
    main()