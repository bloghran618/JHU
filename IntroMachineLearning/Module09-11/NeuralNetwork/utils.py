import pandas as pd
import numpy as np


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


def write_output(output_file, string):
    """
    helper function to write file and console output

    :param output_file: the output file or list of output files
    :param string: the string to output
    :return:
    """
    if isinstance(output_file, list):
        for output in output_file:
            # write to all output files in output file list
            out_file = open(output, 'a+')
            out_file.write(str(string) + '\n')
            out_file.close()
    else:
        # write to just the output file
        out_file = open(output_file, 'a+')
        out_file.write(str(string) + '\n')
        out_file.close()
    print(string)