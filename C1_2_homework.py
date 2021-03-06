# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import h5py
import scipy
from PIL import Image
from scipy import ndimage
from lr_utils import load_dataset
from scipy.special import expit



epsilon = 1e-5

def initialize_with_zeros(dim):
    '''
    >>> w, b = initialize_with_zeros(2)
    >>> print(w)
    [[0.]
     [0.]]
    >>> print(b)
    0.0
    '''
    w = np.zeros((dim, 1))
    b = 0.0

    assert (w.shape == (dim, 1))
    assert (isinstance(b, float) or isinstance(b, int))

    return w, b

def propagate(w, b, X, Y):
    """

    :param w: weights, a numpy array of size (num_px * num_px * 3, 1)
    :param b: bias, a scalar
    :param X: data of size (num_px * num_px * 3, number of examples)
    :param Y: true "label" vector ( 0 if non-cat, 1 if cat) of size (1, number of examples)

    :return:
    cost: the value of cost function
    grads: {"dw": dw,
            "db": db}

    """
    m = X.shape[1] # number of examples
    Z = np.dot(w.T, X) + b # (1, m)
    A = expit(Z) # (1, m)
    cost = -(1.0 / m) * np.sum(Y * np.log(A+epsilon) + (1-Y) * np.log(1-A+epsilon))

    dZ = A - Y
    dw = (1.0/m)*np.dot(X, dZ.T)
    db = (1.0/m)*np.sum(dZ)

    assert dw.shape == w.shape
    assert db.dtype == float
    cost = np.squeeze(cost)
    assert cost.shape == ()

    grads = {"dw": dw,
             "db": db}

    return grads, cost

def optimize(w, b, X, Y, num_iterations, learning_rate, print_cost=False):
    """
    :param w: weight (m, 1)
    :param b: bias
    :param X:
    :param Y:
    :param num_iterations:
    :param learning_rate:
    :param print_cost:
    :return:
    """
    costs = []
    for i in range(num_iterations):
        grads, cost = propagate(w, b, X, Y)

        dw = grads['dw']
        db = grads['db']

        w = w - learning_rate*dw
        b = b - learning_rate*db

        if i % 100 == 0:
            costs.append(cost)

        if print_cost and i % 100 == 0:
            print("Cost after iteration %i: %f" %(i, float(cost)))

    params = {"w": w,
              "b": b}

    grads = {"dw": dw,
             "db": db}

    return params, grads, costs

def predict(w, b, X):
    m = X.shape[1]
    Y_prediction = np.zeros((1, m))
    w = w.reshape((X.shape[0], 1))

    A = expit(np.dot(w.T, X)+b)

    for i in range(A.shape[1]):
        if A[0,i] > 0.5:
            Y_prediction[0, i] = 1
        else:
            Y_prediction[0, i] = 0

    assert Y_prediction.shape == (1, m)

    return Y_prediction


def model(X_train, Y_train, X_test, Y_test, num_iterations=3000, learning_rate=0.005, print_cost=False):
    w, b = initialize_with_zeros(X_train.shape[0])
    parameters, grads, costs = optimize(w, b, X_train, Y_train, num_iterations, learning_rate=learning_rate, print_cost=print_cost)
    w = parameters['w']
    b = parameters['b']

    Y_prediction_train = predict(w, b, X_train)
    Y_prediction_test = predict(w, b, X_test)

    print('train accuracy: {} %'.format(100 - np.mean(np.abs(Y_prediction_train-Y_train))))
    print('test accuracy: {} %'.format(100 - np.mean(np.abs(Y_prediction_test-Y_test))))

    d = {
        "costs": costs,
        "Y_prediction_test": Y_prediction_test,
        "Y_prediction_train": Y_prediction_train,
        "w": w,
        "b": b,
        "learning_rate": learning_rate,
        "num_iterations": num_iterations
    }

    return d




if __name__ == '__main__':
    # w, b, X, Y = np.array([[1.], [2.]]), 2., np.array([[1., 2., -1.], [3., 4., -3.2]]), np.array([[1, 0, 1]])
    # grads, cost = propagate(w, b, X, Y)
    # print("dw = " + str(grads["dw"]))
    # print("db = " + str(grads["db"]))
    # print("cost = " + str(cost))
    # params, grads, costs = optimize(w, b, X, Y, num_iterations=100, learning_rate=0.009, print_cost=False)
    # print("w = " + str(params["w"]))
    # print("b = " + str(params["b"]))
    # print("dw = " + str(grads["dw"]))
    # print("db = " + str(grads["db"]))
    # w = np.array([[0.1124579], [0.23106775]])
    # b = -0.3
    # X = np.array([[1., -1.1, -3.2], [1.2, 2., 0.1]])
    # print("predictions = " + str(predict(w, b, X)))
    train_set_x_orig, train_set_y, test_set_x_orig, test_set_y, classes = load_dataset()

    # Example of a picture
    # index = 25
    # plt.imshow(train_set_x_orig[index])
    # plt.show()

    # print(train_set_x_orig.shape[0])

    m_train = train_set_x_orig.shape[0]
    m_test = test_set_x_orig.shape[0]
    num_px = train_set_x_orig.shape[1]
    #
    # print("Number of training examples: m_train = " + str(m_train))
    # print("Number of testing examples: m_test = " + str(m_test))
    # print("Height/Width of each image: num_px = " + str(num_px))
    # print("Each image is of size: (" + str(num_px) + ", " + str(num_px) + ", 3)")
    # print("train_set_x shape: " + str(train_set_x_orig.shape))
    # print("train_set_y shape: " + str(train_set_y.shape))
    # print("test_set_x shape: " + str(test_set_x_orig.shape))
    # print("test_set_y shape: " + str(test_set_y.shape))

    train_set_x_flatten = train_set_x_orig.reshape(m_train, -1).T
    test_set_x_flatten = test_set_x_orig.reshape(m_test, -1).T
    # print(train_set_x_flatten)

    train_set_x = train_set_x_flatten / 255
    test_set_x = test_set_x_flatten / 255

    # make ( learning_rate = 0.005 ) model
    # d = model(train_set_x, train_set_y, test_set_x, test_set_y, num_iterations=3000,
    #           learning_rate=0.005, print_cost=True)

    num_iterations = 3000
    learning_rates = [0.01, 0.001, 0.0001]
    models = {}


    plt.figure(figsize=(20,8))

    # make models of different learning rate
    for i in learning_rates:
        print("learning rate is :" + str(i) + ' now')
        models[str(i)] = model(train_set_x, train_set_y, test_set_x, test_set_y, num_iterations=num_iterations,
                               learning_rate=i, print_cost=True)
        print("\n" + "-"*50)

    # record the costs (type: list) of models, turn these to numpy array, and plot these
    for index, i in enumerate(learning_rates):
        costs = models[str(i)]["costs"]
        costs_ = np.squeeze(costs)
        plt.plot(costs_, label="model {} learning rate={}".format(index, str(i)))

    plt.ylabel("cost")
    plt.xlabel("iterations")

    plt.xticks([i for i in range(int(num_iterations/100))])
    plt.legend(loc=0)
    plt.show()