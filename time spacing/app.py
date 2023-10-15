from dash import Dash, html

# This line is known as the Dash constructor and is responsible for initializing your app. It is almost always the same for any Dash app you create.
app = Dash(__name__)

app.layout = html.Div([
    html.Div(children='Hello World')
])

if __name__ == '__main__':
    app.run(debug=True)