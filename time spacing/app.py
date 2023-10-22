from dash import Dash, html, dash_table, dcc, callback, Output, Input, State, ctx
import pandas as pd
import plotly.express as px
import datetime
today = datetime.datetime.now().date()
index = 0
data = [["lurk", "se cacher/se tapir/roder", 1, today], ["stumbling", "qui trébuche", 2, today]]
columns = ['question', 'answer', 'interval', 'date']
words = pd.DataFrame(data, columns=columns)

row = words.loc[index]

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='First app with data'),
    html.Hr(),
    html.Div(id='question', children=row['question']),
    dcc.Input(id="answer", type="text", placeholder="", style={'marginRight':'10px'}),
    html.Button('Submit', id='submit-val'),
    html.Div(id='correction'),
    html.Div(id='test2'),
    html.Button('Yes', id='right-button'),
    html.Button('No', id='wrong-button'),
])


@callback(
    Output(component_id='correction', component_property='children', allow_duplicate=True),
    Input('submit-val', 'n_clicks'),
    State('answer', 'value'),
    prevent_initial_call=True
)
#--------------------------------------------------------------------------------
#                      function to print the answer
#--------------------------------------------------------------------------------
def update_output(n_clicks, value):
    print(n_clicks)
    index += 1
    return row['answer']


@callback(
    Output('question', 'children'),
    Output(component_id='correction', component_property='children'),
    Input('right-button', 'n_clicks'),
    Input('wrong-button', 'n_clicks'),

    )
#--------------------------------------------------------------------------------
#                      function to indicate if the answer is right or not
#--------------------------------------------------------------------------------
def update_output_yes(b1, b2):
    triggered_id = ctx.triggered_id
    row = words.loc[index]
    if triggered_id == 'right-button':
        print('yes')
    elif triggered_id == 'wrong-button':
        print('no')
        print(row['question'], row['answer'])
    return row['question'], row['answer']

#--------------------------------------------------------------------------------
#                      function which return a row of the data
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
#                      function which replace the old row with the new one updated
#--------------------------------------------------------------------------------

# Run the app
if __name__ == '__main__':
    app.run(debug=True)