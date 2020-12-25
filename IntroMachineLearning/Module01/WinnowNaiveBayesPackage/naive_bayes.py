from preprocess_datafile import preprocess
from write_to_output import write_output
import yaml


# get the parsed dataframe
with open('config.yaml') as file:
    set_dict = yaml.load(file, Loader=yaml.FullLoader)
set = set_dict['set']
datafile = f'DataSets/{set}.data'
optionsfile = f'DataSets/{set}.options.yaml'
outputfile = f'output/{set}-naive-bayes.output.txt'
df = preprocess(datafile, optionsfile, outputfile)

# initialize the result instances and probabilities
result_instances = {}
result_probs = {}

# indicate the name fo the result column, which is the last column
result_col = df.columns[-1]

# get the number of training cases and test cases for the dataframe
num_rows = len(df.index)
num_train_cases = int( num_rows * 7 / 10 )
num_test_cases = num_rows - num_train_cases

# find the result classes and the occurance of each result class in the training set
for index, row in enumerate(df.head(num_train_cases).itertuples()):
    result_class = df.at[index, result_col]
    if result_class in result_instances.keys():
        result_instances[result_class] += 1
    else:
        result_instances[result_class] = 1

# convert result occurance to result probability
result_probs = result_instances.copy()
for key, value in result_probs.items():
    result_probs[key] = value / num_train_cases
write_output(outputfile, f'the class instances: {result_instances}')
write_output(outputfile, f'the class probabilities: {result_probs}')

# create an object {result_class: [{}, {}, ...]} to track conditional probability
conditional_instances = {}
for key in result_instances:
    conditional_instances[key] = []
    for col in df.columns[:-1]:
        conditional_instances[key].append({})

# populate values for each conditional instance
for index, row in enumerate(df.head(num_train_cases).itertuples()):
    # get the result class of the df row
    result_class = df.at[index, result_col]
    for col_num, col in enumerate(df.columns[:-1]):
        # count up the conditional instances of each attribute
        attribute = df.loc[df.index[index], col]
        if attribute in conditional_instances[result_class][col_num].keys():
            conditional_instances[result_class][col_num][attribute] += 1
        else:
            conditional_instances[result_class][col_num][attribute] = 1

# convert conditional instance to conditional probability
conditional_probabilities = conditional_instances.copy()
for result_class in conditional_probabilities:
    for index, attribute_counts in enumerate(conditional_probabilities[result_class]):
        class_instances = result_instances[result_class]
        for attribute, count in attribute_counts.items():
            conditional_probabilities[result_class][index][attribute] = count/class_instances
write_output(outputfile, 'conditional probabilities:')
for key, value in conditional_probabilities.items():
    write_output(outputfile, f'{key}: {value}')

# done training

# initialize predictions to 0
correct_predictions = 0
incorrect_predictions = 0

# borrow formatting for result prediction dictionary
result_prediction = result_instances.copy()

# predict the result class based on conditional probabilities
for index, row in enumerate(df.tail(num_test_cases).itertuples()):
    write_output(outputfile, f'row: {row}')
    total_class_value = 0
    for result_class in result_prediction:
        class_value = 1
        for col_num, col in enumerate(df.columns[:-1]):
            try:
                class_value = class_value * conditional_probabilities[result_class][col_num][df.loc[df.index[index], col]]
            except KeyError:
                # if the class has not seen this value before, give lowest possible value that isnt 0
                class_value = class_value / num_test_cases

        # print(f'the class probability: {result_probs[result_class]}')
        class_value = class_value * result_probs[result_class]
        result_prediction[result_class] = class_value
        total_class_value += class_value
    write_output(outputfile, f'result prediction raw: {result_prediction}')

    # normalize the result
    for result_class in result_prediction:
        result_prediction[result_class] = result_prediction[result_class] / total_class_value * 100
    write_output(outputfile, f'result prediction normalized: {result_prediction}')

    # make a prediction based on the maximum of the result predictions
    predicted_class = max(result_prediction, key=result_prediction.get)
    write_output(outputfile, f'the predicted class is: {predicted_class}')
    write_output(outputfile, f'the actual class is: {df.at[index, result_col]}\n')

    # check if the prediction is correct
    if predicted_class == df.at[index, result_col]:
        correct_predictions += 1
    else:
        incorrect_predictions += 1

# output a human readable data model
write_output(outputfile, f'the class probabilities:')
for result_class, probability in result_probs.items():
    write_output(outputfile, f'{result_class}: {probability}')
for result_class in result_prediction:
    write_output(outputfile, f'\nthe attribute probabilities for {result_class}:')
    probabilities = conditional_probabilities[result_class]
    for index, dictionary in enumerate(probabilities):
        write_output(outputfile, f'{df.columns[index]} probabilities: {dictionary}')

# output the accuracy of the model
write_output(outputfile, f'percent correct: {correct_predictions / num_test_cases * 100}%')
