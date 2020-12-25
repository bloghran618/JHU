from preprocess_datafile import preprocess
from write_to_output import write_output
import yaml


def train(df, alpha, theta):
    """
    Train the given dataframe to produce weights for the model

    :param df: the dataframe to train
    :param alpha: the alpha value to use for training
    :param theta: the theta value to use for training

    :return: weights: the list of weights
    """
    # initialize weights to 1
    weights = []
    for column in df:
        weights.append(1)
    weights = weights[:-1]

    # train the model
    for index, row in enumerate(df.loc[0:num_test_cases].itertuples()):
        write_output(outputfile, f'row number {index}: {row}')
        # get the sum of the product of the columns and weights
        sum = 0
        for col_num, column in enumerate(df.columns[:-1]):
            sum = sum + df.loc[df.index[index], column] * weights[col_num]
        write_output(outputfile, f'sum is: {sum}')
        write_output(outputfile, f'threshold is: {theta}')

        # make a prediction based on the calculated sum and theta value
        if sum > theta:
            prediction = 1
        else:
            prediction = 0
        result = df.at[index, result_col]

        # demotion
        if prediction == 1 and result == 0:
            # demote all columns with value of 1 by a factor of alpha
            write_output(outputfile, f'prediction is incorrect; demote old weights: {weights}')
            for col_num, column in enumerate(df.columns[:-1]):
                if df.loc[df.index[index], column] == 1:
                    weights[col_num] = weights[col_num] / alpha
            write_output(outputfile, f'new weights: {weights}')
        # promotion
        elif prediction == 0 and result == 1:
            # promote all columns with a value of 1 by a factor of alpha
            write_output(outputfile, f'prediction is incorrect; promote old weights: {weights}')
            for col_num, column in enumerate(df.columns[:-1]):
                if df.loc[df.index[index], column] == 1:
                    weights[col_num] = weights[col_num] * alpha
            write_output(outputfile, f'new weights: {weights}')
        else:
            write_output(outputfile, 'prediction is correct!')
        write_output(outputfile, '\n')

    # this is the model
    write_output(outputfile, f'model a={alpha}, theta={theta}, trained weights: {weights}')
    return weights


def get_row_sum(df, df_row, weights):
    """
    Get the sum of the row for winnow-2

    :param df: the dataframe that we are using
    :param df_row: the row from the dataframe to compute the sum
    :param weights: the weight values for the model

    :return: sum: the computed sum
    """
    sum = 0
    for col_num, column in enumerate(df.columns[:-1]):
        # calculate the sum
        sum = sum + df.loc[df.index[df_row[0]], column] * weights[col_num]
    return sum


def test(df, weights, theta, start_row, end_row):
    """
    Test the winnow-2 model against the testing subset of the data for 2-classification problem

    :param df: the dataframe that we are using
    :param weights: the weight values of the model
    :param theta: the theta value of the model
    :param start_row: the first row of the test data set
    :param end_row: the last row of the test data set

    :return: num_incorrect: the number of incorrect classifications
    """
    num_incorrect = 0

    # test the model
    for row in df.loc[start_row+1:end_row].itertuples():
        sum = get_row_sum(df, row, weights)

        # make a prediction based on the calculated sum and theta value
        if sum > theta:
            prediction = 1
        else:
            prediction = 0
        result = df.at[row[0], result_col]

        # check if the prediction is incorrect and update num_incorrect if so
        if prediction != result:
            num_incorrect += 1

    return num_incorrect


def test_multiclass(df, weights, thetas, start_row, end_row, unique_results):
    """
    Test the winnow-2 model against the testing subset of the data for 2-classification problem

    :param df: the dataframe that we are using
    :param weights: the weight values of the model
    :param theta: the theta value of the model
    :param start_row: the first row of the test data set
    :param end_row: the last row of the test data set
    :param unique_results: the list of unique result classes

    :return: num_incorrect: the number of incorrect classifications
    """
    num_incorrect = 0

    # test the model
    for row in df.loc[start_row:end_row].itertuples():
        write_output(outputfile, row)

        # create a list of sums for each of the k models
        sums = []
        for index, result in enumerate(unique_results):
            sums.append(get_row_sum(df, row, weights[index]))

        write_output(outputfile, f'the sums for index {row[0]} are {sums}')

        # normalize the sums against their theta values for fair comparison
        for index, sum in enumerate(sums):
            sums[index] = sum / thetas[index]
        write_output(outputfile, f'the normalized sums using thetas={thetas} are {sums}')

        # select the class with the highest normalize sum value
        best_index = sums.index(max(sums))
        predicted_result = unique_results[best_index]
        actual_result = df.at[row[0], result_col]

        write_output(outputfile, f'the predicted result is: {predicted_result}')
        write_output(outputfile, f'the actual result is:    {actual_result}')

        # check if the prediction is incorrect and update num_incorrect if so
        if predicted_result != actual_result:
            num_incorrect += 1

    return num_incorrect


def tune(df):
    """
    tune the given dataframe according to winnow-2 to produce alpha and theta values

    :param df: the dataframe to tune

    :return: best_alpha, best_theta: the best values for alpha and theta to use for testing
    """
    alpha_range = [1.25, 1.5, 2, 3, 5]
    theta_range = [5, 10, 25, 100, 300]

    least_wrong = num_tune_cases + 1

    # utilize grid search for to find best alpha and theta
    for tune_alpha in alpha_range:
        for tune_theta in theta_range:
            weights = train(df, tune_alpha, tune_theta)
            num_wrong = test(df, weights, tune_theta, num_test_cases, num_test_cases+num_tune_cases)

            write_output(outputfile, f'produces {(num_tune_cases - num_wrong) / num_tune_cases * 100}% correct predictions\n')

            # update model values if loss function is better than previous minimum
            if num_wrong < least_wrong:
                least_wrong = num_wrong
                best_alpha = tune_alpha
                best_theta = tune_theta

    write_output(outputfile, f'the best model is alpha={best_alpha} theta={best_theta} for {result_col} with {num_wrong} wrong')

    return best_alpha, best_theta


# get the parsed dataframe
with open('config.yaml') as file:
    set_dict = yaml.load(file, Loader=yaml.FullLoader)
set = set_dict['set']
datafile = f'DataSets/{set}.data'
optionsfile = f'DataSets/{set}.options.yaml'
outputfile = f'output/{set}-winnow.output.txt'
df = preprocess(datafile, optionsfile, outputfile)

# empty the contents of the output file on start
open(outputfile, 'w').close()

# get the number of training cases and test cases for the dataframe
num_rows = len(df.index)
num_train_cases = int( num_rows * 6 / 10 )
num_tune_cases = int ( num_rows / 10)
num_test_cases = num_rows - num_tune_cases - num_train_cases

# the result column is the last column in the dataframe
result_col = df.columns[-1]

# check if we have a 2-classification problem or more
unique_results = df[result_col].unique()
if len(unique_results) == 2:
    multi_category = False
    # if 2-classification, convert result class to binary
    for binary, result in enumerate(unique_results):
        df['result'] = df['result'].replace([result], binary)
    write_output(outputfile, 'convert results from {unique_results} to [0, 1]')
else:
    multi_category = True

if not multi_category:
    # tune values for alpha and theta
    alpha, theta = tune(df)

    # get weights for the trained model
    weights = train(df, alpha, theta)

    # output the weights
    write_output(outputfile, f'model has alpha={alpha}; theta={theta}\nweights:')
    for index, weight in enumerate(weights):
        write_output(outputfile, f'{df.columns[index]}={weight}')

    # test the model and determine loss
    num_incorrect = test(df, weights, theta, num_train_cases+num_tune_cases, num_rows)

    write_output(outputfile, f'model accuracy: {(num_test_cases - num_incorrect) / num_test_cases * 100}%')
else:
    # initialize a series of alpha, theta and weights for the k models for k classifications
    alpha_values = []
    theta_values = []
    weights_values = []
    for result in unique_results:
        # create a new dataframe where the result is 1 if the result class is the model and 0 otherwise
        new_df = df.copy(deep=True)
        col_name = f'result={result}'
        new_df[col_name] = [1 if (val == result) else 0 for val in new_df['result']]
        del new_df['result']
        result_col = new_df.columns[-1]
        write_output(outputfile, f'the dataframe for {result} is \n{new_df}')

        # tune the model to get alpha and theta and train the model to get the weights
        alpha, theta = tune(new_df)
        weights = train(new_df, alpha, theta)

        # save the alpha theta and weights values for each of the k models
        alpha_values.append(alpha)
        theta_values.append(theta)
        weights_values.append(weights)

    # output the results of tuning and training for each of the unique classes
    write_output(outputfile, f'alpha values: {alpha_values}')
    write_output(outputfile, f'theta values: {theta_values}')
    write_output(outputfile, f'weights values: ')
    for weight in weights_values:
        write_output(outputfile, weight)
    write_output(outputfile, f'the unique results: {unique_results}')

    # test the model and determine loss
    result_col = df.columns[-1]
    num_incorrect = test_multiclass(df, weights_values, theta_values, num_train_cases+num_tune_cases, num_rows, unique_results)

    # output the data model for each of the k models
    for ind, result in enumerate(unique_results):
        write_output(outputfile, f'\n{result} model has alpha={alpha_values[ind]}; theta={theta_values[ind]}\nweights:')
        for index, weight in enumerate(weights):
            write_output(outputfile, f'{df.columns[index]}: {weights_values[ind][index]}')

    write_output(outputfile, f'model accuracy: {(num_test_cases - num_incorrect) / num_test_cases * 100}%')

