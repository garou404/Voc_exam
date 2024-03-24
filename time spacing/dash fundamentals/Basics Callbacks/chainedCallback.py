from dash import Dash, html, dcc, Input, Output, callback

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

all_options = {
    'America': ['New York City', 'San Francisco', 'Cincinnati'],
    'Canada': ['Montréal', 'Toronto', 'Ottawa']
}

app.layout = html.Div([
    dcc.RadioItems(
        list(all_options.keys()),
        'America',
        id='countries-radio',
    ),

    html.Hr(),

    dcc.RadioItems(id='cities-radio'),

    html.Hr(),

    html.Div(id='display-selected-values')
])
@callback(
    Output('cities-radio', 'options'),
    Input('countries-radio', 'value'))
def set_cities_options(country):
    #print([{'label': i, 'value': i} for i in all_options[country]])
    return [{'label': i, 'value': i} for i in all_options[country]]

@callback(
    Output('cities-radio', 'value'),
    Input('cities-radio', 'options'),)
def set_cities_value(available_options):
    return available_options[0]['value']



@callback(
    Output('display-selected-values', 'children'),
    Input('countries-radio', 'value'),
    Input('cities-radio', 'value'),)
def set_display_children(selected_country, selected_city):
    return f'{selected_city} is a city of {selected_country}'

if __name__ == '__main__':
    app.run(debug=True)