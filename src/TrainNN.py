import csv
import time
import numpy as np

from NeuralNetwork import NNProblem


# Trains neural network

# Trains the neural network
def test_GA(x, y, verbose = True):  #[[outputs]]
    size = 200
    layers = [42, 69, 25, 7]
    pop_size = 100   # 200
    num_epochs = 250  # 200
    mut_rate = 0.001
    elites = 1
    problem = NNProblem(x, y, layers)
    f_name = f'size{size}_{layers}_pop{pop_size}_ep{num_epochs}_mut{mut_rate}_el{elites}'
    print("\nParams: ")
    print(f_name)
    num_restarts = 1
    solve_rate = 0

    x = x[:size]
    y = y[:size]

    for i in range(num_restarts):
        initial = problem.create_population(pop_size)
        ans = train(problem, initial, mut_rate, num_epochs, elites, verbose)
        print("Run ", i)
        examine_best(problem, ans, f_name)
        if problem.solved_problem(ans, 0.99):
            solve_rate += 1
    print("GA run " + str(num_restarts) + " times.")
    print("Number of successes: " + str(solve_rate))


# Actual training of the neural network
def train(problem, initial, mut_rate, epochs = 10, elites = 2, verbose = True):
    population = initial
    total_time = 0
    t_count = 0
    if verbose:
        print("\nStarting GA\n")
    for i in range(epochs):
        start = time.time()
        weights = [problem.evaluate(i) for i in population]

        pairs = [(population[i], weights[i]) for i in range(len(population))]  # sorting based on fitness
        pairs = list(sorted(pairs, key=lambda x: x[1]))
        pairs.reverse()

        new_population = [pairs[i][0] for i in range(elites)]

        while len(new_population) < len(population):
            parent = problem.selection(population, weights, 10)
            child1 = problem.crossover(parent[0], parent[1])
            child1 = problem.mutate(state=child1, rate=mut_rate, mu=0, s=25)
            new_population.append(child1)
        population = new_population
        best = problem.found_solution(population)
        end = time.time()
        total_time += (end-start)
        t_count += 1
        avg_time = total_time / t_count
        if best is not None:
            return best
        if verbose:
            fitness = str(np.max(weights))
            runtime = str(round(end-start, 3)) + "s"
            elapsed = str(round(total_time / 60, 2)) + "m"
            expected = str(round(((epochs-i) * avg_time) / 60, 2)) + "m"
            print("Epoch " + str(i) + " | Fitness: " + fitness + " | Runtime: " + runtime+ " | Total elapsed: " + elapsed + " | Time remaining: " + expected)
    weights = [problem.evaluate(i) for i in population]
    return population[np.argmax(weights)]

# Checks to see the best neural network
def examine_best(problem, best, f_name):
    score = problem.evaluate(best)
    score = round(score, 5)

    #file_name = f'best_weights_2_Aaron_Version_100_0.05_200_{FILE_COUNTER}.npy'
    file_name = f'{f_name}_fit{score}'
    
    print("Final fitness")
    print(score)
    
    print("Best weights ")
    with open(file_name, 'wb') as f:
        np.save(f, best._W)

    for w in best._W:
        print(w)

# Loads inputs and target values
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


# Calculates accuracy score
def accuracy(x, y, nn):
    thres = 0.1

    out = []
    for i in range(x.shape[0]):
        out.append(nn.step(x[i]))
    matches = [1 for i in range(len(y)) if abs(y[i] - out[i]) < thres]
    return len(matches) / np.shape(y)[0]

# Method called by main to start process
def train_connect4_network():
    x, y = load_boards_targets_txt("boards_and_targets.txt")
    test_GA(x[:100], y[:100], True)



if __name__ == '__main__':
    
    train_connect4_network()