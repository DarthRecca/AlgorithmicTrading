import logging
from kiteconnect import KiteConnect

logging.basicConfig(level=logging.DEBUG)

#Getting key and secret
keyFileName = input("Enter name of key file: ")         #Input key file name/path(Keep key file in folder for no path)
keyFile = open(keyFileName,'r')                         #Open the key file
api_key = keyFile.readline().replace("\n","")           #Get first line and remove newline characters
api_secret = keyFile.readline().replace("\n","")        #Get second line and remove newline characters
keyFile.close()                                         #Close the open key file

request_token  = input("Paste Request token: ")

#instantiating KiteAPI
kite = KiteConnect(api_key= api_key)

session_data = kite.generate_session( request_token , api_secret = api_secret )       #Generate a session and get session data with request token and api_secret

kite.set_access_token(session_data["access_token"])                                                     #Use session data to set access_token
print(session_data["access_token"])                                                                     #Print access_token to copy paste to kiteAPI program
accessTokenFile = open("access_token.txt", 'w')                                                         #Create accessTokenFile irrespective of printing to console
accessTokenFile.write(session_data["access_token"])                                                     #Write access_token
accessTokenFile.close()                                                                                 #Close accessTokenFile