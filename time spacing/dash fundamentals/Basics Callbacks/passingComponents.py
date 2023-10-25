from dash import Dash, html, dcc, Input, Output, callback, State

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__, external_stylesheets=external_stylesheets)

my_input = dcc.Input(id='my-input', value='initial value', type='text')
app.layout = html.Div([
    html.H6("Change the value in the text box to see callbacks in action!"),
    html.Div([
        "Input: ",
        my_input
    ]),
    html.Br(),
    my_output := html.Div(id='my-output')
    ])

@callback(
    Output(my_output, 'children'),
    Input(my_input, 'value'))
def update_output_div(input_value):
    return f'Output: {input_value}'

if __name__ == '__main__':
    app.run(debug=True)