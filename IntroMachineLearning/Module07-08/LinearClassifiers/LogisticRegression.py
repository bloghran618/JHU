import yaml

from preprocess_datafile import preprocess
from utils import *


def sigmoid(z):
    """
    return the sigmoid of the prediction

    :param z: the value to get the sigmoid of
    :return: the sigmoid
    """
    return 1 / (1 + np.exp(-z))


def cross_entropy_loss(theta, x, y):
    """
    Determine the cross entropy loss for a model

    :param theta: the model to test
    :param x: the independant variable data
    :param y: the dependant variable data
    :return:
    """
    h = sigmoid(x @ theta)
    cost = 1 / len(y) * np.sum(-y * np.log(h) - (1 - y) * np.log(1 - h))
    grad = 1 / len(y) * ((y - h) @ x)
    return cost, grad


def build_model(x, y, epochs, learn_rate):
    """
    Build the weights vectors

    :param x: the independant variable data
    :param y: the dependant variable data
    :param epochs: the number of epochs to iterate over for learning
    :param learn_rate: the learning rate
    :return: the weights vectors for each result class
    """

    # initialize arrays
    x = np.insert(x, 0, 1, axis=1)
    thetas = []
    classes = np.unique(y)
    costs = np.zeros(epochs)

    # iterate over each class in the possible result classes
    for c in classes:
        # initialize model to zeros
        theta = np.zeros(x.shape[1])
        binary_y = np.where(y == c, 1, 0)

        # iterate over a number of epochs
        for epoch in range(epochs):
            # update the model with the gradient
            costs[epoch], grad = cross_entropy_loss(theta, x, binary_y)
            if verbose:
                write_output(outputfile, f'update model {theta} with values: {learn_rate * grad}')
            theta += learn_rate * grad

        thetas.append(theta)
    return thetas


def predict(classes, thetas, x):
    """
    predict the class based on the model and independant variables

    :param classes: the class index to class map
    :param thetas: the models for each class
    :param x: the independant variable data
    :return: the predicted class
    """
    # initialize arrays
    x = np.insert(x, 0, 1, axis=1)
    preds = []

    # iterate over each row in x
    for case in x:
        probs = []
        # iterate over each class model
        for model in thetas:
            poss = sigmoid(case @ model)
            probs.append(poss)

        # choose the class with the highest probability
        write_output(outputfile, f'softmax class probabilities: {probs}')
        preds.append(np.argmax(probs))

    # convert class indexes to class name
    write_output(outputfile, f'preds: {preds}')
    for index, pred in enumerate(preds):
        preds[index] = classes[pred]

    return preds


def classification_loss(classes, theta, x, y):
    """
    Get the classification loss of a subset

    :param classes: the class index to class map
    :param thetas: the models for each class
    :param x: the independant variable data
    :param y: the dependant variable data
    :return: the classification loss
    """
    # initialize loss
    loss = 0

    # make predictions
    predictions = predict(classes, theta, x)

    # check each prediction to see if it matches dependant variable
    for index, pred in enumerate(predictions):
        if pred != y[index]:
            loss += 1
    return loss


def tune_hyperparameters(x, y, tune_x, tune_y):
    """
    Tune the number of epochs and the learning rate

    :param x: the independant variable data
    :param y: the dependant variable data
    :param tune_x: the independant tuning variable data
    :param tune_y: the dependant tuning variable data
    :return: the tuned hyperparameters
    """

    # initialize candidate hyperparameters and best loss to high number
    learn_rate_vals = [.01, .1, 1, 10, 100]
    num_iterations_vals = [5000, 1000, 500]
    best_loss = len(tune_y) + 1

    # iterate over each hyperparameter
    for learn_rate in learn_rate_vals:
        for num_iterations in num_iterations_vals:

            # build the model
            thetas = build_model(x, y, num_iterations, learn_rate)
            classes = np.unique(y)

            # compute the loss
            loss = classification_loss(classes, thetas, tune_x, tune_y)

            if loss < best_loss:
                best_learn_rate = learn_rate
                best_num_iterations = num_iterations
                best_loss = loss

    return best_num_iterations, best_learn_rate


def main():

    # get the preprocessed dataframe
    df = preprocess(datafile, optionsfile, outputfile)

    # convert result col to numeric
    df['result'] = df['result'].astype('category').cat.codes

    # split out the tuning dataset from the main dataset
    df, tune_set = split_tune_df(df)
    write_output(outputfile, f'the tuning data set:\n {tune_set}')

    # split out the dependant and independant tuning variables
    tune_data = np.array(tune_set)
    x_tune = tune_data[:, :-1].astype(float)
    y_tune = tune_data[:, -1].astype(float)

    # split the remaining data into 5 groups for 5-fold cross validation
    group1, group2, group3, group4, group5 = split_5_fold_cross_validation(df)
    write_output(outputfile, f'group 1:\n{group1}')
    write_output(outputfile, f'group 2:\n{group2}')
    write_output(outputfile, f'group 3:\n{group3}')
    write_output(outputfile, f'group 4:\n{group4}')
    write_output(outputfile, f'group 5:\n{group5}')
    groups = [group1, group2, group3, group4, group5]

    # initialize the loss to 0
    total_loss = 0

    # cross validate each of the 5 sets
    for index, group in enumerate(groups):
        groups_copy = groups.copy()
        test_set = groups_copy.pop(index)
        train_set = pd.concat(groups_copy, axis=0)
        train_set = train_set.reset_index()
        del train_set['index']

        # convert the dataframe to array
        train_data = np.array(train_set)
        test_data = np.array(test_set)

        # split out the dependant and independant variables
        x_train = train_data[:, :-1].astype(float)
        y_train = train_data[:, -1].astype(float)
        x_test = test_data[:, :-1].astype(float)
        y_test = test_data[:, -1].astype(float)

        # tune the hyperparameters
        epochs, learn_rate = tune_hyperparameters(x_train, y_train, x_tune, y_tune)
        write_output(outputfile, f'The hyperparameters for cross {index} are:')
        write_output(outputfile, f'Learning Rate: {learn_rate}')
        write_output(outputfile, f'Number of Iterations: {epochs}')

        # build the model
        thetas = build_model(x_train, y_train, epochs, learn_rate)
        classes = np.unique(y_train)
        write_output(outputfile, f'model: {thetas}')
        write_output(outputfile, f'classes: {classes}')

        # get the loss and accuracy
        test_loss = classification_loss(classes, thetas, x_test, y_test)
        test_accuracy = (len(test_data) - test_loss) / len(test_data)
        total_loss += test_loss

        write_output(outputfile, f'Cross {index} Accuracy: {test_accuracy:.3f}')

    # output total classification loss and model accuracy
    write_output(outputfile, f'total classification loss: {total_loss}')
    model_accuracy = (len(df) - total_loss) / len(df) * 100
    write_output(outputfile, f'model accuracy: {model_accuracy:.2f}%')


if __name__ == '__main__':

    # initialize some options based on the selected set
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    set = config['set']
    verbose = config['verbose']
    datafile = f'DataSets/{set}.data'
    optionsfile = f'DataSets/{set}.options.yaml'
    outputfile = f'output/{set}-logistic-regression.output.txt'

    main()
