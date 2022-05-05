from flask import Flask, request, abort
import requests
import json
from .Config import *
from uncleengineer import thaistock
import ccxt


app = Flask(__name__)

binance = ccxt.binance({
    'apiKey': api_key, 'secret': binance_secret_key, 'enableRateLimit': True,
})

def GET_BTC_PRICE():
    data = binance.fetch_tickers('BTC/USDT')['BTC/USDT']['ask']
    BTC_PRICE = data
    return BTC_PRICE

def GET_DOGE_PRICE():
    data = binance.fetch_tickers('DOGE/USDT')['DOGE/USDT']['ask']
    DOGE_PRICE = data
    return DOGE_PRICE

def GET_ETH_PRICE():
    data = binance.fetch_tickers('ETH/USDT')['ETH/USDT']['ask']
    ETH_PRICE = data
    return ETH_PRICE

def GET_BNB_PRICE():
    data = binance.fetch_tickers('BNB/USDT')['BNB/USDT']['ask']
    BNB_PRICE = data
    return BNB_PRICE

def GET_XRP_PRICE():
    data = binance.fetch_tickers('XRP/USDT')['XRP/USDT']['ask']
    XRP_PRICE = data
    return XRP_PRICE

def GET_LUNA_PRICE():
    data = binance.fetch_tickers('LUNA/USDT')['LUNA/USDT']['ask']
    LUNA_PRICE = data
    return LUNA_PRICE

def GET_SOL_PRICE():
    data = binance.fetch_tickers('SOL/USDT')['SOL/USDT']['ask']
    SOL_PRICE = data
    return SOL_PRICE

@app.route('/webhook', methods=['POST','GET'])
def webhook():
    if request.method == 'POST':
        payload = request.json

        Reply_token = payload['events'][0]['replyToken']
        print(Reply_token)
        message = payload['events'][0]['message']['text']
        print(message)
        if 'หุ้น' in message :
            ITD = thaistock('ITD')
            Reply_messasge = 'ราคาหุ้น อิตาเลียนไทย ขณะนี้ : {}'.format(ITD)
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        
        elif "btc" in message :
            Reply_messasge = 'ราคา BITCOIN ขณะนี้ : {} usdt'.format(GET_BTC_PRICE())
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        elif "doge" in message :
            Reply_messasge = 'ราคา DOGECOIN ขณะนี้ : {} usdt'.format(GET_DOGE_PRICE())
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        elif "eth" in message :
            Reply_messasge = 'ราคา ETH ขณะนี้ : {} usdt'.format(GET_ETH_PRICE())
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        elif "bnb" in message :
            Reply_messasge = 'ราคา BNB ขณะนี้ : {} usdt'.format(GET_BNB_PRICE())
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        elif "xrp" in message :
            Reply_messasge = 'ราคา XRP ขณะนี้ : {} usdt'.format(GET_XRP_PRICE())
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        elif "luna" in message :
            Reply_messasge = 'ราคา LUNA ขณะนี้ : {} usdt'.format(GET_LUNA_PRICE())
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        elif "sol" in message :
            Reply_messasge = 'ราคา SOL ขณะนี้ : {} usdt'.format(GET_SOL_PRICE())
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)


        return request.json, 200

    elif request.method == 'GET' :
        return 'this is method GET!!!' , 200

    else:
        abort(400)

@app.route('/')
def hello():
    return 'hello world book',200

def ReplyMessage(Reply_token, TextMessage, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format(Line_Acees_Token) ##ที่ยาวๆ
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization':Authorization
    }

    data = {
        "replyToken":Reply_token,
        "messages":[{
            "type":"text",
            "text":TextMessage
        }]
    }

    data = json.dumps(data) ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data) 
    return 200