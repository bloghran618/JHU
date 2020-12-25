import yaml
from preprocess_datafile import preprocess
from utils import *


def list_lists(list):
    """
    Convert list to list of lists  - helper function

    :param list: the list to convert
    :return: the list of lists
    """
    return [[element] for element in list]


def weight_initialization(n_features):
    """
    Initialize weights and intercept to zeros

    :param n_features: the number of features to initialize
    :return: the zeroed weights and intercept
    """
    w = np.zeros((1, n_features))
    b = 0
    return w, b


def build_model(w, b, x, y, learning_rate, no_iterations):
    """
    Build the weights vectors for training data

    :param w: the initialized weights
    :param b: the initialized intercept
    :param x: the training independant variables
    :param y: the training dependant variables
    :param learning_rate: the learning rate
    :param no_iterations: the number of iterations to pass
    :return: the weights and intercept
    """

    # get the number of cases in x
    cases = x.shape[0]

    for i in range(no_iterations):
        # process result vector
        results = 1 / (1 + np.exp(-(np.dot(w, x.T) + b)[0]))

        # calculate gradient
        dw = (1 / cases) * (np.dot(x.T, (results - y.T).T))
        db = (1 / cases) * (np.sum(results - y.T))

        # update weights
        if verbose:
            write_output(outputfile, f"update weights {w} with gradient {- (learning_rate * (dw.T))}")
            write_output(outputfile, f"update intercept {b} by value {- (learning_rate * db)}")
        w = w - (learning_rate * (dw.T))
        b = b - (learning_rate * db)

    return w, b


def predict(classes, confidence):
    """
    Predict the result classes based on one vs. all confidence values

    :param classes: the possible result classes
    :param confidence: the class confidence
    :return: the predicted classes
    """

    predictions = []
    write_output(outputfile, f'Possible result classes: {classes}')

    # iterate over each instance in the confidence values
    for index, instance in enumerate(confidence[0]):
        instance_confidence = []

        # iterate over each confidence value
        for class_confidence in confidence:
            instance_confidence.append(class_confidence[index])
        write_output(outputfile, f'instance confidence[{index}] = {instance_confidence}')
        # guess the result class with the highest confidence
        guess_index = instance_confidence.index(max(instance_confidence))
        write_output(outputfile, f'prediction: {classes[guess_index]}')
        predictions.append(classes[guess_index])
    return predictions


def train_test(train_set, test_set, learn_rate, num_iterations):
    """
    Train a model and find classification loss of the model

    :param train_set: the training data
    :param test_set: the test data
    :param learn_rate: the learning rate
    :param num_iterations: the number of iterations
    :return: the classification loss of the learned model
    """
    # initialize the result classes and sigmoid values to empty lists
    result_classes = []
    confidence_values = []

    # get a copy of the training set and results for repeated use
    train_set_copy = train_set.copy()
    actual_results = test_set['result'].copy()

    for result_class in train_set['result'].unique():
        # manipulate result to be 1 if result class else 0
        train_set['result'] = [1 if (val == result_class) else 0 for val in train_set['result']]

        # split out the dependant and independant variables
        x_train = train_set.drop('result', axis=1)
        x_test = test_set.drop('result', axis=1)
        y_train = np.array(list_lists(train_set['result'].as_matrix()))

        # initialize weights and intercept
        w, b = weight_initialization(x_train.shape[1])

        # build the model
        w, b = build_model(w, b, x_train, y_train, learning_rate=learn_rate, no_iterations=num_iterations)
        write_output(outputfile, f'Model for class: {result_class}')
        write_output(outputfile, f'Model weights: {w[0]}')
        write_output(outputfile, f'Model intercept: {b}')

        # make prediction
        final_test_pred = 1 / (1 + np.exp(-(np.dot(w, x_test.T) + b)[0]))
        write_output(outputfile, f'{result_class} final test pred: \n{final_test_pred}')

        # track classes and class confidence values
        result_classes.append(result_class)
        confidence_values.append(final_test_pred)

        # copy train set for reuse
        train_set = train_set_copy.copy()

    # initialize classification loss to 0
    write_output(outputfile, f'\n\nTest Set:')
    classification_loss = 0

    # get the predictions based on class confidence
    y_pred = predict(result_classes, confidence_values)

    # check predictions against actual result class
    for index, row in enumerate(y_pred):
        write_output(outputfile, f'pred: {y_pred[index]}; actual: {actual_results.loc[index]}')
        if y_pred[index] != actual_results.loc[index]:
            # iterate loss if prediction is wrong
            classification_loss += 1
    write_output(outputfile, f'classification loss: {classification_loss}')
    return classification_loss


def tune_hyperparameters(train_set, tune_set):
    """
    Tune the number of iterations  and the learning rate

    :param train_set: the training set
    :param tune_set: the tuning validation set
    :return: the hyperparameters
    """

    # initialize candidate hyperparameters and best loss to high number
    learn_rate_vals = [.01, .1, 1, 10, 100]
    num_iterations_vals = [250, 100, 10]
    best_loss = len(tune_set) + 1

    # iterate over each hyperparameter
    for learn_rate in learn_rate_vals:
        for num_iterations in num_iterations_vals:

            # build a model and find the loss
            loss = train_test(train_set.copy(), tune_set.copy(), learn_rate, num_iterations)

            # update best hyperparameters if the loss improves
            if loss < best_loss:
                best_learn_rate = learn_rate
                best_num_iterations = num_iterations
                best_loss = loss

    return best_learn_rate, best_num_iterations


def main():

    # get the preprocessed dataframe
    df = preprocess(datafile, optionsfile, outputfile)

    # split out the tuning dataset from the main dataset
    df, tune_set = split_tune_df(df)
    write_output(outputfile, f'the tuning data set:\n {tune_set}')

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

        # tune the hyperparameters for model building
        learn_rate, num_iterations = tune_hyperparameters(train_set, tune_set)
        write_output(outputfile, f'The hyperparameters for cross {index} are:')
        write_output(outputfile, f'Learning Rate: {learn_rate}')
        write_output(outputfile, f'Number of Iterations: {num_iterations}')

        # get the loss and accuracy
        cross_loss = train_test(train_set, test_set, learn_rate, num_iterations)
        test_accuracy = (len(test_set) - cross_loss) / len(test_set)
        total_loss += cross_loss

        write_output(outputfile, f'Cross {index} Accuracy: {test_accuracy:.3f}')

    # output total classification loss and model accuracy
    write_output(outputfile, f'total classification loss: {total_loss}')
    model_accuracy = (len(df) - total_loss) / len(df) * 100
    write_output(outputfile, f'model accuracy: {model_accuracy:.2f}%')


if __name__ == "__main__":

    # initialize some options based on the selected set
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    set = config['set']
    verbose = config['verbose']
    datafile = f'DataSets/{set}.data'
    optionsfile = f'DataSets/{set}.options.yaml'
    outputfile = f'output/{set}-adaline.output.txt'

    main()
