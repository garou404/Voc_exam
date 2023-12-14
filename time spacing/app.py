from dash import Dash, html, dash_table, dcc, callback, Output, Input, State, ctx
import pandas as pd
import plotly.express as px
import datetime
from voc_exam import get_test_series, upload_date, clean_data, update_row

 # data loading
file = 'words_test.xlsx'

df = clean_data('words_test.xlsx') # à améliorer
df['date'] = upload_date(df)
df_tempo = pd.DataFrame()

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div([
        dcc.Input(id="serie-size", type="text", value=""),
        html.Button(id='start-button', n_clicks=0, children='Start series'),
    ], id='quiz-starter'),
    html.Div([

    ], id='quiz-container')
])

@callback(Output('quiz-container', 'children'),
          Input('start-button', 'n_clicks'),
          State('serie-size', 'value'),
          prevent_initial_call=True)
def start_quiz(n_clicks, serie_size):
    global df
    global df_tempo
    df_tempo = get_test_series(df, int(serie_size)).reset_index()
    df_tempo['asked'] = False
    df_tempo['answered'] = False
    df_tempo.at[0, 'asked'] = True
    condition = (df_tempo['answered'] == False) & (df_tempo['asked'] == True)
    question = df_tempo.loc[condition, 'question'][0]
    quiz_layout = html.Div([
        html.Div(question),
        dcc.Input(type='text'),
        html.Button(id='show-answer', children='show answer'),
        html.Div(id='answer-label'),
        html.Button(id='right-answer-button', children='Y'),
        html.Button(id='wrong-answer-button', children='N'),
    ], id='test')
    return quiz_layout

@callback(
    Output('answer-label', 'children'),
    Input('show-answer', 'n_clicks'),
    prevent_initial_call=True)
def show_answer(n_clicks):
    global df_tempo
    condition = (df_tempo['answered'] == False) & (df_tempo['asked'] == True)
    selected_indices = df_tempo.loc[df_tempo['answered'] == False].index.tolist()
    answer = df_tempo.loc[condition, 'answer'][selected_indices[0]]
    return answer

@callback(Output('test', 'children'),
          Input('right-answer-button', 'n_clicks'),
          Input('wrong-answer-button', 'n_clicks'),
          State('answer-label', 'children'),
          prevent_initial_call=True)
def display_next_question(n_clicks_right, n_clicks_wrong, answer):
    global df_tempo
    condition = (df_tempo['answered'] == False) & (df_tempo['asked'] == True)
    selected_indices = df_tempo.loc[df_tempo['answered'] == False].index.tolist()
    if ctx.triggered_id == 'right-answer-button': # update the interval and the date
        print('yes')
        df_tempo.loc[condition, 'answered'] = True
    else:
        print('no')
        df_tempo.loc[condition, 'answered'] = True

    if len(df_tempo['answered'].unique()) == 1:
        return html.Div(['serie complete'])

    cond = (df_tempo['asked'] == False)
    new_selected_indices = df_tempo.loc[cond].index.tolist()
    print(new_selected_indices)
    print(new_selected_indices[0])
    df_tempo.loc[cond & (df_tempo.index == new_selected_indices[0]), 'asked'] = True
    print(df_tempo)
    condition = (df_tempo['answered'] == False) & (df_tempo['asked'] == True)
    question = df_tempo.loc[condition, 'question'][new_selected_indices[0]]
    print(question)
    quiz_layout = html.Div([
        html.Div(question),
        #html.Div('text'),
        dcc.Input(type='text'),
        html.Button(id='show-answer', children='show answer'),
        html.Div(id='answer-label'),
        html.Button(id='right-answer-button', children='Y'),
        html.Button(id='wrong-answer-button', children='N'),
    ], id='test')
    return quiz_layout

# Run the app
if __name__ == '__main__':
    app.run(debug=True)