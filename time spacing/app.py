from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
import pandas as pd
import plotly.express as px


# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='First app with data'),
    html.Hr(),
    dcc.Input(id="answer", type="text", placeholder="", style={'marginRight':'10px'}),
    html.Button('Submit', id='submit-val'),
    html.Div(id='correction'),
])

# Add controls to build the interaction
@callback(
    Output(component_id='correction', component_property='children'),
    Input('submit-val', 'n_clicks'),
    State('answer', 'value'))
def update_output(n_clicks, value):
    return value

# Run the app
if __name__ == '__main__':
    app.run(debug=True)