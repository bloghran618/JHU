import yaml
import pandas as pd
import numpy as np

from write_to_output import write_output


def preprocess(datafile, optionsfile, outputfile):
    with open(optionsfile) as file:
        options = yaml.load(file, Loader=yaml.FullLoader)

    write_output(outputfile, f'options: {options}')

    # deal with missing attributes
    if options.get('missing_attributes') == 'drop':
        df = pd.read_csv(datafile, header=None, na_values=['?'])
        df = df.dropna()
        df = df.reset_index(drop=True)
    else:
        df = pd.read_csv(datafile, header=None)

    # drop the left column if it is an index column
    if options.get('left_index') == True:
        del df[0]

    # one hot encode specified values in options file
    one_hot = options.get('one_hot_encode')
    if one_hot:
        for col_num, name in one_hot.items():
            write_output(outputfile, f'{col_num}: {name}')
            unique = df[col_num-1].unique()
            unique.sort()
            write_output(outputfile, f'unique {name} values: {unique}')
            col_names = []
            for value in unique:
                col_name = f'{name}={value}'
                col_names.append(col_name)
                df[col_name] = [1 if val == value else 0 for val in df[col_num-1]]
            del df[col_num-1]
            write_output(outputfile, f'column names for {unique}: {col_names}')

    # discretize real values in options file
    discretize = options.get('discretize')
    if discretize:
        discretize_groups = options['discretize_groups']
        for col_num, name in discretize.items():
            col_max = df[col_num-1].max()
            col_min = df[col_num-1].min()
            col_range = col_max - col_min
            step = col_range / discretize_groups
            write_output(outputfile, f'real valued column {name} discretized to: ')
            for group in range(discretize_groups):
                group_min = col_min + step * group
                group_max = col_min + step * (group+1)
                # add 1 to the last group maximum to properly handle maximum value
                if group == discretize_groups-1:
                    group_max += 1
                col_name = f'{name.strip()}_{group/discretize_groups*100:.0f}-{(group+1)/discretize_groups*100:.0f}%'
                df[col_name] = [1 if (val >= group_min and val < group_max) else 0 for val in df[col_num-1]]
                write_output(outputfile, f'{col_name}')

            del df[col_num-1]

    # randomize the row order if specified
    if options.get('randomize_rows'):
        df = df.reindex(np.random.permutation(df.index))
        df = df.reset_index()
        del df['index']

    # move the result column to the end and replace values if neccessary
    df = df.rename(columns={options.get('result_col')-1: 'result'})
    cols = df.columns.tolist()
    cols.remove('result')
    cols.append('result')
    df = df[cols]
    if options.get('result_encode'):
        for convert_from, convert_to in options.get('result_encode').items():
            df['result'] = df['result'].replace([convert_from], convert_to)

    pd.set_option("display.max_columns", None)
    pd.set_option("display.expand_frame_repr", False)
    write_output(outputfile, df)

    return df
