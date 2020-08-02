from dash import Dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State
from dash_table import DataTable

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.Div([
        html.Div([

            html.Img(src='https://document-export.canva.com/DAEDvhGXJhI/396/preview/0001-9164315689.png', style={'width':'100%'}),

        ], className="three columns"),

        html.Div([

            html.Label('Area of Contribution: '),
            dcc.Dropdown(
                id='continent',
                options=[
                    dict(label=x, value=x)
                    for x in ['North America', 'South America', 'Europe', 'Africa', 'Asia', 'Australia', 'Antarctica']
                ],
            ),

            html.Br(),
            
            html.Label('Contribution Amount ($): '),
            dcc.Input(id='amount', type='number'),

            html.Br(),
            html.Br(),
            
            html.Button('Submit', id='submit'),

            html.Div(id='receipt'),

        ], className="two columns"),
    ], className="row"),

    html.Br(),

    DataTable(
        id='table',
        columns=[
            dict(name=x, id=x)
            for x in ['Timestamp', 'Continent', 'Amount', 'Address']
        ],
        data=[],
    ),
])

import datetime
time = lambda: datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")

@app.callback(
    [
        Output('receipt', 'children'),
        Output('table', 'data'),
    ],    
    [
        Input('submit', 'n_clicks'),
    ],
    [
        State('continent', 'value'),
        State('amount', 'value'),
        State('table', 'data'),
        State('table', 'columns'),
    ]
)
def submit(clicks, continent, amount, data, columns):
    if clicks==None:
        return [
            '',
            [],
        ]

    data.append(
        {
            key['id']: value
            for key, value
            in zip(columns, [time(), continent, amount, 'temp'])
        }
    )

    return [
        f'You want to give ${amount} to CryptoCharity\'s {continent} Operations',
        data,
    ]

if __name__ == '__main__':
    app.run_server()
