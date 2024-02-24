from dash import Dash, html, dash_table, dcc, callback, Output, Input, State, ctx
import pandas as pd
import plotly.express as px
import datetime

from pandas import DataFrame

from voc_exam import get_dataframe, upload_date, clean_data, update_row, save_series, get_series

 # data loading
file = 'words/words_lv.xlsx'
#file = 'words_lv.xlsx'
df_tempo: DataFrame = pd.DataFrame()

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Input(id="serie-size", type="text", value="", className='form-control ')
                ], className='col-md-8'),
                html.Div([
                    html.Button(id='start-button', n_clicks=0, children='Start series', className='btn btn-primary ')
                ], className='col-md-4'),
            ], id='quiz-starter',
            className='row border-bottom border-dark p-5'),
                html.Div([
            ], id='quiz-container', className='row')
        ], className='col-6 mt-5 border border-primary rounded ')
    ], className='row justify-content-md-center pt-5')
], className='container')

@callback(Output('quiz-container', 'children'),
          Input('start-button', 'n_clicks'),
          State('serie-size', 'value'),
          prevent_initial_call=True)
def start_quiz(n_clicks, serie_size):
    global df_tempo
    df_tempo = get_series(get_dataframe(file), int(serie_size))
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
        df = get_dataframe(file)
        save_series(df, df_tempo, file)
        return html.Div(['serie complete'])

    result = df_tempo.loc[df_tempo['asked'] == False]
    result.iloc[0, result.columns.get_loc('asked')] = True
    df_tempo.update(result)
    if result.iloc[0, result.columns.get_loc('fr_to_eng')] == True:
        print(result.iloc[0, result.columns.get_loc('answer')])
    question = result.iloc[0, result.columns.get_loc('question')]
    return get_quiz_layout(question)


def get_quiz_layout(input_text):
    quiz_layout = html.Div([
        html.Div([
            html.Div(input_text, className='form-label text-center my-5 h4'),
        ], className='row'),
        html.Div([
            html.Div([
                html.Div([
                    dcc.Input(type='text', className='form-control'),
                ], className='col-md-8'),
                html.Div([
                    html.Button(id='show-answer', children='Answer', className='btn btn-primary'),
                ], className='col-md-4'),
            ], className='row'),
            html.Div([
                html.Div(id='answer-label', className='form-label'),
            ], className='row'),
        ], className='row'),
        html.Div([
            html.Div([
                html.Button(id='right-answer-button', children='Good', className='btn btn-success mx-2 px-5'),
            ], className='col-md-6 d-flex justify-content-center'),
            html.Div([
                html.Button(id='wrong-answer-button', children='Wrong', className='btn btn-danger mx-2 px-5' ),
            ], className='col-md-6 d-flex justify-content-center'),
        ], className='row my-5'),
    ], id='quiz_layout', className='mt-5')
    return quiz_layout

# Run the app
if __name__ == '__main__':
    app.run(debug=True)