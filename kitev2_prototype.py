import logging
from kiteconnect import KiteTicker
from kiteconnect import KiteConnect
import numpy as np
import datetime as dt
import sys
import time
import os
import math
from sys import exit
from time import sleep
import pandas as pd

logging.basicConfig(level=logging.DEBUG)

#Getting key and secret
keyFileName = input( "Enter name of key file: " )               #Input key file name/path(Keep key file in folder for no path)
keyFile = open( keyFileName,'r' )                               #Open the key file
api_key = keyFile.readline().replace( "\n" , "" )               #Get first line and remove newline characters
api_secret = keyFile.readline().replace( "\n" , "" )            #Get second line and remove newline characters
keyFile.close()                                                 #Close the open key file

accessTokenFile = open( "access_token.txt" , "r" )              #Open accessTokenFile created by access_token program
access_token = accessTokenFile.readline().replace( "\n" , "" )  #Get and store access_token
accessTokenFile.close()                                         #Close accessTokenFile

#Initialise
kite = KiteConnect(api_key= api_key)                            #Initiate KiteConnection
kws = KiteTicker( api_key, access_token )                       #Initiate KiteTicker

################################################################ GLOBAL VARIABLES ################################################################

stock_name = ""                                                     #Initialise name of stock eg.CRUDEOIL,TATASTEEL etc.

exchange_code =  ""                                                 #Initialise the name of exchange eg NSE,BSE,NFO,BFO,MCX etc.

expiry_year = ""                                                    #Year of expiry of stock/future/option/commodity
expiry_month = ""                                                   #Month of expirt of stock/future/option/commodity

product_type = ""                                                   #Initialise type of product eg. NRML,MIS etc.

lot_size = 0                                                        #Initialise the size of the lot

spike_threshold = 0                                                 #Initialise the spike rise/dip threshold

order_type = ""                                                     #Initialise the type of order eg. MARKET,LIMIT

strategy_switch = ""                                                #Initialise the switch of strategy eg. MVA, MOM etc

upper_difference_limit = 0.0                                        #Initialise the upper difference limit
lower_difference_limit = 0.0                                        #Initialise the lower difference limit
square_off_difference_limit = 0.0                                   #Initialise the difference limit during square off
max_loss_limit = 0.0                                                #Initialise the max loss allowed limit

moving_average_short_array_size = 0                                 #Initialise the size of array used for moving_average->short calculation and analysis
moving_average_long_array_size = 0                                  #Initialise the size of array used for moving_average->long calculation and analysis
volume_difference_array_size = 0                                    #Initialise the size of array used for volume difference calculation and analysis
price_difference_array_size = 0                                     #Initialise the size of array used for price difference calculation and analysis

online_offline_switch = ""                                          #Initialise the flag representing offline and online mode switch
directional_switch = ""                                             #Initialise the switch for directional orders eg. BI Directional or UNI directional

first_position_type = ""                                            #Initialise the type of position (for first stream) eg.FUT,CE,PE,EQ
first_instrument_code = 0                                           #Initialise the instrument code for first stream subscription
first_position_offer_price = 0.0                                    #Initialise the variable to store the first position offer price
first_position_bid_price = 0.0                                      #Initialise the variable to store the first position bid price    
first_position_volume = 0                                           #Initialise the variable to store the first position volume
first_position_last_traded_price = 0.0                              #Initialise the variable to store the first position last traded price
 
second_position_type = ""                                           #Initialise the type of position (for second stream) eg.FUT,CE,PE,EQ
second_instrument_code = 0                                          #Initialise the instrument code for second stream subscription 
second_position_offer_price = 0.0                                   #Initialise the variable to store the second position offer price
second_position_bid_price = 0.0                                     #Initialise the variable to store the second position bid price
second_position_volume = 0                                          #Initialise the variable to store the second position volume
second_position_last_traded_price = 0.0                             #Initialise the variable to store the second position last traded price

ce_instrument_code = 0                                              #Initialise the instrument code for call option of stock/commodity
ce_strike_rate = 0                                                  #Initialise the strike rate for call option of stock/commodity
ce_offer_price = 0.0                                                #Initialise the variable to store the call option offer price
ce_bid_price = 0.0                                                  #Initialise the variable to store the call option bid price
ce_volume = 0                                                       #Initialise the variable to store the call option volume
ce_last_traded_price = 0.0                                          #Initialise the variable to store the call option last traded price

pe_instrument_code = 0                                              #Initialise the instrument code for put  option of stock/commodity
pe_strike_rate = 0                                                  #Initialise the stirke rate for put option of stock/commodity
pe_offer_price = 0.0                                                #Initialise the variable to store the put option offer price
pe_bid_price = 0.0                                                  #Initialise the variable to store the put option bid price
pe_volume = 0                                                       #Initialise the variable to store the put option volume
pe_last_traded_price = 0.0                                          #Initialise the variable to store the put option last traded price

iteration_pointer = 0                                               #Initialize the variable to store the iterator/iteration

data_file_name = ""                                                 #Initialise the variable to store the name of the offline input data file

################################################################ INPUT TEMPLATE FUNCTION ################################################################

def input_template():                                                      #Function to take i/p file and set the necessry variables
        #Set up the global variable names used in this function
    global stock_name, exchange_code, expiry_year, expiry_month, product_type, lot_size, spike_threshold, order_type, online_offline_switch #General global variables
    global directional_switch, strategy_switch, data_file_name                                                                              #General global variables
    global first_instrument_code, first_position_type                                                                                       #First position variables
    global second_instrument_code, second_position_type                                                                                     #Second position variables
    global ce_instrument_code, ce_strike_rate                                                                                               #Call option variables
    global pe_instrument_code, pe_strike_rate                                                                                               #Put option variables
    global upper_difference_limit, lower_difference_limit,square_off_difference_limit, max_loss_limit                                       #Difference-Limit Variables
    global moving_average_long_array_size, moving_average_short_array_size, volume_difference_array_size, price_difference_array_size       #Array Size Variables
     
    inputFileName = input("Enter the name of input template file: ")    #Enter name of i/p template file
    inputFile = pd.read_csv(inputFileName)                              #Use given name to open file and convert to pandas->dataframe   
     
    stock_name = str(inputFile.ix[0,1])                                 #Store name of stock eg.CRUDEOIL,TATASTEEL etc.
     
    exchange_code =  str(inputFile.ix[1,1])                             #Store the name of exchange eg NSE,BSE,NFO,BFO,MCX etc.
     
    expiry_year = "18"                                                  #Year of expiry of stock/future/option/commodity
    expiry_month = str(inputFile.ix[2,1])                               #Month of expirt of stock/future/option/commodity
     
    product_type = str(inputFile.ix[3,1])                               #Store type of product eg. NRML,MIS etc.
     
    lot_size = int(inputFile.ix[4,1])                                   #Store the size of the lot
     
    spike_threshold = int(inputFile.ix[5,1])                            #Store the spike rise/dip threshold
     
    first_position_type = str(inputFile.ix[6,1])                        #Store the type of position (for first stream) eg.FUT,CE,PE,EQ
    second_position_type = str(inputFile.ix[7,1])                       #Store the type of position (for second stream) eg.FUT,CE,PE,EQ
     
    online_offline_switch = str(inputFile.ix[8,1])                      #Store the flag representing offline and online mode switch
     
    order_type = str(inputFile.ix[9,1])                                 #Store the type of order eg. MARKET,LIMIT
     
    directional_switch = str(inputFile.ix[10,1])                        #Store the switch for directional orders eg. BI Directional or UNI directional
      
    upper_difference_limit = float(inputFile.ix[11,1])                  #Store the upper difference limit
    lower_difference_limit = float(inputFile.ix[12,1])                  #Store the lower difference limit
    square_off_difference_limit = float(inputFile.ix[13,1])             #Store the difference limit during square off
    max_loss_limit = float(inputFile.ix[14,1])                          #Store the max loss allowed limit
     
    moving_average_short_array_size = int(inputFile.ix[15,1])           #Store the size of array used for moving_average->short calculation and analysis
    moving_average_long_array_size = int(inputFile.ix[16,1])            #Store the size of array used for moving_average->long calculation and analysis
    volume_difference_array_size = int(inputFile.ix[17,1])              #Store the size of array used for volume difference calculation and analysis
    price_difference_array_size = int(inputFile.ix[17,1])               #Store the size of array used for price difference calculation and analysis
     
    strategy_switch = str(inputFile.ix[18,1])                           #Store the switch of strategy eg. MVA, MOM etc
     
    first_instrument_code = int(inputFile.ix[19,1])                     #Store the instrument code for first stream subscription 
    second_instrument_code = int(inputFile.ix[20,1])                    #Store the instrument code for second stream subscription 
     
    ce_instrument_code = int(inputFile.ix[21,1])                        #Store the instrument code for call option of stock/commodity
    ce_strike_rate = int(inputFile.ix[22,1])                            #Store the strike rate for call option of stock/commodity
     
    pe_instrument_code = int(inputFile.ix[23,1])                        #Store the instrument code for put option of stock/commodity
    pe_strike_rate = int(inputFile.ix[24,1])                            #Store the strike rate for put option of stock/commodity 
      
    print("Inputted template file: ")                                   #Print the pandas->dataframe storing the input template file
    print(inputFile)
    inputFile.close()                                                   #Close the input template file
     
    data_file_name = stock_name + "_INPUT_DATA_FILE.csv"
     
    local_date = dt.datetime.now().date()                               #Get current date
    outputFileName = stock_name + "_OUTPUT_DATA_" + str(local_date) + ".csv"        #Create specified file name 
    outputFile = open(outputFileName, "a")                                          #Open/Create file in write/append mode with specified file name
        #Create a template for output file
    outputFile.write("Time,")
    outputFile.write(" First Position Offer Price, First Position Bid Price, First Position Last Traded Price, First Position Volume,")
    outputFile.write(" Second Position Offer Price, Second Position Bid Price, Second Position Last Traded Price, Second Position Volume,")
    outputFile.write(" CE Offer Price, CE Bid Price, CE Last Traded Price,")
    outputFile.write(" PE Offer Price, PE Bid Price, PE Last Traded Price")
    outputFile.close()                                                              #Close the output template file
#End of Function

################################################################ ONLINE/OFFLINE SWITCH HANDLING ################################################################

def switch_streams():                                                                       #Function to decide whether to run in online/offline mode
    #Set up the global variable names used in this function
    global online_offline_switch, kws                                                       #General Global Variables
     
    if online_offline_switch == "ON" :                                                      #For Online Stream
        confirm_stream = str(input("Online stream mode. Please confirm(Y/N): "))            #Confirm if Intention was Online streaming
        if(confirm_stream == "Y" or confirm_stream == "y") :
            # Assign the callbacks.
            kws.on_ticks = on_ticks                                                         #Call and start the online stream data gathering function
            kws.on_connect = on_connect                                                     #Connect to the online WebSocket stream
            #kws.on_close = on_close                                                        #For Closing connection

            # Infinite loop on the main thread. Nothing after this will run.
            # You have to use the pre-defined callbacks to manage subscriptions.
            
            kws.connect()                                                                   #Start the connection
        else :
            break                                                                           #If not intention for online stream, break and exit program

    elif online_offline_switch == "OFF" :                                                   #For Offline Stream
        confirm_stream = str(input("Offline stream mode. Please confirm(Y/N): "))           #Confirm if Intention was Offline testing
        if(confirm_stream == "N" or confirm_stream == "n") :                                
            offline_stream_simulation()                                                     #Call the Offline test data gathering function
        else :
            break                                                                           #If not intention for offline stream, break and exit program
    else :
        print("Invalid input. Please change switch parameter in the input template file.")  #If invalid input print error message and exit program
        break
#End of Function
    
################################################################ ONLINE DATA GATHERING FUNCTION ################################################################    
    
def on_ticks(ws, ticks):                                                                    #Function to gather online stream data
        #Global variables required
    global first_instrument_code, first_position_offer_price, first_position_bid_price, first_position_volume, first_position_last_traded_price        #First Position Variables
    global second_instrument_code, second_position_offer_price, second_position_bid_price, second_position_volume, second_position_last_traded_price   #Second Position Variables
    global ce_instrument_code, ce_offer_price, ce_bid_price, ce_volume, ce_last_traded_price                                                           #Call Option Variables
    global pe_instrument_code, pe_offer_price, pe_bid_price, pe_volume, pe_last_traded_price                                                           #Put Option Variables
    
        #First instrument stream data collection    
    if(ticks[0]['instrument_token'] == int(first_instrument_code)):                     #Match the incoming stream data's instrument code to that of first position instrument code
        first_position_offer_price = ticks[0]['depth']['sell'][0]['price']                  #Store the first position's offer price
        first_position_bid_price = ticks[0]['depth']['buy'][0]['price']                     #Store the first position's bid price
        first_position_volume = ticks[0]['volume']                                          #Store the first position's traded volume
        first_position_last_traded_price = ticks[0]['last_price']                           #Store the first position's last traded price

        #Second instrument stream data collection    
    if(ticks[0]['instrument_token'] == int(second_instrument_code)):                    #Match the incoming stream data's instrument code to that of second position instrument code
        second_position_offer_price = ticks[0]['depth']['sell'][0]['price']                  #Store the second position's offer price
        second_position_bid_price = ticks[0]['depth']['buy'][0]['price']                     #Store the second position's bid price
        second_position_volume = ticks[0]['volume']                                          #Store the second position's traded volume
        second_position_last_traded_price = ticks[0]['last_price']                           #Store the second position's last traded price

        #Call Option instrument stream data collection    
    if(ticks[0]['instrument_token'] == int(ce_instrument_code)):                        #Match the incoming stream data's instrument code to that of Call Option instrument code
        ce_offer_price = ticks[0]['depth']['sell'][0]['price']                              #Store the Call Option's offer price
        ce_bid_price = ticks[0]['depth']['buy'][0]['price']                                 #Store the Call Option's bid price
        ce_volume = ticks[0]['volume']                                                      #Store the Call Option's traded volume
        ce_last_traded_price = ticks[0]['last_price']                                       #Store the Call Option's last traded price 

        #Put Option instrument stream data collection    
    if(ticks[0]['instrument_token'] == int(pe_instrument_code)):                        #Match the incoming stream data's instrument code to that of Put Option instrument code
        pe_offer_price = ticks[0]['depth']['sell'][0]['price']                              #Store the Put Option's offer price
        pe_bid_price = ticks[0]['depth']['buy'][0]['price']                                 #Store the Put Option's bid price
        pe_volume = ticks[0]['volume']                                                      #Store the Put Option's traded volume
        pe_last_traded_price = ticks[0]['last_price']                                       #Store the Put Option's last traded price       
    
    data_analyze()
#End of Function 
 
################################################################ ONLINE OPEN CONNECTION FUNCTION ################################################################
    
def on_connect(ws, response):                                                               #Function to subscribe to instruments and set mode of incoming stream data
        #Global Variable Declaration
    global first_instrument_code                                                #First position instrument code global variable
    global second_instrument_code                                               #Second position instrument code global variable
    global ce_instrument_code                                                   #Call Option instrument code global variable
    global pe_instrument_code                                                   #Put Option instrument code global variable
       
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens.
    ws.subscribe([int(first_instrument_code)])                                  #Subscribe to first instrument token
    ws.subscribe([int(second_instrument_code)])                                 #Subscribe to second instrument token
    ws.subscribe([int(ce_instrument_code)])                                     #Subscribe to CE instrument token
    ws.subscribe([int(pe_instrument_code)])                                     #Subscribe to PE instrument token
       
    # Set instrument to tick in `full` mode.
    ws.set_mode(ws.MODE_FULL, [first_instrument_code])                          #Set first online input stream to full mode
    ws.set_mode(ws.MODE_FULL, [second_instrument_code])                         #Set second online input stream to full mode
    ws.set_mode(ws.MODE_FULL, [ce_instrument_code])                             #Set ce online input stream to full mode
    ws.set_mode(ws.MODE_FULL, [pe_instrument_code])                             #Set pe online input stream to full mode
#End of Function

################################################################ ONLINE CLOSE CONNECTION FUNCTION ################################################################

def on_close(ws, code, reason):                                                             #Function to handle closing of the stream connection
    # On connection close stop the main loop
    # Reconnection will not happen after executing `ws.stop()`
    ws.stop()
#End of Function

################################################################ OFFLINE STREAM SIMULATOR ################################################################
    
def offline_stream_simulation():                                                            #Function to simulate streaming of data in offline mode
    global iteration_pointer, data_file_name                                                                                       #General global variables
      
    offline_stream_input_dataframe = pd.read_csv( data_file_name, parse_dates = True )
      
    while iteration_pointer in range (len(offline_stream_input_dataframe)):                     #Iterating the dataframe which holds the offline input data
        off_ticks(offline_stream_input_dataframe)                                               #Calling the function to load data from offline input data into global variables
        iteration_pointer = iteration_pointer + 1                                               #iterating forward
#End of Function

################################################################ OFFLINE DATA GATHERING FUNCTION ################################################################    
    
def off_ticks(offline_stream_input_dataframe = pd.DataFrame()):                             #Function to gather offline test data
    #Global variables required
    global stock_name, data_file_name, iteration_pointer                                                                           #General global variables
    global first_position_offer_price, first_position_bid_price, first_position_volume, first_position_last_traded_price           #First Position Variables
    global second_position_offer_price, second_position_bid_price, second_position_volume, second_position_last_traded_price       #Second Position Variables
    global ce_offer_price, ce_bid_price, ce_volume, ce_last_traded_price                                                           #Call Option Variables
    global pe_offer_price, pe_bid_price, pe_volume, pe_last_traded_price                                                           #Put Option Variables
     
    #First instrument stream data collection    
    first_position_offer_price = float(offline_stream_input_dataframe.ix[iteration_pointer,1])                  #Store the first position's offer price
    first_position_bid_price = float(offline_stream_input_dataframe.ix[iteration_pointer,2])                    #Store the first position's bid price
    first_position_volume = int(offline_stream_input_dataframe.ix[iteration_pointer,3])                         #Store the first position's traded volume
    first_position_last_traded_price = float(offline_stream_input_dataframe.ix[iteration_pointer,4])            #Store the first position's last traded price
     
    #Second instrument stream data collection    
    second_position_offer_price = float(offline_stream_input_dataframe.ix[iteration_pointer,5])                 #Store the first position's offer price
    second_position_bid_price = float(offline_stream_input_dataframe.ix[iteration_pointer,6])                   #Store the first position's bid price
    second_position_volume = int(offline_stream_input_dataframe.ix[iteration_pointer,7])                        #Store the first position's traded volume
    second_position_last_traded_price = float(offline_stream_input_dataframe.ix[iteration_pointer,8])           #Store the first position's last traded price
     
    #Call Option instrument stream data collection    
    ce_offer_price = float(offline_stream_input_dataframe.ix[iteration_pointer,9])                              #Store the first position's offer price
    ce_bid_price = float(offline_stream_input_dataframe.ix[iteration_pointer,10])                               #Store the first position's bid price
    ce_volume = int(offline_stream_input_dataframe.ix[iteration_pointer,11])                                    #Store the first position's traded volume
    ce_last_traded_price = float(offline_stream_input_dataframe.ix[iteration_pointer,12])                       #Store the first position's last traded price
     
    #Put Option instrument stream data collection    
    pe_offer_price = float(offline_stream_input_dataframe.ix[iteration_pointer,13])                             #Store the first position's offer price
    pe_bid_price = float(offline_stream_input_dataframe.ix[iteration_pointer,14])                               #Store the first position's bid price
    pe_volume = int(offline_stream_input_dataframe.ix[iteration_pointer,15])                                    #Store the first position's traded volume
    pe_last_traded_price = float(offline_stream_input_dataframe.ix[iteration_pointer,16])                       #Store the first position's last traded price
        
    data_analyze()
#End of Function 

################################################################ DATA ANALYSIS FUNCTION ################################################################

def data_analyze():                                                                         #Function to analyze the gathered data based on pre-determined parameter
    #Placeholder
    
################################################################ DECISION MAKING FUNCTION ################################################################

def decide_buy_sell():                                                                      #Function to use the analyzed data to decide whether to buy or to sell
    #Placeholder
    
################################################################ BUY ORDER FUNCTION ################################################################

def buy():                                                                                  #Function to place Buy order using given parameters
    #Placeholder
    
################################################################ SELL ORDER FUNCTION ################################################################

def sell():                                                                                 #Function to place Sell order using given parameters
    #Placeholder
    
################################################################ OUTPUT TO FILE FUNCTION ################################################################

def output_template(offline_stream_input_dataframe = pd.DataFrame()):                       #Function to output the stream data into a file for later testing and analysis
        #Global Varibale Declaration
    global stream_switch, iteration_pointer                                                                                     #General global variables
    global data_file_name                                                                                                       #Offline stream global variables
    global first_position_offer_price, first_position_bid_price, first_position_volume,first_position_last_traded_price         #First Position global variables
    global second_position_offer_price, second_position_bid_price, second_position_volume, second_position_last_traded_price    #Second Position global variables
    global ce_offer_price, ce_bid_price, ce_volume, ce_last_traded_price                                                        #Call Option global variables
    global pe_offer_price, pe_bid_price, pe_volume, pe_last_traded_price                                                        #Put Option global variables
    
        #Check the switch so as to get proper timestamp
    if(stream_switch == "OFF"):                                                     #If stream switch is set to off   
        localtime = offline_stream_input_dataframe.ix[iteration_pointer,0]                  #Get the corresponding timestamp for the current iteration
    elif(stream_switch == "ON"):                                                    #If stream switch is set to on
        localtime = time.asctime( time.localtime(time.time()) )                             #Get the current timestamp
    
    local_date = dt.datetime.now().date()                                                   #Get and Store th current data
    outputFileName = stock_name + "_OUTPUT_DATA_" + str(local_date) + ".csv"                #Create the specified file name
    outputFile = open(outputFileName, "a")                                                  #Open the file with specified file name
    
        #Write the data gathered of current iteration into the output file
    outputFile.write( str(localtime) + ", " )        
    outputFile.write( str(first_position_offer_price) + ", " + str(first_position_bid_price) + ", " + str(first_position_volume) + ", " + str(first_position_last_traded_price) + ", " )
    outputFile.write( str(second_position_offer_price) + ", " + str(second_position_bid_price) + ", " + str(second_position_volume) + ", " + str(second_position_last_traded_price) + ", " )
    outputFile.write( str(ce_offer_price) + ", " + str(ce_bid_price) + ", " + str(ce_volume) + ", " + str(ce_last_traded_price) + ", " )
    outputFile.write( str(pe_offer_price) + ", " + str(pe_bid_price) + ", " + str(pe_volume) + ", " + str(pe_last_traded_price) + ", " )
       
    outputFile.close()
#End of Function

################################################################ MAIN ################################################################

input_template()
switch_streams()
