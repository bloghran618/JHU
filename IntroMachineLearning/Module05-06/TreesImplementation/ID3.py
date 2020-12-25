import numpy as np
eps = np.finfo(float).eps
from numpy import log2 as log
import yaml
import math

from preprocess_datafile import preprocess
from utils import *


def is_numeric(df, attribute):
    """
    Check if a df column is numeric or categorical

    :param df: the dataframe
    :param attribute: the attribute
    :return: whether the attribute is numeric
    """
    return pd.to_numeric(df[attribute], errors='coerce').notnull().all()


def find_entropy(df):
    """
    Compute the entropy of the df results

    :param df: the data set
    :return: the entropy of the data set
    """
    result = df.keys()[-1]
    entropy = 0
    values = df[result].unique()
    for value in values:
        # compute the entropy for the result
        fraction = df[result].value_counts()[value] / len(df[result])
        entropy += -fraction * np.log2(fraction)
    return entropy


def find_entropy_attribute(df, attribute):
    """
    Compute the entropy of a single attribute

    :param df: the data set
    :param attribute: an attribute in the data frame
    :return: the entropy of the attribute
    """
    result = df.keys()[-1]
    target_variables = df[result].unique()
    variables = df[attribute].unique()
    entropy2 = 0
    # iterate over each unique attribute
    for variable in variables:
        entropy = 0
        # iterate over each unique result
        for target_variable in target_variables:
            # compute the entropy for the attribute
            num = len(df[attribute][df[attribute] == variable][df[result] == target_variable])
            den = len(df[attribute][df[attribute] == variable])
            fraction = num / (den + eps)
            entropy += -fraction * log(fraction + eps)
        fraction2 = den / len(df)
        entropy2 += -fraction2 * entropy
    return abs(entropy2)


def intrinsic_info_attribute(df, attribute):
    """
    Compute the intrinsic information of an attribute

    :param df: the data set
    :param attribute: an attribute in the data frame
    :return: the intrinsic info of the attribute
    """
    variables = df[attribute].unique()
    # edge case to ensure that split is not on pure attribute
    if len(variables) == 1:
        return float('inf')
    split_info = 0
    # iterate over each unique attribute
    for variable in variables:
        # compute the split info of the attribute
        num = sum(df[attribute] == variable)
        den = len(df)
        fraction = num / (den + eps)
        split_info += -fraction * log(fraction + eps)
    return abs(split_info)


def best_split(df, full_df):
    """
    Find the best split for the data

    :param df: the data set to split
    :param full_df: the full dataframe, used for determining categorical or numeric data
    :return: the splitting criteria
    """
    gain_ratios = []
    split_tracker = {}
    result = df.keys()[-1]
    # check each of the attributes for split
    for key in df.keys()[:-1]:
        if not is_numeric(full_df, key):
            # the attribute is categorical: compute gain ratio
            information_gain = find_entropy(df) - find_entropy_attribute(df, key)
            write_output(outputfile, f'information gain {key}: {information_gain}')
            gain_ratio = information_gain / intrinsic_info_attribute(df, key)
            write_output(outputfile, f'gain ratio {key}: {gain_ratio}')
            gain_ratios.append(information_gain / intrinsic_info_attribute(df, key))
        else:
            # the attribute is numeric
            sorted_df_att = df.sort_values(by=[key, result])
            attribute_gain_ratios = []
            split_rows = []
            # iterate over each row in the dataframe
            for row in range(len(df)-1):
                # determine whether the row is a potential split point
                if df.loc[row, result] != df.loc[row+1, result]:
                    # split the data on the row
                    split = (df.loc[row, key] + df.loc[row+1, key]) / 2
                    # convert column to 0 if less than criteria, else 1
                    sorted_df_att[key] = sorted_df_att[key].apply(lambda x: 0 if x < split else 1)
                    # compute gain ratio for split
                    information_gain = find_entropy(sorted_df_att) - find_entropy_attribute(sorted_df_att, key)
                    attribute_gain_ratios.append(information_gain / intrinsic_info_attribute(sorted_df_att, key))
                    split_rows.append(split)
            # get and output gain ratio
            gain_ratio = max(attribute_gain_ratios)
            write_output(outputfile, f'gain ratio {key}: {gain_ratio}')
            gain_ratios.append(gain_ratio)
            split_tracker[key] = split_rows[attribute_gain_ratios.index(max(attribute_gain_ratios))]

    # get the best gain raatio
    best_gain_key = df.keys()[:-1][np.argmax(gain_ratios)]
    write_output(outputfile, f'gain ratios: \n{gain_ratios}')
    write_output(outputfile, f'the best gain is for {best_gain_key}')
    if is_numeric(full_df, best_gain_key):
        # return criteria if attribute was numeric
        return f'{best_gain_key}<{split_tracker[best_gain_key]}'
    else:
        # return criteriaa if attribute was categorical
        return df.keys()[:-1][np.argmax(gain_ratios)]


def get_split(df, node, value):
    """
    Get the data that meets the node criteria

    :param df: the data set
    :param node: the criteria to split on
    :param value: the value to split on (either 0/1 for numeric attributes or name for categorical)
    :return: the subset of data that meets the criteria
    """
    if '<' in node:
        # criteria is numeric
        attribute, condition = node.split('<')
        condition = float(condition)
        return df[df[attribute] < condition].reset_index(drop=True)
    else:
        # criteria is categorical
        return df[df[node] == value].reset_index(drop=True)


def build_tree(df, full_df, min_samples, tree=None):
    """
    Build the decision tree

    :param df: the training dataset
    :param full_df: full_df: the full dataframe, used for determining categorical or numeric data
    :param min_samples: the minimum number of samples for the node
    :param tree: the current tree
    :return: the decision tree
    """
    result = df.keys()[-1]

    # get the best splitting criteria
    node = best_split(df, full_df)
    write_output(outputfile, f'split criteria: {node}')

    if '<' in node:
        # criteria is numeric
        attValue = [0, 1]
    else:
        # criteria is categorical
        attValue = np.unique(df[node])

    if tree is None:
        # initialize tree if it is empty
        tree = {node: {}}

    for value in attValue:

        # get the subtable and
        subtable = get_split(df, node, value)
        write_output(outputfile, f'the current subtable:\n {subtable}')
        result_val, counts = np.unique(subtable[result], return_counts=True)

        # helps tree to predict if it sees an unfamiliar example
        if '<' not in node:
            tree[node]['default'] = subtable[result].value_counts().index[0]

        if len(counts) == 1:
            # data is pure, node is result
            write_output(outputfile, f'the pure node is: {result_val[0]}')
            tree[node][value] = result_val[0]
        elif len(subtable) < min_samples:
            # cutoff tree with min samples
            write_output(outputfile, f'the cutoff node is: {subtable[result].value_counts().index[0]}')
            tree[node][value] = subtable[result].value_counts().index[0]
        else:
            # data is not pure yet, recursively split
            tree[node][value] = build_tree(subtable, full_df, min_samples)

    return tree


def predict(inst, tree):
    """
    Predict the value on an instance using the decision tree

    :param inst: the instance to predict
    :param tree: the decision tree
    :return: the predicted value
    """
    for nodes in tree.keys():

        # check if the node has numeric criteria
        if '<' in nodes:
            # get the data attribute and numeric condition
            attribute, condition = nodes.split('<')
            value = inst[attribute]
            condition = float(condition)
            if value < condition:
                # follow true branch
                tree = tree[nodes][1]
            else:
                # follow false branch
                tree = tree[nodes][0]
        else:
            # the condition is categorical, follow category
            value = inst[nodes]
            try:
                tree = tree[nodes][value]
            except KeyError:
                # the tree does not recognize this example, select most common value from subtrees
                
                prediction = tree[nodes]['default']
                break;

        # check if the node is a leaf node
        if type(tree) is dict:
            # node is not leaf, recursively follow tree
            prediction = predict(inst, tree)
        else:
            # node is leaf, return prediction
            prediction = tree
            break;

    return prediction


def test_model(d_tree, test_set):
    """
    Test a series of instances against a decision tree

    :param d_tree: the decision tree to test
    :param test_set: the data set to test with
    :return: the loss (categorical loss)
    """
    loss = 0
    # try every instance in the test set
    for index in range(len(test_set)):
        # get the prediction
        instance = test_set.iloc[index]
        prediction = predict(instance, d_tree)
        write_output(outputfile, f"pred: {prediction} actual: {instance['result']}")
        if prediction != instance['result']:
            # prediction was wrong, iterate loss
            loss += 1

    return loss


def tune_cutoff(train_set, tune_set):
    """
    Tune the best cutoff value

    :param train_set: the set to train on
    :param tune_set: the set to tune on
    :return: the best cutoff value
    """
    # cutoff values to test
    cutoff_values = [1, 2, 3, 5, 7, 10]

    # set initial best error to a high value
    best_loss = math.inf
    for cutoff in cutoff_values:
        write_output(outputfile, f'try cutoff value: {cutoff}')
        # train a tree and get the error of the tree on the tuning set
        tree = build_tree(train_set, train_set, cutoff)
        loss = test_model(tree, tune_set)

        # save the best cutoff value
        if loss < best_loss:
            best_loss = loss
            best_cutoff = cutoff

    return best_cutoff


if __name__ == '__main__':

    # initialize the config, input file, outputfile, and options
    with open('ID3config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    set = config['set']
    datafile = f'DataSets/{set}.data'
    optionsfile = f'DataSets/{set}.options.yaml'
    outputfile = f'output/{set}.output.txt'
    outputsummary = f'output/{set}.summary.txt'
    prune = config['prune']

    if prune:
        outputfile = f'output/{set}-prune.output.txt'

    df = preprocess(datafile, optionsfile, outputfile)

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

    # cross validate each of the 5 sets
    for index, group in enumerate(groups):
        groups_copy = groups.copy()
        test_set = groups_copy.pop(index)
        train_set = pd.concat(groups_copy, axis=0)
        train_set = train_set.reset_index()
        del train_set['index']

        # build and test tree for validation set
        if prune:
            cutoff = tune_cutoff(train_set, tune_set)
        else:
            cutoff = 1
        tree = build_tree(train_set, train_set, cutoff)
        write_output(outputfile, f'cross {index} model looks like: \n{tree}')
        loss = test_model(tree, test_set)
        write_output(outputfile, f'cross {index} loss: {loss} = {(len(test_set) - loss) / len(test_set * 100):.2f}% accurate')
        total_loss += loss

    # output the total model accuracy
    model_accuracy = (len(df) - total_loss) / len(df) * 100
    write_output(outputfile, f'model accuracy on {set} is: {model_accuracy:.2f}%')

