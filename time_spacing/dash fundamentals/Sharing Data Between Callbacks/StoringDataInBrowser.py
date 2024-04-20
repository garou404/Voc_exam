from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(),
    dcc.Table(),
    dcc.Dropdown(),

    #dcc.Store stores the intermediate value
    dcc.Store(id='intermediate-value')
])

@callback(
    Output('intermediate-value', 'data'),
    Input('dropdown', 'value'))
def clean_data(value):
    # some expensive data processing step
    cleaned_df = slow_processing_step(value)

    # more generally, this line would be
    # json.dumps(cleaned_df)
    return cleaned_df.to_json(date_format='iso', orient='split')

@callback(
    Output('graph', 'figure'),
    Input('intermediate-value', 'data'))
def update_graph(jsonified_cleaned_data):
    # more generally, this line would be
    # json.loads(jsonified_cleaned_data)
    dff = pd.read_json(jsonified_cleaned_data, orient='split')

    figure = create_figure(dff)
    return figure

@callback(
    Output('table', 'children'),
    Input('intermediate-value', 'data'))
def update_table(jsonified_cleaned_data):
    dff = pd.read_json(jsonified_cleaned_data, orient='split')
    table = create_table(dff)
    return table


if __name__ == '__main__':
    app.run(debug=True)