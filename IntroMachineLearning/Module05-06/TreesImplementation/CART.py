import yaml
import math

from preprocess_datafile import preprocess
from utils import *


def check_purity(data):
    """
    Determine the purity of the result class

    :param data: the data array
    :return: whether the data is pure
    """
    # get the unique results
    result_col = data[:, -1]
    unique_results = np.unique(result_col)

    # check if data is pure
    if len(unique_results) == 1:
        return True
    else:
        return False


def get_potential_splits(data):
    """
    Determine the potential splits

    :param data: the data array
    :return: a list of list of potential splits
    """
    potential_splits = {}
    num_rows, num_cols = data.shape
    # iterate over each of the columns
    for index in range(num_cols - 1):

        # splits at unique data points
        values = data[:, index]
        unique_values = np.unique(values)
        potential_splits[index] = unique_values

    return potential_splits


def calculate_mse(data):
    """
    Calculate the mean squared error for the data set

    :param data: the data array
    :return: the mean squared error of the result column
    """
    mse = 0
    # ensure that data is not empty
    if len(data) != 0:

        # compute mse against the average of the data
        result_col = data[:, -1]
        prediction = np.mean(result_col)
        mse = np.mean((result_col - prediction) ** 2)

    return mse


def calculate_weighted_mse(below, above):
    """
    Calculate the weighted msean squared error based on two split data sets

    :param below: the data set below the criteria
    :param above: the data set above the criteria
    :return: the weighted mean squared error
    """

    # get the percentage of data below and above for weighting
    percent_below = len(below) / (len(below) + len(above))
    percent_above = len(above) / (len(below) + len(above))

    # get the weighted mse
    weighted_mse = (percent_below * calculate_mse(below) + percent_above * calculate_mse(above))

    return weighted_mse


def get_best_split(data, potential_splits):
    """
    Determine the best split based on the mean squared error

    :param data: the data to split
    :param potential_splits: the potential splits
    :return: the column and value to split on for best mse
    """

    # initialize the best mean squared value to a high number
    best_mse = math.inf

    # iterate over all possible splits
    for col in potential_splits:
        for value in potential_splits[col]:

            # get the mse for the potential split
            data_below, data_above = split_data(data, col, value)
            mse = calculate_weighted_mse(data_below, data_above)

            # check if this is the best mse
            if mse <= best_mse:
                best_mse = mse
                best_split_col = col
                best_split_val = value
                write_output(outputfile, f'better split found on {best_split_col} at {best_split_val} with mse={mse}')

    return best_split_col, best_split_val


def split_data(data, split_col, split_val):
    """
    Split the data on given column value

    :param data: the data array to split
    :param split_col: the column to split on
    :param split_val: the value to split on
    :return: the high and low data arrays
    """
    # get the values of the split column
    split_col_vals = data[:, split_col]

    type_of_feature = feature_types[split_col]
    if type_of_feature == "numeric":
        # split on numeric value
        data_below = data[split_col_vals <= split_val]
        data_above = data[split_col_vals > split_val]
    elif type_of_feature == "categorical":
        # split on whether the category matches or not
        data_below = data[split_col_vals == split_val]
        data_above = data[split_col_vals != split_val]
    else:
        # something went wrong
        raise RuntimeError("Unrecognized feature type")

    return data_below, data_above


def build_tree(data, min_samples, recursions=0):
    """
    Recursively build the decision tree

    :param data: the data array
    :param min_samples: the minimum number of samples for a leaf node
    :return: the decision tree
    """

    # check whether we can create a leaf
    if (check_purity(data)) or recursions > 500:
        return np.mean(data[:, -1])
    if len(data) <= min_samples:
        write_output(outputfile, f'data {data} \nhas less than {min_samples} samples, prune subtree')
        return np.mean(data[:, -1])

    # else create an internal node
    else:
        recursions += 1

        # split the data on the best possible split
        potential_splits = get_potential_splits(data)
        split_column, split_value = get_best_split(data, potential_splits)
        data_below, data_above = split_data(data, split_column, split_value)

        # determine the type of internal node
        col_name = col_names[split_column]
        feature_type = feature_types[split_column]
        if feature_type == "numeric":
            # create a <= condition on a numeric data type
            condition = f"{col_name} <= {split_value}"
        elif feature_type == "categorical":
            # create an == condition on a categorical data type
            condition = f"{col_name} == {split_value}"
        else:
            # something went wrong
            raise RuntimeError("Unrecognized feature type")

        # recursively build subtrees
        sub_tree = {condition: []}
        condition_true = build_tree(data_below, min_samples, recursions)
        condition_false = build_tree(data_above, min_samples, recursions)

        # append to the subtree options (true is first, false is second)
        sub_tree[condition].append(condition_true)
        sub_tree[condition].append(condition_false)

        return sub_tree


def predict(row, tree):
    """
    predict a row of a dataframe based on the decision tree

    :param row: the row to predict
    :param tree: the decision tree
    :return: the prediction
    """

    # get the components of the condition at the node
    condition = list(tree.keys())[0]
    col_name, operator, value = condition.split(" ")

    # numerical condition
    if operator == "<=":
        if row[col_name] <= float(value):
            # row agrees with condition
            prediction = tree[condition][0]
        else:
            # row disagrees with condition
            prediction = tree[condition][1]
    # categorical condition
    elif operator == "==":
        if str(row[col_name]) == value:
            # row agrees with condition
            prediction = tree[condition][0]
        else:
            # row disagrees with condition
            prediction = tree[condition][1]
    else:
        # something went wrong
        raise RuntimeError("Condition is not in <= and ==")

    # determine whether to recursively continue or return prediction
    if isinstance(prediction, dict):
        sub_tree = prediction
        return predict(row, sub_tree)
    else:
        return prediction


def calculate_accuracy(df, tree):
    """
    Calculate the mean squared error and avg error for a dataset and decision tree

    :param df: the dataset to predict
    :param tree: the decision tree
    :return: the mean squared error and the average error
    """
    # predict the dataset
    predictions = df.apply(predict, args=(tree,), axis=1)

    # get the mse and avg difference
    mse = ((df['result'] - predictions) ** 2).mean()
    avg_diff = (abs(df['result'] - predictions)).mean()

    # show predictions and actual values
    for i in range(len(df)):
        write_output(outputfile, f"pred: {predictions.loc[i]:.2f} actual: {df.loc[i, 'result']:.2f}")

    return mse, avg_diff


def tune_cutoff(train_set, tune_set):
    """
    Tune the best cutoff value

    :param train_set: the set to train on
    :param tune_set: the set to tune on
    :return: the best cutoff value
    """
    # cutoff values to test
    cutoff_values = [1, 2, 3, 5, 7, 10]

    # set initial best mse to a high value
    best_mse = math.inf
    for cutoff in cutoff_values:
        write_output(outputfile, f'try cutoff value: {cutoff}')
        # train a tree and get the mse of the tree on the tuning set
        tree = build_tree(train_set.values, cutoff)
        mse, avg_diff = calculate_accuracy(tune_set, tree)

        # save the best cutoff value
        if mse < best_mse:
            best_mse = mse
            best_cutoff = cutoff

    return best_cutoff


if __name__ == '__main__':
    # initialize the config, input file, outputfile, and options
    with open('CARTconfig.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    set = config['set']
    datafile = f'DataSets/{set}.data'
    optionsfile = f'DataSets/{set}.options.yaml'
    outputfile = f'output/{set}.output.txt'
    outputsummary = f'output/{set}.summary.txt'
    early_stopping = config['early_stopping']

    if early_stopping:
        outputfile = f'output/{set}-early.output.txt'

    df = preprocess(datafile, optionsfile, outputfile)

    # determine the column headers and feature types for the dataframe
    col_names = df.columns
    feature_types = []
    for attribute in df.columns[:-1]:
        if pd.to_numeric(df[attribute], errors='coerce').notnull().all():
            feature_types.append('numeric')
        else:
            feature_types.append('categorical')

    # split out the tuning dataset from the main dataset
    df, tune_set = split_tune_df(df)

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
    total_avg_diff = 0

    # cross validate each of the 5 sets
    for index, group in enumerate(groups):
        groups_copy = groups.copy()
        test_set = groups_copy.pop(index)
        train_set = pd.concat(groups_copy, axis=0)
        train_set = train_set.reset_index()
        del train_set['index']

        # get the tuned cutoff value
        if early_stopping:
            cutoff = tune_cutoff(train_set, tune_set)
        else:
            cutoff = 1

        # create the decision tree and compute the error
        tree = build_tree(train_set.values, cutoff)
        mse, avg_diff = calculate_accuracy(test_set, tree)

        total_loss += mse
        total_avg_diff += avg_diff

        write_output(outputfile, f'tree on fold {index}: {tree}')
        write_output(outputfile, f'the loss on fold {index} is: {mse}')
        write_output(outputfile, f'the average error on fold {index} is: {avg_diff}')
        write_output(outputfile, f'the cutoff value used on fold {index} is: {cutoff}')

    write_output(outputfile, f'the average error is: {total_avg_diff / 5}')
    write_output(outputfile, f'total loss: {total_loss}')

