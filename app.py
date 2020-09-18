import json, requests
import datetime
from web3 import Web3, HTTPProvider

#sets up web3
url= 'https://sandbox.truffleteams.com/8f7572d1-e253-420a-93bc-2ed8a6f051e6'
web3 = Web3(HTTPProvider(url))

acc=web3.eth.accounts
user, charity, store = acc[:3]

headers=['TimestampEST', 'From', 'To', 'Continent', 'Value', 'Memo', 'TxnHash']
continents=['Asia', 'Africa', 'North America', 'South America', 'Antarctica', 'Europe', 'Australia']

links=[
    'https://drive.google.com/file/d/1Q7t6vPKjGSztqW0pa7XvFiBoM6lf4TNx/view?usp=sharing',
    'https://drive.google.com/file/d/1fMeRkSb2ft8-WZm8TfLBrGNMBvCOxDeF/view?usp=sharing',
    'https://drive.google.com/file/d/1eo4OEBJguToG-E1GzX6ha2hMonV9Ei-C/view?usp=sharing'
]

def readtxt(orig_url):
    file_id = orig_url.split('/')[-2]
    dwn_url='https://drive.google.com/uc?export=download&id=' + file_id
    return requests.get(dwn_url).text

abi=json.loads(text[0])
bytecode=json.loads(text[1])['object']
address=text[2]

c=web3.eth.contract(abi=abi, address=address)
filt = c.eventFilter('trans', {'fromBlock': 0,'toBlock': 'latest'});

#FUNCTIONS FOR FRONTEND
import datetime, pytz
tz=pytz.timezone('America/Detroit')
now=lambda: datetime.datetime.now(tz).strftime("%m/%d/%Y, %H:%M:%S")

#transfers ether from user to charity and records it
def donate(continent, value): #value in wei
    web3.eth.defaultAccount=user
  
    hash=web3.eth.sendTransaction(
        {
            'to': charity,
            'value': value,
        }
    )
    
    c.functions.give(now(), charity, continent, value, '', hash.hex()).transact()

#transfers ether from charity to store and records it
def spend(continent, value, memo): #value in wei
    web3.eth.defaultAccount=charity
  
    hash=web3.eth.sendTransaction(
        {
            'to': store,
            'value': value,
        }
    )

    c.functions.take(now(), store, continent, value, memo, hash.hex()).transact()

#frontend layout
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
        html.H1('CryptoCharity Interface'),
    ], style=dict(textAlign='center')),

    html.Div([

        html.Div([
            html.H2('Donator Side'),

            html.Label('Area of Contribution: '),
            dcc.Dropdown(
                id='continent',
                options=[
                    dict(label=x, value=x)
                    for x in continents
                ],
            ),

            html.Br(),
            
            html.Label('Contribution Amount (wei): '),
            dcc.Input(id='amount', type='number'),

            html.Br(),
            html.Br(),
            
            html.Button('Donate', id='submit'),

            html.Div(id='receipt'),

        ], className="three columns"),

        html.Div([
            html.H2('Charity Side'),

            html.Label('Area of Withdrawal: '),
            dcc.Dropdown(
                id='continent1',
                options=[
                    dict(label=x, value=x)
                    for x in continents
                ],
            ),

            html.Br(),
            
            html.Label('Withdrawal Amount (wei): '),
            dcc.Input(id='amount1', type='number'),

            html.Br(),
            html.Br(),
            
            html.Label('Memo Line: '),
            dcc.Input(id='memo', type='text'),

            html.Br(),
            html.Br(),
            
            html.Button('Spend', id='submit1'),

            html.Div(id='receipt1'),

        ], className="three columns"),

        html.Div([
            html.H2('Balances'),
            
            DataTable(
                id='balances',
                columns=[
                    dict(name=x, id=x)
                    for x in ['Continent', 'Balance']
                ],
                
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'Continent'},
                        'textAlign': 'left'
                    }
                ],

                style_as_list_view=True,
            ),

            html.Br(),
            
            html.Button('Update Tables', id='submit2'),

        ], className="two columns"),

        html.Div([
            
            html.Img(src='https://cdn.discordapp.com/attachments/738150178153955339/739574691949314159/Crypto-2.png', style={'width':'33%'}),

        ], className="four columns", style=dict(textAlign='center')),

    ], className="row"),

    html.H2('Transactions'),

    DataTable(
        id='trans',
        columns=[
            dict(name=x, id=x)
            for x in headers
        ],
        data=[],
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        page_action="native",
        page_current= 0,
        page_size= 10,
    ),  
])

#FRONTEND CALLBACK FUNCTIONS
#when 'Donate' button is hit, user sends ether to charity
#transaction is recorded
@app.callback(
    [
        Output('receipt', 'children'),
    ],    
    [
        Input('submit', 'n_clicks'),
    ],
    [
        State('continent', 'value'),
        State('amount', 'value'),
    ]
)
def give(clicks, cont, amount):
    continent=continents.index(cont)

    donate(continent, amount)

    return [
        f'{cont}, {amount}',
    ]

#when 'Spend' button is hit, charity sends ether to store
#the 'store' represents all vendors to the charity
#transaction is recorded
@app.callback(
    [
        Output('receipt1', 'children'),
    ],    
    [
        Input('submit1', 'n_clicks'),
    ],
    [
        State('continent1', 'value'),
        State('amount1', 'value'),
        State('memo', 'value'),
    ]
)
def take(clicks, cont, amount, memo):
    continent=continents.index(cont)

    spend(continent, amount, memo)

    return [
        f'{cont}, {amount}, {memo}',
    ]

#fills Balances Table
@app.callback(
    [
        Output('balances', 'data'),
    ],    
    [
        Input('submit2', 'n_clicks'),
    ],
)
def getBals(clicks):
    data=[
        {
            'Continent': cont,
            'Balance': c.functions.bals(i).call()
        }
        for i, cont in enumerate(continents)
    ]

    return [
        data
    ]

#fills Transaction Table
@app.callback(
    [
        Output('trans', 'data'),
    ],    
    [
        Input('submit2', 'n_clicks'),
    ],
)
def getTrans(clicks):
    events=[dict(tran['args']) for tran in filt.get_all_entries()]
    for event in events:
        event['Continent']=continents[event['Continent']]

        for key in 'TxnHash Memo TimestampEST'.split():
            event[key]=event[key].decode('UTF-8')

    return [
        events
    ]

#driver
if __name__ == '__main__':
    app.run_server()
