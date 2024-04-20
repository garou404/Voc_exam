from dash import Dash, html, dcc, Input, Output, callback, State

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id="input-1", type="text", value="Montréal"),
    dcc.Input(id="input-2", type="text", value="Canada"),
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
    html.Div(id="number-output"),
])

@callback(
    Output('number-output', 'children'),
    Input('submit-button-state', 'n_clicks'),
    State('input-1', 'value'),
    State('input-2', 'value'))
def update_output(n_clicks, input1, input2):
    return f'''
            The Button has been pressed {n_clicks} times,
            Input 1 is "{input1}",
            and Input 2 is "{input2}"
        '''

if __name__ == '__main__':
    app.run(debug=True)