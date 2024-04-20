from dash import Dash, html, dcc, Input, Output, callback

app = Dash(__name__)

app.layout = html.Div([
    html.H6('Change the value in the text box to see callbacks in action!'),
    html.Div([
        'Input :',
        dcc.Input(id='my-input', value='initial value', type='text')
    ]),
    html.Br(),
    html.Div(id='my-output'),

])

@callback(
    Output('my-output', 'children'),
    Input('my-input', 'value')
)
def update_output_div(input_value):
    return f'Output: {input_value}'

if __name__ == '__main__':
    app.run(debug=True)