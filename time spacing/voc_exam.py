import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import random as rd
import datetime
import time

# progression steps cst
steps = [1, 1, 2, 4, 15, 26, 28, 29, 29]


# Dataset cleaning function
def clean_data(file_name)->pd.DataFrame:
    data = pd.read_excel(file_name, index_col=0)
    data.reset_index(inplace=True)
    # data = data.dropna(axis=0)
    data = data.reset_index(drop=True)
    count = 0
    # nettoyage et mise en page du tableau
    # concaténation des différentes traduction dans une seule case du tableau
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
    data.dropna(subset=data.columns[:2], inplace=True)
    data = data.reset_index(drop=True)
    return data

# Dates uploading
def upload_date(df:pd.DataFrame) ->pd.DataFrame:
    today = datetime.datetime.now()
    # If the date is older than today date then update it
    df.loc[df['date'] < today, "date"] = pd.to_datetime(today.date())
    for i in range(df.shape[0]):
        if(isinstance(df['date'][i], datetime.datetime)):
            df.loc[i, 'date'] = pd.to_datetime(df.loc[i, 'date'].date())
    return df['date']



# Random draw of 20 words
# Print the words one by one
def iteration(data, file_name, size):
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

def add_words(question, answer) ->pd.DataFrame:
    print("test")

def get_series(data, size) ->pd.DataFrame:
    if data.shape[0] < size:
        raise Exception('serie size superior than data rows')
    selected = pd.DataFrame()
    indexes = []
    count = 0

    date_test = datetime.datetime.now().date()
    while count != size:
        df_temp = data.loc[data['date'].dt.date == date_test]
        list_index = df_temp.index.values
        if size - count < df_temp.shape[0]:
            rd.shuffle(list_index)
            indexes.extend(list_index[:(size - count)])
        else:
            indexes.extend(list_index)
        count = len(indexes)
        date_test = date_test + datetime.timedelta(days=1)

    rd.shuffle(indexes)
    selected = data.loc[indexes]  # selection aléatoire des éléments
    print(selected.head(100).to_string())
    return selected

def update_row(row, result):
    print('input')
    print(row.to_string())
    date_column_index = row.columns.get_loc('date')
    steps_column_index = row.columns.get_loc('steps_index')
    asked_count_col_index = row.columns.get_loc('asked_count')
    row.iloc[0, asked_count_col_index] = row.iloc[0, asked_count_col_index] + 1
    row.iloc[0, row.columns.get_loc('third_last_asked')] = row.iloc[0, row.columns.get_loc('second_last_asked')]
    row.iloc[0, row.columns.get_loc('second_last_asked')] = row.iloc[0, row.columns.get_loc('first_last_asked')]
    if (result == 1):
        right_answer_count_col_index = row.columns.get_loc('right_answer_count')
        row.iloc[0, right_answer_count_col_index] = row.iloc[0, right_answer_count_col_index] + 1
        # change steps index
        if row.iloc[0, steps_column_index] + 1 != len(steps):
            row.iloc[0, steps_column_index] = row.iloc[0, steps_column_index] + 1
        # add (steps[] * days) to the current date
        row.iloc[0, date_column_index] = row.iloc[0, date_column_index] + datetime.timedelta(days=steps[row.iloc[0, steps_column_index]])
        row.iloc[0, row.columns.get_loc('first_last_asked')] = True
    else:
        # change steps index
        if row.iloc[0, steps_column_index] - 1 > 0:
            row.iloc[0, steps_column_index] = row.iloc[0, steps_column_index] - 1
            # add (steps[] * days) to the current date
        row.iloc[0, date_column_index] = row.iloc[0, date_column_index] + datetime.timedelta(days=steps[row.iloc[0, steps_column_index]])
        row.iloc[0, row.columns.get_loc('first_last_asked')] = False
    print('output')
    print(row.to_string())
    return row

def save_series(df, df_temp, file):
    df = clean_data(file)
    df['date'] = upload_date(df)
    df.update(df_temp)
    print(df_temp.head(100).to_string())
    print(df.head(1000).to_string())
    # raise Exception('stop right here')
    df.to_excel(file, index=False)


def save_serie_score(serie_size, score):
    df_series = pd.read_csv('words/series_history.csv', sep=';')
    today = datetime.datetime.now()
    if df_series.shape[0] == 0:
        df_series.loc[0] = [serie_size, score, today.date()]
    else:
        df_series.loc[df_series.shape[0] + 1] = [serie_size, score, today.date()]
    print(df_series)
    print([serie_size, score, today.date()])
    #raise Exception('no serie saving')
    df_series.to_csv('words/series_history.csv', sep=';', index=False)

def get_dataframe(file):
    df = clean_data(file)
    df['date'] = upload_date(df)
    return df

#df = clean_data(file)
#df['date'] = upload_date(df)
#iteration(df, file, 30)# manque mettre la date de demain si on échoue

#rajouter du code: si le fichier est ouvert dit de le fermer

