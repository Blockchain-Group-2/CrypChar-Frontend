import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output
from dash_table import DataTable

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H1('Fake Charity Name'),

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
    html.Br(),
    html.Br(),
    
    html.Div(id='test'),
    html.Br(),
    
    html.Div(id='data'),
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
        Output('test', 'children'),
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
def test(clicks, continent, amount, data, columns):
    data.append(
        {
            key['id']: value
            for key, value
            in zip(columns, [time(), continent, amount, 'temp'])
        }
    )

    return [
        f'You want to give ${amount} to Fake Charity\'s {continent} Operations',
        data,
    ]

if __name__ == '__main__':
    app.run_server()
