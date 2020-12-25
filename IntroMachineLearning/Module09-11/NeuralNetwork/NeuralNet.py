from random import random
import math
import yaml

from preprocess_datafile import preprocess
from utils import *


def discretize_result(dataset):
    """
    Convert result to integer value and return key

    :param dataset: the dataset to convert the results
    :return: the key to convert from integer to class value
    """
    result_col = len(dataset[0]) - 1

    # get the unique class values
    class_values = [row[result_col] for row in dataset]
    unique = set(class_values)

    # convert result values to discretized values
    lookup = {}
    for i, value in enumerate(unique):
        lookup[value] = i
    for row in dataset:
        row[result_col] = lookup[row[result_col]]

    # get the key to convert discretized values back to class values
    class_key = dict()
    for key, val in lookup.items():
        class_key[val] = key
    write_output(outputfile, f'class key: {class_key}')
    return class_key


def apply_class_key(dataset, class_key):
    """
    Convert discretized result column back to class values

    :param dataset: the dataset to convert
    :param class_key: the key to convert from discretized values to class values
    :return: the converted dataset
    """
    result_col = len(dataset[0]) - 1

    # create key to convert the discretized result column
    lookup = {}
    for key, val in class_key.items():
        lookup[val] = key

    # convert the discretized result column
    for row in dataset:
        row[result_col] = lookup[row[result_col]]
    return dataset


def normalize_regression_results(dataset):
    """
    Normalize the result column for a regression dataset

    :param dataset: the dataset to normalize
    :return: the dataset with the normalized result column
    """
    result_col = len(dataset[0]) - 1

    # get the range of the dataset
    min_val = float('inf')
    max_val = float('-inf')
    for row in dataset:
        if row[result_col] < min_val:
            min_val = row[result_col]
        elif row[result_col] > max_val:
            max_val = row[result_col]
    range = max_val - min_val

    # normalize the result column of the dataset within the calculated range
    for row in dataset:
        row[result_col] = (row[result_col] - min_val) / range
    return [min_val, max_val]


def apply_regression_range(dataset, regression_range):
    """
    Extrapolate normalized result column to regression range (de-normalize)

    :param dataset: the dataset to de-normalize
    :param regression_range: the range of the result column
    :return: the de-normalized result column
    """

    result_col = len(dataset[0]) - 1

    # get the min, max and range values from the regression range
    min_val = regression_range[0]
    max_val = regression_range[1]
    range = max_val - min_val

    # de-normalize the result column
    for row in dataset:
        row[result_col] = (row[result_col] - min_val) / range
    return dataset


def classification_accuracy(actual, predicted):
    """
    Compute the number of incorrect classification instances as a percentage

    :param actual: the actual classification value list
    :param predicted: the predicted classification value list
    :return: the number of incorrect classifications as a percentage
    """
    incorrect = 0

    # count the number of incorrect cases
    for i in range(len(actual)):
        if actual[i] != predicted[i]:
            incorrect += 1

    # return the number incorrect as a percentage of total cases
    return incorrect / float(len(actual)) * 100.0


def mse_accuracy(actual, predicted, regression_range):
    """
    Compute the mean squared error between predicted and actual cases

    :param actual: the actual regression value list
    :param predicted: the predicted regression value list
    :param regression_range: the range of the regression result column
    :return: the mean squared error between the predicted and actual result sets
    """
    mse = 0

    # compute mse for each of the predictions
    for i in range(len(actual)):
        # extrapolate predicted and actual values to de-normalized values
        delta = regression_range[1] - regression_range[0]
        actual_val = actual[i] * delta + regression_range[0]
        predicted_val = predicted[i][0] * delta + regression_range[0]

        # sum the mean squared error
        mse += (actual_val - predicted_val) ** 2
    return mse


def neuron_sigmoid_value(weights, inputs):
    """
    Compute the sigmoid activation of a neuron

    :param weights: the weight values for the neuron
    :param inputs: the input values from the previous layer
    :return: the sigmoid activation of the neuron
    """

    # initialize the activation to the bias value
    bias = weights[-1]
    activation = bias

    # add the activation values for each weight/input combination
    for i in range(len(weights) - 1):
        activation += weights[i] * inputs[i]

    if verbose:
        write_output(outputfile, f'node activation value: {activation}')
        write_output(outputfile, f'node sigmoid value: {1.0 / (1.0 + math.exp(-activation))}')

    # return the sigmoid activation of the neuron
    return 1.0 / (1.0 + math.exp(-activation))


def forward_propagate(network, inputs):
    """
    propagate inputs through the trained network and show steps
    This method is functionally the same as forward_propagate() above

    :param network: the network to propoaate
    :param row: the row of input values
    :return: the values of the output layer
    """

    if verbose:
        write_output(outputfile, 'Forward propogation example: ')

    # propagate through each layer
    for layer_num, layer in enumerate(network):
        layer_output = []

        if verbose:
            write_output(outputfile, f'layer {layer_num} inputs: {inputs}')

        # get the output for each neuron in the layer
        for neuron in layer:
            neuron['output'] = neuron_sigmoid_value(neuron['weights'], inputs)
            layer_output.append(neuron['output'])

        if verbose:
            write_output(outputfile, f'layer {layer_num} outputs: {layer_output}')

        inputs = layer_output

    # return the outputs for the final layer
    return inputs


def backward_propagate_error(network, actual):
    """
    Backpropagate error through the network

    :param network: the network to propagate the error through
    :param actual: the actual value
    :return:
    """

    if verbose:
        write_output(outputfile, 'Gradient calculation example: ')

    # iterate over each layer in the network in reverse order
    for layer_num in reversed(range(len(network))):
        layer = network[layer_num]
        errors = []

        # propagate error from a hidden layer
        if layer_num != len(network) - 1:
            for neuron_index in range(len(layer)):
                error = 0.0
                # propagate the error delta
                for neuron in network[layer_num + 1]:
                    error += (neuron['weights'][neuron_index] * neuron['delta'])
                errors.append(error)

        # propagate error from the result layer
        else:
            for neuron_index in range(len(layer)):
                neuron = layer[neuron_index]
                errors.append(actual[neuron_index] - neuron['output'])

        # propagate the error based on the derivative of the sigmoid function
        for neuron_index in range(len(layer)):
            neuron = layer[neuron_index]
            neuron['delta'] = errors[neuron_index] * neuron['output'] * (1 - neuron['output'])

            if verbose:
                write_output(outputfile, f'the error for node {neuron_index} in layer {layer_num} is {errors[neuron_index]}, which correspondes to a gradient of {neuron["delta"]}')


def update_weights(network, row, l_rate):
    """
    Update the weights for the whole network

    :param network: the network to update the weights values of
    :param row: the result row
    :param l_rate: the specified learning rate
    """

    if verbose:
        write_output(outputfile, 'Weight update example: ')

    # iterate over each layer in the network
    for layer_num in range(len(network)):

        # get the expected value for the layer
        inputs = row[:-1]
        if layer_num != 0:
            inputs = [neuron['output'] for neuron in network[layer_num - 1]]
        for neuron in network[layer_num]:
            for input_index in range(len(inputs)):

                if verbose:
                    write_output(outputfile, f'update neuron {input_index} in layer {layer_num} weight from  {neuron["weights"][input_index]} by value of {l_rate * neuron["delta"] * inputs[input_index]}')

                # update the neuron weights by the delta values
                neuron['weights'][input_index] += l_rate * neuron['delta'] * inputs[input_index]

                if verbose:
                    write_output(outputfile, f'new weight value is {neuron["weights"][input_index]}')
            # update the neuron bias by the delta value
            neuron['weights'][-1] += l_rate * neuron['delta']


def train_network(network, train, l_rate, n_epoch, n_outputs, class_key):
    """
    Train a network based on parameters

    :param network: the network to train
    :param train: the training set
    :param l_rate: the learning rate
    :param n_epoch: the number of times to iterate over the training data
    :param n_outputs: the number of output nodes
    :param class_key: a key used to determine if we have regression or classification
    """
    # handle classification training
    if class_key:
        for epoch in range(n_epoch+1):
            sum_error = 0
            # iterate over each training case
            for row in train:
                # compute the prediced output of the network
                outputs = forward_propagate(network, row)

                # get the expected output of the network
                expected = [0 for i in range(n_outputs)]
                expected[row[-1]] = 1

                # propagate the error and update the network
                backward_propagate_error(network, expected)
                update_weights(network, row, l_rate)

                # compute the error of the network
                sum_error += sum(abs(outputs[i] - expected[i]) for i in range(len(outputs)))

            if epoch % 100 == 0 or verbose:
                write_output(outputfile, f'epoch: {epoch}, lrate: {l_rate:.3f}, error: {sum_error:.8f}')

    # handle regression training
    else:
        for epoch in range(n_epoch+1):
            sum_error = 0
            # iterate over each training case
            for row in train:
                # compute the predicted output of the network
                output = forward_propagate(network, row)

                # get the expected output for the network
                expected = [row[-1] for i in range(n_outputs)]

                # propagate the error and update the network
                backward_propagate_error(network, expected)
                update_weights(network, row, l_rate)

            # compute the mse of the network
            sum_error = sum([(expected[i] - output[i]) ** 2 for i in range(len(expected))])

            if epoch % 100 == 0 or verbose:
                write_output(outputfile, f'epoch: {epoch}, lrate: {l_rate:.3f}, error: {sum_error:.8f}')


def initialize_network(n_inputs, n_layers, n_hidden, n_outputs):
    """
    Initialize a network with random weights values

    :param n_inputs: the number of input nodes
    :param n_layers: the number of layers
    :param n_hidden: the number of hidden nodes per layer
    :param n_outputs: the number of output nodes
    :return: the initialized network
    """

    # initialize an empty network
    network = []

    # create a network with 0 hidden layers
    if n_layers == 0:
        # initialize layer with random weights
        output_layer = [{'weights': [random() for _ in range(n_inputs + 1)]} for _ in range(n_outputs)]
        network.append(output_layer)

    # create a network with 1 hidden layers
    elif n_layers == 1:
        # initialize layers with random weights
        hidden_layer = [{'weights': [random() for _ in range(n_inputs + 1)]} for _ in range(n_hidden[0])]
        network.append(hidden_layer)
        output_layer = [{'weights': [random() for _ in range(n_hidden[0] + 1)]} for _ in range(n_outputs)]
        network.append(output_layer)

    # create a network with 2 hidden layers
    elif n_layers == 2:
        # initialize layers with random weights
        hidden_layer = [{'weights': [random() for _ in range(n_inputs + 1)]} for _ in range(n_hidden[0])]
        network.append(hidden_layer)
        hidden_layer2 = [{'weights': [random() for _ in range(n_hidden[0] + 1)]} for _ in range(n_hidden[1])]
        network.append(hidden_layer2)
        output_layer = [{'weights': [random() for _ in range(n_hidden[1] + 1)]} for _ in range(n_outputs)]
        network.append(output_layer)

    # handle if there are more than 2 hidden layers specified
    else:
        raise RuntimeException('Number of layers must be in [0, 1, 2]')

    # output_network(network)

    return network


def output_network(network):
    """
    Helper function to output human readable network

    :param network: the network to output
    """

    # get some network metadata (number of hidden layers, inputs, and outputs
    n_layers = len(network) - 1
    n_inputs = len(network[0][0]['weights']) - 1
    n_outputs = len(network[-1])

    # get the number of hidden nodes in each hidden layer
    n_hidden = []
    for layer in network[:-1]:
        n_hidden.append(len(layer))

    # output the network
    write_output(outputfile, f'the trained network:')
    write_output(outputfile, f'there are a total of {n_layers} hidden layers')
    write_output(outputfile, f'there are {n_inputs} inputs')
    if n_layers > 0:
        write_output(outputfile, f'there are {n_hidden[0]} nodes in the 1st hidden layer')
    if n_layers > 1:
        write_output(outputfile, f'there are {n_hidden[1]} nodes in the 2nd hidden layer')
    write_output(outputfile, f'there are {n_outputs} nodes in the output layer')
    for layer_num, layer in enumerate(network):
        if layer_num < n_layers:
            write_output(outputfile, f'layer {layer_num}: {layer}')
        else:
            write_output(outputfile, f'output layer: {layer}')
        for node_num, node in enumerate(layer):
            write_output(outputfile, f'node #{node_num}: {node}')


def predict(network, inputs, class_key):
    """
    Return the prediction of a network

    :param network: the network to make the prediction
    :param row: the input values to predict
    :param class_key: a key used to determine if we have regression or classification
    :return: the predicted output
    """
    outputs = forward_propagate(network, inputs)
    if class_key:
        return outputs.index(max(outputs))
    else:
        return outputs


def back_propagation(train, test, l_rate, n_epoch, n_layers, n_hidden, class_key):
    """
    Train a network and return predicted values using back propogation

    :param train: the training set
    :param test: the testing set
    :param l_rate: the learning rate
    :param n_epoch: the number of times to iterate over the training data
    :param n_layers: the number of hidden layers
    :param n_hidden: the number of hidden nodes per hidden layer
    :param class_key: the translation from discretized class values to class name
    :return: the predictions from the trained network
    """

    # get the number of inputs in the training data
    n_inputs = len(train[0]) - 1

    # initialize the number of outputs to the number of classes, or 1 for regression
    if class_key:
        n_outputs = len(set([row[-1] for row in train]))
    else:
        n_outputs = 1

    # initialize the network to train
    network = initialize_network(n_inputs, n_layers, n_hidden, n_outputs)

    # train the network
    train_network(network, train, l_rate, n_epoch, n_outputs, class_key)

    output_network(network)

    # predict the result based on the trained network
    predictions = []
    for row in test:
        prediction = predict(network, row, class_key)
        predictions.append(prediction)
    return predictions


def tune(train_set, tune_set, n_layers, class_key, regression_range):
    """
    Tune the hyperparameters for back propogation

    :param train_set: the training set
    :param tune_set: the tuning set
    :param n_layers: the number of hidden layers
    :param class_key: the translation from discretized class values to class name
    :param regression_range: the range of the regression results
    :return:
    """

    # specify the range of tuning parameters
    # l_rate_range = [0.01, 0.1, 0.3, 1, 10]
    # n_epoch_range = [500, 300, 200]
    l_rate_range = [10, 0.5, 0.1]
    n_epoch_range = [500, 300]
    n_hidden_val_range = [5, 9]

    # initialize best loss to very bad
    best_loss = float('inf')

    # create a grid search over the number of hidden nodes depending on the number of hidden layers
    n_hidden_vals = []
    if n_layers == 0:  # 0 hidden layers
        n_hidden_vals.append([])
    elif n_layers == 1:  # 1 hidden layer
        for n0 in n_hidden_val_range:
            n_hidden_vals.append([n0])
    elif n_layers == 2:  # 2 hidden layers
        num_hidden = [None] * n_layers
        for n1 in n_hidden_val_range:
            num_hidden[0] = n1
            for n2 in n_hidden_val_range:
                num_hidden[1] = n2
                n_hidden_vals.append(num_hidden.copy())

    # create a grid search over all tunable parameters
    for l_rate in l_rate_range:
        for n_epoch in n_epoch_range:
            for n_hidden in n_hidden_vals:
                write_output(outputfile, f'l_rate: {l_rate}; n_epoch: {n_epoch}, n_hidden: {n_hidden}')

                # evaluate the loss of the tuning parameters
                loss = evaulate_back_prop(train_set, tune_set, l_rate, n_epoch, n_layers, n_hidden, class_key, regression_range)

                # find the best tuning parameters based off lowest loss
                if loss < best_loss:
                    best_loss = loss
                    best_l_rate = l_rate
                    best_n_epoch = n_epoch
                    best_n_hidden = n_hidden

    # return the best values for the tuning parameters
    write_output(outputfile, f'The tuned model looks like: l_rate: {best_l_rate}; n_epoch: {best_n_epoch}, n_hidden: {best_n_hidden}')
    write_output(outputfile, f'The model has a loss of {best_loss}')
    return best_l_rate, best_n_epoch, best_n_hidden


def evaulate_back_prop(train_set, test_set, l_rate, n_epoch, n_layers, n_hidden, class_key, regression_range):
    """
    Compute the error for the trained network

    :param train_set: the training set
    :param test_set: the test set
    :param l_rate: the learning rate
    :param n_epoch: the number of times to iterate over the training data
    :param n_layers: the number of hidden layers
    :param n_hidden: the number of hidden nodes for each hidden layer
    :param class_key: the translation from discretized class values to class name
    :param regression_range: the range of the regression results
    :return:
    """

    # get the predicted and actual results
    predicted = back_propagation(train_set, test_set, l_rate, n_epoch, n_layers, n_hidden, class_key)
    actual = [row[-1] for row in test_set]

    # write_output(outputfile, f'predicted: {predicted}')
    # write_output(outputfile, f'actual: {actual}')

    # iterate over each prediction
    for index, instance in enumerate(predicted):

        # output predicted and actual class
        if class_key:
            write_output(outputfile, 
                f'predicted: {class_key[predicted[index]]}; actual: {class_key[actual[index]]}')
        # output predicted and actual value
        else:
            range = regression_range[1] - regression_range[0]
            write_output(outputfile, 
                f'predicted: {predicted[index][0] * range + regression_range[0]}; actual: {actual[index] * range + regression_range[0]}')

    # compute the classification loss
    if class_key:
        loss = classification_accuracy(actual, predicted)
    # compute the mean squared error for regression
    else:
        loss = mse_accuracy(actual, predicted, regression_range)
    return loss


def main():

    # get the preprocessed dataframe
    df = preprocess(datafile, optionsfile, outputfile)

    # convert dataframe to list of lists
    dataset = df.values.tolist()

    # determine whether classification or regression and store keys
    if dict(df.dtypes)['result'] not in ['int64', 'float64'] or df["result"].nunique() < 10:
        write_output(outputfile, "This is a classification set")
        class_key = discretize_result(dataset)
        regression_range = False
    else:
        write_output(outputfile, "This is a regression set")
        class_key = False
        regression_range = normalize_regression_results(dataset)

    write_output(outputfile, 'the dataset is: ')
    for row in dataset:
        write_output(outputfile, row)

    # split out the tuning dataset from the main dataset
    df, tune_set = split_tune_df(df)
    write_output(outputfile, f'the tuning data set:\n {tune_set}')

    # process the tuning set
    tune_set = tune_set.values.tolist()
    if class_key:
        tune_set = apply_class_key(tune_set, class_key)
    else:
        tune_set = apply_regression_range(tune_set, regression_range)

    scores = []

    # split the remaining data into 5 groups for 5-fold cross validation
    group1, group2, group3, group4, group5 = split_5_fold_cross_validation(df)
    write_output(outputfile, f'group 1:\n{group1}')
    write_output(outputfile, f'group 2:\n{group2}')
    write_output(outputfile, f'group 3:\n{group3}')
    write_output(outputfile, f'group 4:\n{group4}')
    write_output(outputfile, f'group 5:\n{group5}')
    groups = [group1, group2, group3, group4, group5]

    # cross validate each of the 5 sets
    for index, group in enumerate(groups):
        groups_copy = groups.copy()
        test_set = groups_copy.pop(index)
        train_set = pd.concat(groups_copy, axis=0)
        train_set = train_set.reset_index()
        del train_set['index']

        # process the training and test set
        test_set = test_set.values.tolist()
        train_set = train_set.values.tolist()
        if class_key:
            train_set = apply_class_key(train_set, class_key)
            test_set = apply_class_key(test_set, class_key)
        else:
            train_set = apply_regression_range(train_set, regression_range)
            test_set = apply_regression_range(test_set, regression_range)

        # tune the hyperparameters
        l_rate, n_epoch, n_hidden = tune(train_set, tune_set, n_layers, class_key, regression_range)

        # evaluate loss and save to list for each cross validation fold
        loss = evaulate_back_prop(train_set, test_set, l_rate, n_epoch, n_layers, n_hidden, class_key, regression_range)
        scores.append(loss)

    # output the results of the 5 cross fold validation
    write_output(outputfile, f'The set was {data_set}')
    write_output(outputfile, 'Error by fold: %s' % scores)
    if class_key:
        write_output(outputfile, f'% Incorrect: {(sum(scores) / float(len(scores))):.3f}%')
    else:
        write_output(outputfile, f'Total MSE: {sum(scores)}')

if __name__ == '__main__':

    # initialize some options based on the selected set
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    data_set = config['set']
    verbose = config['verbose']
    n_layers = config['layers']
    datafile = f'DataSets/{data_set}.data'
    optionsfile = f'DataSets/{data_set}.options.yaml'
    outputfile = f'output/{data_set}_{n_layers}_hiddenlayers.output.txt'

    # clear the contents of the outputfile
    open(outputfile, 'w').close()

    main()
