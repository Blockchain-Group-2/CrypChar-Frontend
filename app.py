import json
from web3 import Web3, HTTPProvider

url= 'https://sandbox.truffleteams.com/8f7572d1-e253-420a-93bc-2ed8a6f051e6'

web3 = Web3(HTTPProvider(url))

acc=web3.eth.accounts
acc

user, charity, store = acc[:3]

continents=['Asia', 'Africa', 'North America', 'South America', 'Antarctica', 'Europe', 'Australia']

abi = [ { "inputs": [], "stateMutability": "nonpayable", "type": "constructor" }, { "anonymous": False, "inputs": [ { "indexed": False, "internalType": "address", "name": "sender", "type": "address" }, { "indexed": False, "internalType": "address", "name": "receiver", "type": "address" }, { "indexed": False, "internalType": "uint256", "name": "continent", "type": "uint256" }, { "indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256" }, { "indexed": False, "internalType": "bytes", "name": "memo", "type": "bytes" } ], "name": "t", "type": "event" }, { "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "balances", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "i", "type": "uint256" } ], "name": "get", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "i", "type": "uint256" } ], "name": "getBalance", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "payable", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "hash", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "i", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "num", "type": "uint256" } ], "name": "store", "outputs": [ { "internalType": "bool", "name": "success", "type": "bool" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "receiver", "type": "address" }, { "internalType": "uint256", "name": "to", "type": "uint256" }, { "internalType": "uint256", "name": "value", "type": "uint256" }, { "internalType": "string", "name": "memo", "type": "string" } ], "name": "transfer", "outputs": [ { "internalType": "bool", "name": "success", "type": "bool" } ], "stateMutability": "payable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "receiver", "type": "address" }, { "internalType": "uint256", "name": "to", "type": "uint256" }, { "internalType": "uint256", "name": "value", "type": "uint256" }, { "internalType": "string", "name": "memo", "type": "string" } ], "name": "withdraw", "outputs": [ { "internalType": "bool", "name": "success", "type": "bool" } ], "stateMutability": "payable", "type": "function" } ]

address = '0x6df678325114CaaA7CAC9cf3C75B1a06BF916971'

contract = web3.eth.contract(address=address, abi=abi)

def donate(continent, value): #value in wei
    web3.eth.defaultAccount=user

    if value>web3.eth.getBalance(user):
        return False

    hash=contract.functions.transfer(charity, continents.index(continent), value, '').transact()
    contract.functions.store(int(web3.toHex(hash), 16)).transact()

    return web3.eth.sendTransaction(
        {
            'to': charity,
            'value': value,
        }
    )

def spend(continent, amount, memo):
    web3.eth.defaultAccount=charity

    if amount>contract.functions.getBalance(continents.index(continent)).call():
        return False

    hash=contract.functions.withdraw(store, continents.index(continent), amount, memo).transact()
    contract.functions.store(int(web3.toHex(hash), 16)).transact()

    return web3.eth.sendTransaction(
        {
            'to': store,
            'value': amount,
        }
    )

def getRow(hash):
    event=dict(contract.events.t().processReceipt(web3.eth.getTransactionReceipt(hex(hash)))[0]['args'])

    event['memo']=event['memo'].decode('utf-8')
    event['continent']=continents[event['continent']]

    return event

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
            
            html.Button('Submit', id='submit'),

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
            
            html.Button('Submit', id='submit1'),

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

                style_as_list_view=True,
            ),

        ], className="two columns"),

        html.Div([
            
            html.Img(src='https://cdn.discordapp.com/attachments/738150178153955339/739574691949314159/Crypto-2.png', style={'width':'33%'}),

        ], className="four columns", style=dict(textAlign='center')),

    ], className="row"),

    html.H2('Transactions'),

    DataTable(
        id='trans',
        columns=[
            dict(name=x, id=x.lower())
            for x in ['Sender', 'Receiver', 'Continent', 'Amount', 'Memo']
        ],
        data=[],

        style_as_list_view=True,
    ),  
])

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
def give(clicks, continent, amount):
    donate(continent, amount)

    return [
        f'{continent}, {amount}',
    ]

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
def take(clicks, continent, amount, memo):
    spend(continent, amount, memo)

    return [
        f'{continent}, {amount}, {memo}',
    ]

@app.callback(
    [
        Output('balances', 'data'),
    ],    
    [
        Input('submit', 'n_clicks'),
        Input('submit1', 'n_clicks'),
    ],
)
def getBal(a, b):
    data=[
        {
            'Continent': cont,
            'Balance': contract.functions.getBalance(i).call()
        }
        for i, cont in enumerate(continents)
    ]

    return [
        data
    ]

@app.callback(
    [
        Output('trans', 'data'),
    ],    
    [
        Input('submit', 'n_clicks'),
        Input('submit1', 'n_clicks'),
    ],
    [
        State('trans', 'data'),
    ],    
)
def getTran(a, b, data):
    hashes=[]

    for i in range(len(data), 2**22):
        hash=contract.functions.get(i).call()

        if hash==0:
            break
        
        hashes.append(hash)    

    return [
        data+[getRow(hash) for hash in hashes]
    ]


if __name__ == '__main__':
    app.run_server()
