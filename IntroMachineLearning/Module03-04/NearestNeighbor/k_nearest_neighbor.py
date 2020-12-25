import pandas as pd
import numpy as np
import yaml
import math

from preprocess_datafile import preprocess
from write_to_output import write_output
from neighbors import Neighbors


def split_tune_df(main_df):
    """
    split 10% of the data for tuning from the main dataset

    :param main_df: the main dataset

    :return: main_df: the main dataset sans the tuning set
    :return: tune_df: the tuning dataset
    """
    columns = main_df.columns
    tune_df = pd.DataFrame(columns=columns)

    # take 10% of the dataset for tuning
    condition = main_df.index % 10 == 0
    rows = main_df.loc[condition, :]
    tune_df = tune_df.append(rows, ignore_index=True)
    main_df.drop(rows.index, inplace=True)
    main_df = main_df.reset_index(drop=True)

    return main_df, tune_df


def split_5_fold_cross_validation(main_df):
    """
    split the dataset into 5 equal groups for 5-fold cross validation

    :param main_df: the main dataset
    :return: the 5 equal groups the main dataset was split into
    """
    columns = main_df.columns

    # take 20% of the dataset for cross 0
    cross_0 = pd.DataFrame(columns=columns)
    condition_0 = main_df.index % 5 == 0
    rows_0 = main_df.loc[condition_0, :]
    cross_0 = cross_0.append(rows_0, ignore_index=True)
    cross_0 = cross_0.reindex(np.random.permutation(cross_0.index))
    cross_0 = cross_0.reset_index()
    del cross_0['index']

    # take 20% of the dataset for cross 1
    cross_1 = pd.DataFrame(columns=columns)
    condition_1 = main_df.index % 5 == 1
    rows_1 = main_df.loc[condition_1, :]
    cross_1 = cross_1.append(rows_1, ignore_index=True)
    cross_1 = cross_1.reindex(np.random.permutation(cross_1.index))
    cross_1 = cross_1.reset_index()
    del cross_1['index']

    # take 20% of the dataset for cross 2
    cross_2 = pd.DataFrame(columns=columns)
    condition_2 = main_df.index % 5 == 2
    rows_2 = main_df.loc[condition_2, :]
    cross_2 = cross_2.append(rows_2, ignore_index=True)
    cross_2 = cross_2.reindex(np.random.permutation(cross_2.index))
    cross_2 = cross_2.reset_index()
    del cross_2['index']

    # take 20% of the dataset for cross 2
    cross_3 = pd.DataFrame(columns=columns)
    condition_3 = main_df.index % 5 == 3
    rows_3 = main_df.loc[condition_3, :]
    cross_3 = cross_3.append(rows_3, ignore_index=True)
    cross_3 = cross_3.reindex(np.random.permutation(cross_3.index))
    cross_3 = cross_3.reset_index()
    del cross_3['index']

    # take 20% of the dataset for cross 2
    cross_4 = pd.DataFrame(columns=columns)
    condition_4 = main_df.index % 5 == 4
    rows_4 = main_df.loc[condition_4, :]
    cross_4 = cross_4.append(rows_4, ignore_index=True)
    cross_4 = cross_4.reindex(np.random.permutation(cross_4.index))
    cross_4 = cross_4.reset_index()
    del cross_4['index']

    # return each of the split datasets
    return cross_0, cross_1, cross_2, cross_3, cross_4


def loss_function(method, guess, actual):
    """
    Compute the loss for either classification or regression

    :param method: either classification or regression
    :param guess: the provided guess to compute loss for
    :param actual: the actual value of the set

    :return: the loss for the guess and the actual for the method
    """
    if method == 'classification':
        # if classification, if the guess is wrong, loss is 1, else 0
        if guess == actual:
            return 0
        else:
            return 1
    elif method == 'regression':
        # for regression return rms error
        return (( guess - actual ) ** 2 )
    else:
        raise ValueError('Classification method must be either classification or regression')


def test_nearest_neighbor_classification(outputfile, train_set, test_set, k):
    """
    Test the performance of nearest neighbor on a classification set

    :param outputfile: the output file to write results to
    :param train_set: the already collected data to check against
    :param test_set: the set to test
    :param k: the number of nearest neighbors to consider

    :return: the loss of the nearest neighbor classification
    """
    total_loss = 0
    for row in test_set.itertuples():
        write_output(outputfile, f'\npoint is: {row}')
        # get the nearest neighbors
        nearest = Neighbors(k, train_set.columns, outputfile)
        nearest.get_nearest(train_set, row)
        nearest.output_neighbors(outputfile)
        # make the guess
        guess = nearest.purality_vote()
        write_output(outputfile, f'guess: {guess}')
        actual_result = row[len(train_set.columns)]
        write_output(outputfile, f'actual: {actual_result}')
        # compute the loss
        loss = loss_function('classification', guess, actual_result)
        total_loss += loss

    return total_loss


def tune_classification(outputfile, train_set, tune_set):
    """
    Tune the parameters for classification

    :param outputfile: the output file to write results to
    :param train_set: the already collected data to check against
    :param tune_set: the set used for tuning

    :return: the number of neighbors to consider
    """
    # specify a range for k to tune against
    k_range = [2, 3, 4, 5, 8, 10, 15, 25, 1]

    # initialize best loss to very bad
    best_loss = len(train_set) + 1
    for k_val in k_range:
        loss = test_nearest_neighbor_classification(outputfile, train_set, tune_set, k_val)
        write_output(outputfile, f'loss is {loss} for k={k_val}')

        # return k if loss is 0
        if loss == 0:
            return k_val

        # store value of best loss k and loss
        if loss < best_loss:
            best_loss = loss
            best_k = k_val

    return best_k


def get_regression_loss(outputfile, train_set, test_set, k, sigma):
    """
    Compute the loss of a regression set

    :param outputfile: the output file to write results to
    :param train_set: the already collected data to check against
    :param test_set: the set to test
    :param k: the number of nearest neighbors to consider
    :param sigma: the sigma value to use for kernel function

    :return: the regression loss
    """
    total_loss = 0
    for row in test_set.itertuples():
        write_output(outputfile, f'point is: \n{row}')
        # get the nearest neighbors
        nearest = Neighbors(k, train_set.columns, outputfile)
        nearest.get_nearest(train_set, row)
        nearest.output_neighbors(outputfile)
        # make a guess
        guess = nearest.gaussian_kernel(row, sigma)
        write_output(outputfile, f'guess: {guess}')
        actual_result = row[len(train_set.columns)]
        write_output(outputfile, f'actual: {actual_result}')
        # compute the loss
        loss = loss_function('regression', guess, actual_result)
        total_loss += loss

    return total_loss


def test_nearest_neighbor_regression(outputfile, train_set, test_set, k, sigma, epsilon):
    """
    Test the performance of nearest neighbor on a regression set

    :param outputfile: the output file to write results to
    :param train_set: the already collected data to check against
    :param test_set: the set to test
    :param k: the number of nearest neighbors to consider
    :param sigma: the sigma value to use for kernel function
    :param epsilon: the range of 'correct' solutions

    :return: the number of incorrect guesses
    """
    num_wrong = 0
    for row in test_set.itertuples():
        write_output(outputfile, f'\npoint is: {row}')
        # get the nearest neighbors
        nearest = Neighbors(k, train_set.columns, outputfile)
        nearest.get_nearest(train_set, row)
        nearest.output_neighbors(outputfile)
        # make a guess
        guess = nearest.gaussian_kernel(row, sigma)
        write_output(outputfile, f'guess: {guess}')
        actual_result = row[len(train_set.columns)]
        write_output(outputfile, f'actual: {actual_result}')
        # compute the loss
        if abs(guess - actual_result) > epsilon:
            num_wrong += 1

    return num_wrong


def tune_regression(outputfile, train_set, tune_set):
    """
    Tune the parameters for regression

    :param outputfile: the output file to write results to
    :param train_set: the already collected data to check against
    :param tune_set: the set used for tuning

    :return: the number of neighbors to consider and the best sigma and epsilon values
    """
    # specify range of k, sigma and epsilon to tune over
    k_range = [2, 5, 10, 25, 1]
    sigma_range = [0.05, 0.1, 0.5, 1, 5]
    espilon_range = [1, 2, 5, 10, 25, 50, 100, 250, 500, 1000]

    # initialize best loss to very bad
    best_loss = float('inf')

    # iterate over k and sigma to start
    for k_val in k_range:
        for sigma in sigma_range:
            # compute rms loss
            loss = get_regression_loss(outputfile, train_set, tune_set, k_val, sigma)
            write_output(outputfile, f'loss is {loss} for k={k_val}, sigma={sigma}')

            # store the values of the best loss, k and sigma values
            if loss < best_loss:
                best_loss = loss
                best_k = k_val
                best_sigma = sigma

    # initialize least wrong to very bad
    least_wrong = tune_set.size
    for epsilon in espilon_range:
        # compute how many incorrect guesses with epsilon value
        num_wrong = test_nearest_neighbor_regression(outputfile, train_set, tune_set, best_k, best_sigma, epsilon)
        write_output(outputfile, f'number wrong for epsilon={epsilon} is {num_wrong}')

        # store the values of the best loss and epsilon values
        if num_wrong < least_wrong:
            least_wrong = num_wrong
            best_epsilon = epsilon

    # return the tuned parameters
    return best_k, best_sigma, best_epsilon


def edit_train_set(set, tune_set, method, outputfile):
    """
    Reduce training set for edited k-nearest neighbor

    :param set: the set to reduce
    :param tune_set: the tuning set to tune against for iterations
    :param method: either regression or classification
    :param outputfile: the outputfile to write to

    :return: the edited/reduced set
    """
    # get the initial size of the dataframe
    num_initial_rows = len(set)

    # initialize epsilon to 2% of the result range
    result_col = set[set.columns[-1]]
    if method == 'regression':
        epsilon = (result_col.max() - result_col.min()) / 100

    # get the performance on the baseline set
    if method == 'classification':
        prev_loss = test_nearest_neighbor_classification(outputfile, set, tune_set, 1)
    elif method == 'regression':
        prev_loss = get_regression_loss(outputfile, set, tune_set, 1, 1)

    while True:
        prev_set = set.copy()
        for row in prev_set.itertuples():

            # create a backup df in case we do not want to remove inspected row
            set_not_dropped = set.copy()

            # remove the inspected row from the dataframe
            set = set.drop([row[0]])

            # classify based on nearest 1 neighbor
            nearest = Neighbors(1, set.columns, outputfile)
            nearest.get_nearest(set, row)
            nearest.output_neighbors(outputfile)
            # guess method depends if method is regression or classification
            if method == 'regression':
                guess = nearest.gaussian_kernel(row, 1)  # note that sigma value does not matter for 1 neighbor
            else:
                guess = nearest.purality_vote()
            write_output(outputfile, f'guess: {guess}')
            actual_result = row[len(set.columns)]
            write_output(outputfile, f'actual: {actual_result}')

            # drop row if guess is not result
            if method == 'classification':
                if guess == actual_result:
                    set = set_not_dropped
                else:
                    write_output(outputfile, f'remove row: {row}')

            # drop row if guess is incorrect by more than 2% range
            if method == 'regression':
                if abs(guess - actual_result) <= epsilon:
                    set = set_not_dropped
                else:
                    write_output(outputfile, f'remove row: {row}')

        # get the performance of the edited set
        if method == 'classification':
            current_loss = test_nearest_neighbor_classification(outputfile, set, tune_set, 1)
        elif method == 'regression':
            current_loss = get_regression_loss(outputfile, set, tune_set, 1, 1)

        # if the number of rows does not decrease, return edited neighbors
        write_output(outputfile, f'num rows pre-edited: {len(prev_set)}')
        write_output(outputfile, f'num rows post-edited: {len(set)}')
        if len(set) == len(prev_set):
            write_output(outputfile, 'The number of rows did not decrease: end row removal process')
            write_output(outputfile, f'num rows pre-edited: {num_initial_rows}')
            write_output(outputfile, f'num rows post-edited: {len(set)}')
            return set

        # if the performance does not improve, return the edited set
        write_output(outputfile, f'loss pre-edited: {prev_loss}')
        write_output(outputfile, f'loss post-edited: {current_loss}')
        if current_loss == prev_loss:
            write_output(outputfile, f'The performance did not improve: end row removal')
            return set
        elif current_loss > prev_loss:
            write_output(outputfile, f'The performance got worse: return the previous set and end row removal')
            return prev_set
        else:
            prev_loss = current_loss
        # if the performance improved, the algorithm will iterate again over


def get_incorrect_row(condensed_set, uncondensed_set, method, outputfile):
    """
    helper function which iterates over each row in the condensed set to see if any rows are misclassified

    :param condensed_set: the current condensed set
    :param uncondensed_set: the set to condense
    :param method: either classification or regression
    :param outputfile: the output file to write to

    :return: the incorrect row in the uncondensed_set, if there still is one
    """

    # initialize epsilon to 1% of the result range
    result_col = uncondensed_set[uncondensed_set.columns[-1]]
    if method == 'regression':
        epsilon = (result_col.max() - result_col.min()) / 100

    for row in uncondensed_set.itertuples():
        # classify based on nearest 1 neighbor against the condensed set
        nearest = Neighbors(1, condensed_set.columns, outputfile)
        nearest.get_nearest(condensed_set, row)
        nearest.output_neighbors(outputfile)
        # guess method depends if method is regression or classification
        if method == 'regression':
            guess = nearest.gaussian_kernel(row, 1)  # note that sigma value does not matter for 1 neighbor
        else:
            guess = nearest.purality_vote()
        write_output(outputfile, f'guess: {guess}')
        actual_result = row[len(condensed_set.columns)]
        write_output(outputfile, f'actual: {actual_result}')

        # drop row if guess is not result
        if method == 'classification':
            if guess != actual_result:
                write_output(outputfile, f'add row to condensed set: {row}')
                return row

        # drop row if guess is incorrect by more than 1% range
        if method == 'regression':
            if abs(guess - actual_result) >= epsilon or math.isnan(guess):
                write_output(outputfile, f'add row to condensed set: {row}')
                return row

    return False


def condense_train_set(set, method, outputfile):
    """
    Reduce training set for condensed k-nearest neighbor

    :param set: the set to reduce
    :param method: either regression or classification
    :param outputfile: the outputfile to write to

    :return: the condensed/reduced set
    """

    condensed = pd.DataFrame(columns=set.columns)

    # add the first index to the condensed dataframe
    entry = set.iloc[[0]]
    condensed = pd.concat([condensed, entry])
    print(condensed)

    # get the first incorrect row and begin iterating over the rows
    incorrect_row = get_incorrect_row(condensed, set, method, outputfile)
    while incorrect_row:
        # add the incorrect row to the condensed dataframe
        entry = set.iloc[[incorrect_row[0]]]
        condensed = pd.concat([condensed, entry])

        # get the next incorrect row if there is one
        incorrect_row = get_incorrect_row(condensed, set, method, outputfile)

    # summarize the results of condensing the training set
    write_output(outputfile, f'num rows pre-condensed: {len(set)}')
    write_output(outputfile, f'num rows post-condensed: {len(condensed)}')

    # return the condensed set
    return condensed


def main():
    # initialize the config, input file, outputfile, and options
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    set = config['set']
    datafile = f'DataSets/{set}.data'
    optionsfile = f'DataSets/{set}.options.yaml'
    outputfile = f'output/{set}.output.txt'
    outputsummary = f'output/{set}.summary.txt'

    # determine if we should run edited k nearest neighbor
    if config.get('edited'):
        run_edited = True
        outputfile = f'output/{set}-edited.output.txt'
        outputsummary = f'output/{set}-eddited.summary.txt'
    else:
        run_edited = False

    # determine if we should run edited k nearest neighbor
    if config.get('condensed'):
        run_condensed = True
        outputfile = f'output/{set}-condensed.output.txt'
        outputsummary = f'output/{set}-condensed.summary.txt'
    else:
        run_condensed = False

    # clear the contents of the output files
    open(outputfile, 'w').close()
    open(outputsummary, 'w').close()

    # get the preprocessed dataframe
    df = preprocess(datafile, optionsfile, outputfile)

    # determine how we want to make our estimations (regression or classification)
    method = config['method']
    if method not in ['regression', 'classification']:
        raise ValueError('method: value in config.yaml must be either regression or classification')

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

        # check if we want to run edited or condensed nearest neighbor
        if run_edited:
            new_train_set = edit_train_set(train_set, tune_set, method, outputfile)
            write_output([outputfile, outputsummary],
                         f'reduce training set for cross {index} from {len(train_set)} points to {len(new_train_set)} points')
            train_set = new_train_set
        elif run_condensed:
            new_train_set = condense_train_set(train_set, method, outputfile)
            write_output([outputfile, outputsummary],
                         f'reduce training set for cross {index} from {len(train_set)} points to {len(new_train_set)} points')
            train_set = new_train_set

        # k-nearest neighbor logic for classification problems
        if method == 'classification':

            k = tune_classification(outputfile, train_set, tune_set)
            write_output([outputfile, outputsummary], f'the model for cross {index} is: k={k}')
            loss = test_nearest_neighbor_classification(outputfile, train_set, test_set, k)
            write_output([outputfile, outputsummary], f'the loss for cross {index} is {loss} of {len(group)}\n')
            total_loss += loss

        # k-nearest neighbor logic for regression problems
        elif method == 'regression':
            k, sigma, epsilon = tune_regression(outputfile, train_set, tune_set)

            write_output([outputfile, outputsummary], f'the model for cross {index} is: k={k}, sigma={sigma}, epsilon={epsilon}')
            num_wrong = test_nearest_neighbor_regression(outputfile, train_set, test_set, k, sigma, epsilon)
            write_output([outputfile, outputsummary], f'the number wrong for cross {index} is {num_wrong} of {len(group)}\n')
            total_loss += num_wrong

        else:
            raise ValueError('Classification method must be either classification or regression')

    # program summary output
    write_output([outputfile, outputsummary], f'the loss for all 5 cross validations is: {total_loss}\n')
    accuracy = (len(df) - total_loss) / len(df) * 100
    write_output([outputfile, outputsummary], f'model accuracy is: {accuracy:.2f}%')


if __name__ == '__main__':
    main()
