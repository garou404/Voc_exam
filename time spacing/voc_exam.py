import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import random
import datetime
import csv

file = 'words_test_test.xlsx'
# Dataset cleaning function
def clean_data(file_name)->pd.DataFrame:
    data = pd.read_excel(file_name, index_col=0, header=None)
    data.reset_index(inplace=True)
    data.columns = ['question', 'answer', 'interval', 'date']
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
    data = data.dropna(axis=0)
    data = data.reset_index(drop=True)
    return data

# Dates uploading
def upload_date(df:pd.DataFrame) ->pd.DataFrame:
    today = datetime.datetime.now()
    # If the date is older than today date then update it
    df.loc[df['date'] < today, "date"] = today.date()
    for i in range(df.shape[0]):
        if(isinstance(df['date'][i], datetime.datetime)):
            df['date'][i] = df['date'][i].date()
    return df['date']



# Random draw of 20 words
# Print the words one by one
def iteration(data, file_name, size):
    selected = pd.DataFrame()
    indexes = []
    random_index = random.randint(0, data.shape[0] - 1)
    count = 0
    while count != size:
        if (indexes.count(random_index) == 0) & (data['date'][random_index] == datetime.datetime.now().date()):
            count +=1
            indexes.append(random_index)
        random_index = random.randint(0, data.shape[0] -1)
    selected = data.loc[indexes]#selection aléatoire des éléments
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
    selected = pd.DataFrame()
    indexes = []
    random_index = random.randint(0, data.shape[0] - 1)
    count = 0
    while count != size:
        if (indexes.count(random_index) == 0) & (data['date'][random_index] == datetime.datetime.now().date()):
            count += 1
            indexes.append(random_index)
        random_index = random.randint(0, data.shape[0] - 1)
    selected = data.loc[indexes]  # selection aléatoire des éléments
    return selected

def update_row(row, result):
    if (result == 1):
        # change interval
        row.at[0, 'interval'] = row.at[0, 'interval'] * 2
        # add interval * days to the current date
        row.at[0, 'date'] = row.at[0, 'date'] + datetime.timedelta(days=row.at[0, 'interval'].item())
    else:
        print(row["date"][id] + datetime.timedelta(days=1))
        row.at[0, 'date'] = row.at[0, 'date'] + datetime.timedelta(days=1)
    return row

def save_series(df, df_temp):
    df_temp.set_index('index')
    df.update(df_temp)
    return df

def get_dataframe(size):
    df = clean_data('words_test_test.xlsx')
    df['date'] = upload_date(df)
    df_series = get_series(df, size)
    return df_series

#df = clean_data(file)
#df['date'] = upload_date(df)
#iteration(df, file, 30)# manque mettre la date de demain si on échoue

#rajouter du code: si le fichier est ouvert dit de le fermer

