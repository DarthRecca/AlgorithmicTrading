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
first_position_type = ""                                            #Initialise the type of position (for first stream) eg.FUT,CE,PE,EQ
second_position_type = ""                                           #Initialise the type of position (for second stream) eg.FUT,CE,PE,EQ
first_instrument_code = 0                                           #Initialise the instrument code for first stream subscription 
second_instrument_code = 0                                          #Initialise the instrument code for second stream subscription 
order_type = ""                                                     #Initialise the type of order eg. MARKET,LIMIT
upper_difference_limit = 0.0                                        #Initialise the upper difference limit
lower_difference_limit = 0.0                                        #Initialise the lower difference limit
square_off_difference_limit = 0.0                                   #Initialise the difference limit during square off
max_loss_limit = 0.0                                                #Initialise the max loss allowed limit
moving_average_short_array_size = 0                                 #Initialise the size of array used for moving_average->short calculation and analysis
moving_average_long_array_size = 0                                  #Initialise the size of array used for moving_average->long calculation and analysis
volume_difference_array_size = 0                                    #Initialise the size of array used for volume difference calculation and analysis
price_difference_array_size = 0                                     #Initialise the size of array used for price difference calculation and analysis
online_offline_switch = ""                                          #Initialise the flag representing offline and online mode switch

################################################################ INPUT TEMPLATE FUNCTION ################################################################

def input_template():                                                      #Function to take i/p file and set the necessry variables
    #Set up the global variable names used in this function
    global stock_name, exchange_code, expiry_year, expiry_month, product_type, lot_size, spike_threshold, order_type, online_offline_switch #General global variables
    global first_instrument_code, first_position_type                                                                                       #First position variables
    global second_instrument_code, second_position_type                                                                                     #Second position variables
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
    first_instrument_code = int(inputFile.ix[8,1])                      #Store the instrument code for first stream subscription 
    second_instrument_code = int(inputFile.ix[9,1])                     #Store the instrument code for second stream subscription 
    order_type = str(inputFile.ix[10,1])                                #Store the type of order eg. MARKET,LIMIT
    upper_difference_limit = float(inputFile.ix[11,1])                  #Store the upper difference limit
    lower_difference_limit = float(inputFile.ix[12,1])                  #Store the lower difference limit
    square_off_difference_limit = float(inputFile.ix[13,1])             #Store the difference limit during square off
    max_loss_limit = float(inputFile.ix[14,1])                          #Store the max loss allowed limit
    moving_average_short_array_size = int(inputFile.ix[15,1])           #Store the size of array used for moving_average->short calculation and analysis
    moving_average_long_array_size = int(inputFile.ix[16,1])            #Store the size of array used for moving_average->long calculation and analysis
    volume_difference_array_size = int(inputFile.ix[17,1])              #Store the size of array used for volume difference calculation and analysis
    price_difference_array_size = int(inputFile.ix[17,1])               #Store the size of array used for price difference calculation and analysis
    online_offline_switch = str(inputFile.ix[18,1])                     #Store the flag representing offline and online mode switch

    print("Inputted template file: ")                                   #Print the pandas->dataframe storing the input template file
    print(inputFile)
    #End of Function

################################################################ ONLINE/OFFLINE SWITCH HANDLING ################################################################

def switch_streams():                                                                       #Function to decide whether to run in online/offline mode
    #Set up the global variable names used in this function
    global online_offline_switch
    
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
            off_ticks()                                                                     #Call the Offline test data gathering function
        else :
            break                                                                           #If not intention for offline stream, break and exit program
    else :
        print("Invalid input. Please change switch parameter in the input template file.")  #If invalid input print error message and exit program
        break
    #End of Function
    
################################################################ ONLINE DATA GATHERING FUNCTION ################################################################    
    
def on_ticks(ws, ticks):                                                                    #Function to gather online stream data
    #Placeholder
 
################################################################ ONLINE OPEN CONNECTION FUNCTION ################################################################
    
def on_connect(ws, response):                                                               #Function to subscribe to instruments and set mode of incoming stream data
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens.
    ws.subscribe([])

    # Set instrument to tick in `full` mode.
    ws.set_mode(ws.MODE_FULL, [])

################################################################ ONLINE CLOSE CONNECTION FUNCTION ################################################################

def on_close(ws, code, reason):                                                             #Function to handle closing of the stream connection
    # On connection close stop the main loop
    # Reconnection will not happen after executing `ws.stop()`
    ws.stop()

################################################################ OFFLINE DATA GATHERING FUNCTION ################################################################    
    
def off_ticks():                                                                            #Function to gather offline test data
    #Placeholder    
    
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
    
