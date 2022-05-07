import csv

import numpy as np

from NeuralNetwork import NNProblem




def test_GA(x, y, verbose = True):  #[[outputs]] or [outputs]
    FILE_COUNTER = 0
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
        examine_best(problem, ans, FILE_COUNTER)
        FILE_COUNTER += 1
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

def examine_best(problem, best, FILE_COUNTER):
    file_name = f'best_weights_2_{FILE_COUNTER}.npy'
    
    print("Final fitness")
    print(problem.evaluate(best))
    
    print("Best weights ")
    with open(file_name, 'wb') as f:
        np.save(f, best._W)
    
            
            
        
    for w in best._W:
        print(w)

def load_boards_targets_txt(filepath):
    """
        Loads the .csv file and parses each lines.
        Each line represents the input to the network and
        the expected output/target.
        To parse, 'x' corresponds to a 1 and each 'o' corresponds to a 0.
        Cwin corresponds to 1 and Xwin corresponds to 0.
        :param filepath: .cvs file
        :return: x and y for inputs targets
        """
    data = csv.reader(open(filepath), delimiter=",")
    data = np.array(list(data))
    x = []
    y = []
    for line in data:
        line = [int(x) for x in line]
        x.append(line[0:-1])
        y.append([line[-1]])
    x = np.array(x)
    y = np.array(y)
    return x, y

def accuracy(x, y, nn):
    thres = 0.1

    out = []
    for i in range(x.shape[0]):
        out.append(nn.step(x[i]))
    matches = [1 for i in range(len(y)) if abs(y[i] - out[i]) < thres]
    return len(matches) / np.shape(y)[0]


def train_connect4_network():
    x, y = load_boards_targets_txt("boards_and_targets.txt")
    test_GA(x, y, True)

def main():
    
    train_connect4_network()

if __name__ == '__main__':
    
    main()