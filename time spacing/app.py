from dash import Dash, html, dash_table, dcc, callback, Output, Input, State, ctx
import pandas as pd
import plotly.express as px
import datetime
from voc_exam import get_test_series, upload_date, clean_data

 # data loading
file = 'words_test.xlsx'
df = clean_data(file)
df['date'] = upload_date(df)
df = get_test_series(df, 10)
print(df)
index = 0

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div([

        dcc.Input(id="series-size", type="text", value=""),
        html.Button(id='start-button', n_clicks=0, children='Start series'),
    ], id='quizz-container')
])

@callback(
    Output('quizz-container', 'children', allow_duplicate=True),
    Input('start-button', 'n_clicks'),
    State('series-size', 'value'),
    prevent_initial_call=True)
def start_series(n_clicks, series_size):
    global df
    global index
    first_row = df.iloc[index]
    index += 1
    quiz_layout = html.Div([
        html.Div(first_row['question']),
        dcc.Input(type='text'),
        html.Button(id='show-answer', children='show answer'),
        html.Div(first_row['answer']),
        html.Button(id='right-answer-button', children='Y'),
        html.Button(id='wrong-answer-button', children='N'),
    ], id='test')
    return quiz_layout


@callback(
    Output('test', 'children'),
    Input('right-answer-button', 'n_clicks'),
    Input('wrong-answer-button', 'n_clicks'),
    prevent_initial_call=True)
def change_question(n_clicks_yes, n_clicks_no):
    button_id = ctx.triggered_id
    global df
    global index
    if index == 10:
        index = 0
        basic_layout = html.Div([
            dcc.Input(id="series-size", type="text", value=""),
            html.Button(id='start-button', n_clicks=0, children='Start series')
        ])
        return basic_layout
    next_row = df.iloc[index]
    index += 1
    quiz_layout = html.Div([
        html.Div(next_row['question']),
        dcc.Input(type='text'),
        html.Button(id='show-answer', children='show answer'),
        html.Div(next_row['answer']),
        html.Button(id='right-answer-button', children='Y'),
        html.Button(id='wrong-answer-button', children='N'),
    ])
    return quiz_layout

# Run the app
if __name__ == '__main__':
    app.run(debug=True)