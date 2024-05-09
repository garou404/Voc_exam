import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import random as rd
import datetime
import os

# progression steps
STEPS = [1, 1, 2, 4, 15, 26, 28, 29, 29]
DATA_PATH = 'words/'
WORDS_FILE = DATA_PATH+'words_V1.0.0.xlsx'
SERIES_HISTO_FILE = DATA_PATH+'series_history.csv'
BIN_PATH = DATA_PATH+'bin.csv'

def clean_data(file_name) -> pd.DataFrame:
    """
    dataset cleaning
    :param file_name: words data path
    :return: return the words dataframe
    """
    data = pd.read_excel(file_name, index_col=0)
    data.reset_index(inplace=True)
    data = data.reset_index(drop=True)
    count = 0
    # concatenate the translations with the previous one if the question value is empty
    for idx in data.index:
        if not isinstance(data['question'][idx], str):
            count += 1
            continue
        next_index = 1
        if count < data.shape[0] - 1:
            while isinstance(data['question'][idx + next_index], str) == False:
                data['answer'][idx] = data['answer'][idx] + "#" + data['answer'][idx + next_index]
                next_index += 1
        count += 1
    # then drop the data with empty values
    data.dropna(subset=data.columns[:2], inplace=True)
    data = data.reset_index(drop=True)
    return data


def upload_date(df:pd.DataFrame) -> pd.Series:
    """
    update the date older than today to today's date
    :param df: words_dataframe
    :return: return the updated date column
    """
    today = datetime.datetime.now()
    # If the date is older than today's date then update it
    df.loc[df['date'] < today, "date"] = pd.to_datetime(today.date())
    # change date column type to date and not datetime
    for i in range(df.shape[0]):
        if(isinstance(df['date'][i], datetime.datetime)):
            df.loc[i, 'date'] = pd.to_datetime(df.loc[i, 'date'].date())
    return df['date']


def add_words(question, answer):
    """
    add new words to the dataset
    is to done
    :param question:
    :param answer:
    :return:
    """
    print("add word")


def get_series(data, size) -> pd.DataFrame:
    """
    get a data subset for the quiz
    :param data: entire dataset of words
    :param size: number of words to be asked
    :return: return the subset
    """
    # verify that the series size isn't bigger than the entire dataset
    if data.shape[0] < size:
        raise Exception('series size bigger than dataset rows')
    selected = pd.DataFrame()
    indexes = []
    selected_words_count = 0

    date_exam = datetime.datetime.now().date()
    # iterate over the days until the number of selected rows is equal to size
    while selected_words_count != size:
        df_temp = data.loc[data['date'].dt.date == date_exam]
        list_index = df_temp.index.values
        if size - selected_words_count < df_temp.shape[0]:
            rd.shuffle(list_index)
            indexes.extend(list_index[:(size - selected_words_count)])
        else:
            indexes.extend(list_index)
        selected_words_count = len(indexes)
        # increments exam date by one day
        date_exam = date_exam + datetime.timedelta(days=1)

    # randomize indexes selection
    rd.shuffle(indexes)
    selected = data.loc[indexes]
    return selected


def update_row(row, result):
    """
    update the word row according to the answer (yes or no)
    :param row: word row
    :param result: 1 good answer 0 otherwise
    :return: return the updated row
    """
    # get columns index in columns list
    date_column_index = row.columns.get_loc('date')
    steps_column_index = row.columns.get_loc('steps_index')
    asked_count_col_index = row.columns.get_loc('asked_count')
    # increment asked count
    row.iloc[0, asked_count_col_index] = row.iloc[0, asked_count_col_index] + 1
    # shift the last asked values
    row.iloc[0, row.columns.get_loc('third_last_asked')] = row.iloc[0, row.columns.get_loc('second_last_asked')]
    row.iloc[0, row.columns.get_loc('second_last_asked')] = row.iloc[0, row.columns.get_loc('first_last_asked')]

    if (result == 1):
        # increment right answer count
        right_answer_count_col_index = row.columns.get_loc('right_answer_count')
        row.iloc[0, right_answer_count_col_index] = row.iloc[0, right_answer_count_col_index] + 1

        # change steps index
        if row.iloc[0, steps_column_index] + 1 != len(STEPS):
            row.iloc[0, steps_column_index] = row.iloc[0, steps_column_index] + 1
        # add (steps[] * days) to the current date
        row.iloc[0, date_column_index] = row.iloc[0, date_column_index] + \
                                         datetime.timedelta(days=STEPS[row.iloc[0, steps_column_index]])
        row.iloc[0, row.columns.get_loc('first_last_asked')] = True
    else:
        # change steps index
        if row.iloc[0, steps_column_index] - 1 > 0:
            row.iloc[0, steps_column_index] = row.iloc[0, steps_column_index] - 1
            # add (steps[] * days) to the current date
        row.iloc[0, date_column_index] = row.iloc[0, date_column_index] + \
                                         datetime.timedelta(days=STEPS[row.iloc[0, steps_column_index]])
        row.iloc[0, row.columns.get_loc('first_last_asked')] = False
    return row


def save_series(df, df_temp, file):
    """
    update the dataset with the updated dataset used for the quiz
    :param df:
    :param df_temp: updated dataset
    :param file: words data path
    :return: nothing
    """
    df = clean_data(file)
    df['date'] = upload_date(df)
    df.update(df_temp)

    # Select rows index that need to go
    index_to_evict = df_temp.loc[df_temp['trash'] == True].index
    df_cleaned = df.drop(index_to_evict)

    # Create bin file if doesn't exist and add first line for df columns
    if not os.path.exists(BIN_PATH):
        with open(BIN_PATH, 'a') as bin_file:
            bin_file.write('old_index;question;answer;date;steps_index;fr_to_eng;right_answer_count;asked_count;\
            first_last_asked;second_last_asked;third_last_asked')

    # Forms the df_bin with old words and new ones
    df_bin = pd.read_csv(BIN_PATH, sep=';')
    df_add_to_bin = df_temp.loc[df_temp['trash'] == True, df_temp.columns.values[:-3]].rename_axis('old_index').reset_index()
    df_bin = pd.concat([df_bin, df_add_to_bin])

    df_bin.to_csv(BIN_PATH, index=False, sep=';')
    df_cleaned.to_excel(file, index=False)


def save_series_score(series_size, score):
    """
    add the current series score to the previous ones and save it
    :param series_size:
    :param score:
    :return:
    """
    df_series = pd.read_csv(SERIES_HISTO_FILE, sep=';')
    today = datetime.datetime.now()
    if df_series.shape[0] == 0:
        df_series.loc[0] = [series_size, score, today.date()]
    else:
        if pd.to_datetime(df_series.loc[df_series.shape[0] - 1, 'date']).date() == today.date():
            df_series.loc[df_series.shape[0] - 1, 'serie_size'] = \
                df_series.loc[df_series.shape[0] - 1, 'serie_size'] + series_size
            df_series.loc[df_series.shape[0] - 1, 'serie_score'] = \
                df_series.loc[df_series.shape[0] - 1, 'serie_score'] + score
        else:
            df_series.loc[df_series.shape[0] + 1] = [series_size, score, today.date()]
    df_series.to_csv(SERIES_HISTO_FILE, sep=';', index=False)


def get_dataframe(file) -> pd.DataFrame:
    """
    :param file: path of words file
    :return: return the entire words DataFrame
    """
    df = clean_data(file)
    df['date'] = upload_date(df)
    return df

def get_ranking(best):
    """

    :param best:
    :return:
    """
    df_words = get_dataframe(WORDS_FILE)
    df_words_asked = df_words.loc[df_words['asked_count'] >= 3]
    df_words_asked['ratio'] = df_words['right_answer_count']/df_words['asked_count']
    df_words_asked['score'] = df_words['right_answer_count'].astype(str)+'/'+df_words['asked_count'].astype(str)

    if best:
        df_words_asked = df_words_asked.sort_values(by=['ratio', 'asked_count'], ascending=[False, False])
        df_words_asked = df_words_asked.reset_index(drop=True).reset_index()
        df_words_asked['index'] = df_words_asked['index'] + 1
        return df_words_asked[['index', 'question', 'score']].head()
    else:
        df_words_asked = df_words_asked.sort_values(by=['ratio', 'asked_count'], ascending=[True, False])
        df_words_asked = df_words_asked.reset_index(drop=True).reset_index()
        df_words_asked['index'] = df_words.loc[df_words['asked_count'] >= 3].shape[0] - df_words_asked['index']
        return df_words_asked[['index', 'question', 'score']].head()

def iteration(data, file_name, size):
    """
    command version of the quiz
    :param data:
    :param file_name:
    :param size:
    :return:
    """
    selected = pd.DataFrame()
    indexes = []
    random_index = rd.randint(0, data.shape[0] - 1)
    count = 0
    while count != size:
        if (indexes.count(random_index) == 0) & (data['date'][random_index] == datetime.datetime.now().date()):
            count +=1
            indexes.append(random_index)
        random_index = rd.randint(0, data.shape[0] -1)
    selected = data.loc[indexes] #selection aléatoire des éléments
    print(indexes)
    for id in selected.index:
        print(id)
        print("What is the meaning of: "+selected["question"][id])
        entree = str(input())
        print("My answer : "+ entree+" The answer : "+selected["answer"][id])
        print("Did you get it right?(Y, N)")
        entree = str(input())
        if entree == "Y":
            # change interval
            selected["interval"][id] = selected["interval"][id] * 2
            # add interval * days to the current date
            selected["date"][id] = selected["date"][id] + datetime.timedelta(days = selected["interval"][id].item())# marche pas visiblement
        elif entree == "exit":
            break
        else:
            print(selected["date"][id] + datetime.timedelta(days=1))
            selected["date"][id] = selected["date"][id] + datetime.timedelta(days=1)
    data.loc[indexes] = selected
    #df['date'] = datetime.datetime.today().date()
    data.to_excel(file_name, index=False, header=False)