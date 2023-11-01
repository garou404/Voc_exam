from dash import Dash, html, dash_table, dcc, callback, Output, Input, State, ctx
import pandas as pd
import plotly.express as px
import datetime
from voc_exam import get_test_series, upload_date, clean_data

 # data loading
file = 'words_test.xlsx'

df = clean_data('words_test.xlsx') # à améliorer
df['date'] = upload_date(df)
print(df)
index = 0
size = 0

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
    global size
    print('test')
    print(df)
    print(df.dtypes)
    print(type(serie_size))
    df = get_test_series(df, int(serie_size))
    print('test 2')
    size = serie_size
    print('test 3')
    row = df.iloc[index]
    print('test 4')
    quiz_layout = html.Div([
        html.Div(row['question']),
        dcc.Input(type='text'),
        html.Button(id='show-answer', children='show answer'),
        html.Div(row['answer']),
        html.Button(id='right-answer-button', children='Y'),
        html.Button(id='wrong-answer-button', children='N'),
    ], id='test')
    return quiz_layout


@callback(Output('test', 'children'),
          Input('right-answer-button', 'n_clicks'),
          Input('wrong-answer-button', 'n_clicks'),
          prevent_initial_call=True)
def display_next_question(n_clicks_right, n_clicks_wrong):
    global index
    global df
    global size
    print(type(size))
    print(type(index))
    row = df.iloc[index]
    if str(index) == size:
        index = 0
        size = 0
        return html.Div(['serie complete'])
    quiz_layout = html.Div([
        html.Div(row['question']),
        dcc.Input(type='text'),
        html.Button(id='show-answer', children='show answer'),
        html.Div(row['answer']),
        html.Button(id='right-answer-button', children='Y'),
        html.Button(id='wrong-answer-button', children='N'),
    ], id='test')
    index += 1
    return quiz_layout
# Run the app
if __name__ == '__main__':
    app.run(debug=True)