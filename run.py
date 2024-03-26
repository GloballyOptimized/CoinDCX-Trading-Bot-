from functions import *
#.....................................................................................................
#The code below is just one of the deviced stratergy which can be altered according to need 
#......................................................................................................

balance = get_user_balance()

while balance < 50000:
   
    #................................................................................................
    balance_before = get_user_balance()                            #Checking balance before the trade executes
                                                                #for checking if the order is fulfilled

    #.................................................................................................
    order_data = create_order()     
    print(order_data)                               #Create the futures market order
    #.................................................................................................
    order_id = order_data[0]['id']     
    position_id = get_position_id()                           #Order id | Position ID | Buying Price 
    order_price = order_data[0]['price']
    #.................................................................................................

    current_trend = coin_candlestick_trend()
    if current_trend == 'buy':
        order_tp = order_price+(round((order_price*0.0025),2))        #Values when the market trend is to buy 
        order_sl = order_price-(round((order_price*0.0025),2))

    elif current_trend == 'sell':
        order_tp = order_price-(round((order_price*0.0025),2))
        order_sl = order_price+(round((order_price*0.0025),2))         #Values when the market trednis to sell 

    #..................................................................................................
    '''o_id = get_order_id()
    while True:
        if order_status(o_id) != 'filled':
            time.sleep(0.5)                  
            print('we stuck at order id')                      #Checking if the order is actually listed to the market or not 
        else:
            break'''
    
    while True:
        if get_position_data() > 0:
            break
        else:
            time.sleep(3)
    #...................................................................................................
    print(order_tp,order_sl)
    tpsl_data = take_profit_stop_loss(trade_id=position_id,
                                    stop_loss=order_sl,          #Take profit and stop loss setting 
                                    take_profit=order_tp)
    
    time.sleep(6)
    
    #....................................................................................................

    while True:
        if get_position_data() == 0:
            break
        else:
            time.sleep(10)
    #.......................................................................................................
                                                                 
    time.sleep(time_to_bid())                                    #Time to let the market move before next trade

    #.........................................................................................................