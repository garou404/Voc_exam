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
                print()
                print()
                print("data['answer'][idx]")
                print(data['answer'][idx])
                print("data['answer'][idx] type : " + str(type(data['answer'][idx])))
                print()
                print("data['answer'][idx + next_index]")
                print(data['answer'][idx + next_index])
                print("data['answer'][idx + next_index] type :" + str(type(data['answer'][idx + next_index])))
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
    if data.shape[0] < size:
        raise Exception('serie size superior than data rows')
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
    print(selected.head(100).to_string())
    return selected

def update_row(row, result):
    y_axis_date = row.columns.get_loc('date')
    if (result == 1):
        # change interval
        y_axis_interval = row.columns.get_loc('interval')
        row.iloc[0, y_axis_interval] = row.iloc[0, y_axis_interval] * 2
        # add interval * days to the current date
        row.iloc[0, y_axis_date] = row.iloc[0, y_axis_date] + datetime.timedelta(days=row.iloc[0, y_axis_interval].item())
    else:
        row.iloc[0, y_axis_date] = row.iloc[0, y_axis_date] + datetime.timedelta(days=1)
    return row

def save_series(df, df_temp, file):
    df = clean_data(file)
    df['date'] = upload_date(df)
    df.update(df_temp)
    print(df_temp.head(100).to_string())
    print(df.head(1000).to_string())
    raise Exception('stop right here')
    df.to_excel(file, index=False, header=False)

def get_dataframe(file):
    df = clean_data(file)
    df['date'] = upload_date(df)
    return df

#df = clean_data(file)
#df['date'] = upload_date(df)
#iteration(df, file, 30)# manque mettre la date de demain si on échoue

#rajouter du code: si le fichier est ouvert dit de le fermer

