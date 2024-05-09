from dash import Dash, html, dcc
import callbacks


# Initialize the app
app = Dash(__name__)
app.config["suppress_callback_exceptions"] = True


# App layout
app.layout = html.Div([
    dcc.Location(id='main-url'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(figure=callbacks.get_scores_graph())
                ], className='mb-4'),
                html.Div([
                    html.Div([
                        dcc.Graph(figure=callbacks.get_month_heatmap_graph(current=False)),
                    ], className='col-md-6'),
                    html.Div([
                        dcc.Graph(figure=callbacks.get_month_heatmap_graph(current=True))
                    ], className='col-md-6')
                ], className='row'),
                html.Div(className='row pb-5', id='words-ranking-container')
            ], className='container-fluid')
        ], className='col-auto col-md-4 px-sm-2 px-0 bg-dark'),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Input(id="serie-size", type="text", value="", className='form-control ')
                        ], className='col-md-8'),
                        html.Div([
                            html.Button(id='start-button', n_clicks=0, children='Start series', className='btn btn-primary ')
                        ], className='col-md-4'),
                    ], id='quiz-starter', className='row border-bottom border-dark p-5'),
                    html.Div([
                    ], id='quiz-container', className='row')
                ], className='col-6 mt-5 border border-primary rounded ')
            ], className='row justify-content-md-center pt-5')
        ], className='col')
    ], className='row', style={'height': '100vh'})
], className='container-fluid', style={'height': '100vh'})


# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
