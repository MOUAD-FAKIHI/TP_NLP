from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from dotenv import load_dotenv
import os
import requests

# Load the .env file
load_dotenv('api.env')

class ActionFetchStockPrice(Action):
    def name(self) -> str:
        return "action_fetch_stock_price"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> list:
        stock = tracker.get_slot("stock")
        api_key = os.getenv('API_KEY')
        response = requests.get(f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}')
        data = response.json()
        price = data['Global Quote']['05. price']
	dispatcher.utter_message(template="utter_stock_price", stock=stock, price=price)
        return [SlotSet("price", price)]

class ActionFetchCryptoPrice(Action):
    def name(self) -> str:
        return "action_fetch_crypto_price"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> list:
        crypto = tracker.get_slot("crypto")
        api_key = os.getenv('API_KEY')
        response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd')
        data = response.json()
        price = data[crypto]['usd']
	dispatcher.utter_message(template="utter_crypto_price", crypto=crypto, price=price)
        return [SlotSet("price", price)]
