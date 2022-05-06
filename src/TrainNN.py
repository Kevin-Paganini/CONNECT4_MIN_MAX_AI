def main():
    pass





import csv
import numpy as np

from NeuralNetwork import NNProblem, NeuralNetwork




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













if __name__ == '__main__':
    main()