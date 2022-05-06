import csv

import numpy as np

from NeuralNetwork import NNProblem

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


def test_connect4_network():
    x, y = load_boards_targets_txt("boards_and_targets.txt")
    test_GA(x, y, True)

    
    # layers = [9, 4, 1]
    # problem = NNProblem(x,y,layers)
    # nn = NeuralNetwork(problem._layer_size,load_4_layer_ttt_network())
    # a = accuracy(x, y,nn)
    # print("Testing Tic Tac Toe Network")
    
    # print("Accuracy ", a)


def load_4_layer_ttt_network():
    W = []
    weights_2 = np.array([[-0.00142707, -0.08451622, -0.00777166, 0.07153606],
        [-3.12064667, -0.62044264, -3.18868069, -1.06183619],
        [-2.75995675, -0.3063746, -3.24168826, -0.7056788],
        [0.35471861, -1.40337629, 0.3368032, 1.96311844],
        [0.31900681, -0.98534514, 0.36569296, 1.7516015],
        [1.18823403, -0.88661356, 1.42729163, 2.3146592],
        [2.24817726, -0.73170809, 2.42017968, 3.13494424],
        [2.43338048, -1.12167492, 2.78634464, 3.30680788],
        [1.57132788, -1.4313579, 1.66389342, 2.45366816],
        [1.4126572, -1.38204671, 1.45066697, 2.78777504]])
    weights_3 = np.array([[0.03276832],
        [6.10550764],
        [2.6696074],
        [6.58122877],
        [-5.46573692]])
    W.append(weights_2)
    W.append(weights_3)
    return W







def main():
    
    test_connect4_network()

if __name__ == '__main__':
    main()