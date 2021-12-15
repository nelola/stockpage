import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader.data as web
import datetime

# comment out to avoid cashing
start = datetime.datetime(2021, 1, 1)
end = datetime.datetime(2021, 12, 14)
df = web.DataReader(['AAPL.US', 'GOOGL', 'FB', 'PFE', 'BNTX', 'MRNA', 'AMZN'],
                    'stooq', start=start, end=end)

df = df.stack().reset_index()
print(df[:15])

df.to_csv("mystocks.csv", index=False)
df = df.reset_index()
print(df[:15])

# create the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',  # allows app to be responsive
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

# Layout section: Bootstrap
# ------------------------------------------------
app.layout = dbc.Container({

    dbc.Row(
        # Header one
        dbc.Col(html.H1("Stock Market Dashboard",
                        className='text-center text-primary, mb-4'),
                width=12)
    ),

    dbc.Row([

        dbc.Col([
            dcc.Dropdown(id='my-dpdn', multi=False, value='AMZN',
                         options=[{'label': x, 'value': x}
                                  for x in sorted(df["Symbols"].unique())],
                         ),
            dcc.Graph(id='line-fig', figure={})
        ],
            xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
            dcc.Dropdown(id='my-dpdn2', multi=True, value=['PFE', 'BNTX'],
                         options=[{'label': x, 'value': x}
                                  for x in sorted(df['Symbols'].unique())],
                         ),
            dcc.Graph(id='line-fig2', figure={})
        ],
            xs=12, sm=12, md=12, lg=5, xl=5
        ),

    ], justify='start'),

    dbc.Row([
        dbc.Col([
            html.P("Select Company Stock",
                   style={"textDecoration": "underline"}),
            dcc.Checklist(id='my-checklist', value=['FB', 'GOOGL', 'AMZN'],
                          options=[{'label': x, 'value': x}
                                   for x in sorted(df['Symbols'].unique())],
                          labelClassName='mr-3'),
            dcc.Graph(id='my-hist', figure={}),
        ],
            xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
            dbc.Card(
                [
                    dbc.CardBody(
                        html.P(
                            "we're better together. Help Each other out!",
                            className="card-text")
                    ),
                    dbc.CardImg(
                        src="https://media.giphy.com/media/Ll0jnPa6IS8eI/giphy.gif",
                        bottom=True),
                ],
                style={"width": "24rem"},
            )
        ],
            xs=12, sm=12, md=12, lg=5, xl=5
        )
    ], align="center")

}, fluid=True)


# Callback section: connecting the components
# ******************************************************************
# Line chart - Single

@app.callback(
    Output('line-fig', 'figure'),
    Input('my-dpdn', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'] == stock_slctd]
    figln = px.line(dff, x='Date', y='High')
    return figln


# Line chart - multiple
@app.callback(
    Output('line-fig2', 'figure'),
    Input('my-dpdn2', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    figln2 = px.line(dff, x='Date', y='Open', color='Symbols')
    return figln2


# Histogram
@app.callback(
    Output('my-hist', 'figure'),
    Input('my-checklist', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    dff = dff[dff['Date'] == '2021-12-13']
    fighist = px.histogram(dff, x='Symbols', y='Close')
    return fighist


if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
