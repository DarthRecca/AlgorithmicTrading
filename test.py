"""
import numpy as np

#################### POP AND PUSH EMULATE AS QUEUE ######################################

a = np.array([0,1,2,3,4,5,6,7,8,9])
a = np.roll(a,-1)
a[9] = 25
print (a)
"""
"""
import pandas as pd

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
"""