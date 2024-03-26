
#A list of all the libraries imported for the task 
#.................................................................................
import hmac
import hashlib
import base64
import json
import time
import requests
from datetime import datetime
from credentials import *
#..................................................................................

#Tested and working fine for now ....
def get_coin_candlesticks(market_pair:str='B-BNB_USDT',time_interval:str='5',total_sticks:int=1):
    time_to = time.time()
    time_from = time_to-(total_sticks*300)
    url = "https://public.coindcx.com/market_data/candlesticks"
    query_params = {
        "pair": market_pair,  # similar to this format"B-MKR_USDT"
        "from": time_from,
        "to": time_to,
        "resolution": time_interval,  # '1' OR '5' OR '60' OR '1D'
        "pcode": "f"
    }
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        data = response.json()
        # Process the data as needed
    return(data)
 
#..........................................................................................................
    
#Tested and working fine for now ....    
def coin_candlestick_trend():
    rdata = get_coin_candlesticks()
    trade_open =(rdata['data'][0]['open'])
    trade_close =(rdata['data'][0]['close'])
    if trade_open - trade_close < 0:
        return('buy')
    else:
        return('sell')
#.........................................................................................................
    
# Tersted and working fine for now ...
def get_user_info(api_key=API_Key,secret_key=Secret_Key): #Tested and working fine 

    secret_bytes = bytes(secret_key,encoding='utf-8') #encoding the key for secure data transfer 
    # Generating a timestamp
    timeStamp = int(round(time.time() * 1000))

    body = {
    "timestamp": timeStamp
    }

    json_body = json.dumps(body, separators = (',', ':'))

    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

    url = "https://api.coindcx.com/exchange/v1/users/info"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': api_key,
        'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data = json_body, headers = headers)
    data = response.json()
    return(data)
#...............................................................................................

#Tested and working fine for now ....
def get_user_balance(api_key = API_Key,secret_key = Secret_Key): # Tested and working fine 
    secret_bytes = bytes(secret_key,encoding='utf-8') #encoding the key for secure data transfer 
    # Generating a timestamp
    timeStamp = int(round(time.time() * 1000))

    body = {
    "timestamp": timeStamp
    }

    json_body = json.dumps(body, separators = (',', ':'))

    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

    url = "https://api.coindcx.com/exchange/v1/users/balances"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': api_key,
        'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data = json_body, headers = headers)
    data = response.json()
    return float(data[2]['balance'])
#.........................................................................................................

# Tested and working fine....
def trade_quantity(leverage=20):

    price_data = get_coin_candlesticks()
    price = price_data['data'][0]['high']
    final_funds = float(get_user_balance())*leverage
    
    quantity = round(float((12)/price),2)
    return quantity
#..........................................................................................................

#
def order_status(order_id:str,secret=Secret_Key,key=API_Key):
    # python3
    secret_bytes = bytes(secret, encoding='utf-8')
    

    # Generating a timestamp.
    timeStamp = int(round(time.time() * 1000))

    body = {
    "id": order_id, # Enter your Order ID here.
    # "client_order_id": "2022.02.14-btcinr_1", # Enter your Client Order ID here.
    "timestamp": timeStamp
    }

    json_body = json.dumps(body, separators = (',', ':'))

    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

    url = "https://api.coindcx.com/exchange/v1/orders/status"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data = json_body, headers = headers)
    data = response.json()
    return(data['status'])


#..........................................................................................................

#Tested and working fine 
def time_to_bid():
    time_remains = (68-(time.time()%60))
    return time_remains

#............................................................................................................

def create_order(secret=Secret_Key,key=API_Key):
    # python3
    secret_bytes = bytes(secret, encoding='utf-8')

    # Generating a timestamp
    timeStamp = int(round(time.time() * 1000))

    body = {
            "timestamp":timeStamp , # EPOCH timestamp in seconds
            "order": {
            "side": coin_candlestick_trend(), # buy OR sell
            "pair": "B-BNB_USDT", # instrument.string
            "order_type": "market_order", # market_order OR limit_order 
            "total_quantity": trade_quantity(), #numerice value
            "leverage": 20, #numerice value
            "notification": "email_notification", # no_notification OR email_notification OR push_notification
            "hidden": False, # True or False
            "post_only": False, # True or False
            }
            }

    json_body = json.dumps(body, separators = (',', ':'))

    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

    url = "https://api.coindcx.com/exchange/v1/derivatives/futures/orders/create"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data = json_body, headers = headers)
    data = response.json()
    return(data)
#........................................................................................................................

def take_profit_stop_loss(trade_id:str,stop_loss:float,take_profit:float,secret=Secret_Key,key=API_Key):
    # python3
    secret_bytes = bytes(secret, encoding='utf-8')

    # Generating a timestamp
    timeStamp = int(round(time.time() * 1000))

    body = {
    "timestamp": timeStamp, # EPOCH timestamp in seconds
    "id": trade_id, # position.id
    "take_profit": {
        "stop_price":take_profit,
        "order_type": "take_profit_market" # take_profit_limit OR take_profit_market
    },
    "stop_loss": {
        "stop_price":stop_loss,
        #"limit_price": stop_loss, # required for stop_limit orders
        "order_type": "stop_market" # stop_limit OR stop_market
    }
    }


    json_body = json.dumps(body, separators = (',', ':'))

    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

    url = "https://api.coindcx.com/exchange/v1/derivatives/futures/positions/create_tpsl"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data = json_body, headers = headers)
    data = response.json()
    return(data)

#.................................................................................................................

def get_position_id(secret=Secret_Key,key=API_Key):
        # python3
    secret_bytes = bytes(secret, encoding='utf-8')

    # Generating a timestamp
    timeStamp = int(round(time.time() * 1000))

    body = {
            "timestamp":timeStamp , # EPOCH timestamp in seconds
            "page": "1", #no. of pages needed
            "size": "10" #no. of records needed
            }


    json_body = json.dumps(body, separators = (',', ':'))

    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

    url = "https://api.coindcx.com/exchange/v1/derivatives/futures/positions"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data = json_body, headers = headers)
    data = response.json()
    return(data[0]['id'])
    
#..............................................................................................................
def get_order_id(secret=Secret_Key,key=API_Key):
    # python3
    secret_bytes = bytes(secret, encoding='utf-8')

    # Generating a timestamp.
    timeStamp = int(round(time.time() * 1000))

    body = {
    "limit": 1,
    "timestamp": timeStamp,
    "sort": "asc",
    }

    json_body = json.dumps(body, separators = (',', ':'))

    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

    url = "https://api.coindcx.com/exchange/v1/orders/trade_history"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data = json_body, headers = headers)
    data = response.json()
    return(data[0]['order_id'])
#............................................................................................
def get_position_data(secret=Secret_Key,key=API_Key):
        # python3
    secret_bytes = bytes(secret, encoding='utf-8')

    # Generating a timestamp
    timeStamp = int(round(time.time() * 1000))

    body = {
            "timestamp":timeStamp , # EPOCH timestamp in seconds
            "page": "1", #no. of pages needed
            "size": "1" #no. of records needed
            }


    json_body = json.dumps(body, separators = (',', ':'))

    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

    url = "https://api.coindcx.com/exchange/v1/derivatives/futures/positions"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data = json_body, headers = headers)
    data = response.json()
    return(data[0]['active_pos'])

#.......................................................................................................

def cancle_all_open_orders(key=API_Key,secret=Secret_Key):
    
    # python3
    secret_bytes = bytes(secret, encoding='utf-8')

    # Generating a timestamp
    timeStamp = int(round(time.time() * 1000))

    body = {
    "timestamp": timeStamp  
    }

    json_body = json.dumps(body, separators = (',', ':'))

    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

    url = "https://api.coindcx.com/exchange/v1/derivatives/futures/positions/cancel_all_open_orders_for_position"

    headers = {
    'Content-Type': 'application/json',
    'X-AUTH-APIKEY': key,
    'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data = json_body, headers = headers)
    data = response.json()
    return(data)