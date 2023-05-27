import conf      
import time
import json 
import requests
from boltiot import Bolt,Sms

bolt=Bolt(conf.BOLT_API,conf.DEVICE_ID)
sms=Sms(conf.SSID,conf.AUTH_TOKEN,conf.TO_NUMBER,conf.FROM_NUMBER)

print("Select any one of the following currency input\nINR\nUSD\nJPY\nEUR")
currency=input("Enter the above Currency from which you have to invest in:")
sell_price=float(input("Enter Your Selling Price:"))

def price_check():
    url=("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms={}".format(currency.upper()))
    response=requests.request("GET",url)
    response=json.loads(response.text)
    current_price=response[currency.upper()]
    return current_price

while True:
    market_price=price_check()
    print("Market price of Bitcoin is:",market_price)
    print("Selling Price is:",sell_price)
    try:
         if market_price < sell_price:      
             bolt.digitalWrite("1","HIGH")
             response1=sms.send_sms("The Bitcoins are at price ={} You can Invest now if you want".format(current_bitcoin_value))
             print("Status of Sms at Twilo:"+str(response1.status))
             
            
          elif market_price > sell_price:
              bolt.digitalWrite("0","HIGH")#BUZZER gets "ON
             response1=sms.send_sms("The Bitcoins are at price ={} You need to be cautious".format(current_bitcoin_value))
             print("Status of Sms at Twilo:"+str(response1.status))
             
    except Exception as e:
        print("An error occured\n")
        print(e)
    time.sleep(5).
    bolt.digitalWrite("0","LOW")#led gets off
    bolt.digitalWrite("1","LOW")#buzzer gets off
    time.sleep(30)