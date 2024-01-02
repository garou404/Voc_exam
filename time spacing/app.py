from dash import Dash, html, dash_table, dcc, callback, Output, Input, State, ctx
import pandas as pd
import plotly.express as px
import datetime
from voc_exam import get_dataframe, upload_date, clean_data, update_row, save_series, get_series

 # data loading
file = 'words_lv.xlsx'

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
    global df_tempo
    df_tempo = get_series(get_dataframe('words_lv.xlsx'), int(serie_size))
    df_tempo['asked'] = False
    df_tempo['answered'] = False
    df_tempo.iloc[0, df_tempo.columns.get_loc('asked')] = True
    condition = (df_tempo['answered'] == False) & (df_tempo['asked'] == True)
    question = df_tempo.loc[condition, 'question']
    return get_quiz_layout(question)

@callback(
    Output('answer-label', 'children'),
    Input('show-answer', 'n_clicks'),
    prevent_initial_call=True)
def show_answer(n_clicks):
    global df_tempo
    condition = (df_tempo['answered'] == False) & (df_tempo['asked'] == True)
    answer = df_tempo.loc[condition, 'answer']
    return answer

@callback(Output('quiz_layout', 'children'),
          Input('right-answer-button', 'n_clicks'),
          Input('wrong-answer-button', 'n_clicks'),
          State('answer-label', 'children'),
          prevent_initial_call=True)
def display_next_question(n_clicks_right, n_clicks_wrong, answer):
    global df_tempo
    condition = (df_tempo['answered'] == False) & (df_tempo['asked'] == True)

    if ctx.triggered_id == 'right-answer-button': # update the interval and the date
        df_tempo.update(update_row(df_tempo[condition], 1))
    else:
        df_tempo.update(update_row(df_tempo[condition], 0))
    df_tempo.loc[condition, 'answered'] = True

    if len(df_tempo['answered'].unique()) == 1: # end of serie
        df = get_dataframe('words_lv.xlsx')
        save_series(df, df_tempo, 'words_lv.xlsx')
        return html.Div(['serie complete'])

    result = df_tempo.loc[df_tempo['asked'] == False]
    result.iloc[0, result.columns.get_loc('asked')] = True
    df_tempo.update(result)
    question = result.iloc[0, result.columns.get_loc('question')]
    return get_quiz_layout(question)


def get_quiz_layout(input_text):
    quiz_layout = html.Div([
        html.Div(input_text),
        dcc.Input(type='text'),
        html.Button(id='show-answer', children='show answer'),
        html.Div(id='answer-label'),
        html.Button(id='right-answer-button', children='Y'),
        html.Button(id='wrong-answer-button', children='N'),
    ], id='quiz_layout')
    return quiz_layout

# Run the app
if __name__ == '__main__':
    app.run(debug=True)