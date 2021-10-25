import hashlib
import hmac
import json
import time

from http import client
from urllib.parse import urlencode

# Mercado Bitcoin Trade API v3 Python Wrapper
# Author: Luciano Ayres (lucianofarias@gmail.com)
# March 20, 2021
# API Doc: https://www.mercadobitcoin.com.br/trade-api

class mbpy:
    def __init__(self, user_tapi_id, user_tapi_secret):
        # Constants
        self.MB_TAPI_ID = user_tapi_id
        self.MB_TAPI_SECRET = user_tapi_secret
        self.REQUEST_HOST = 'www.mercadobitcoin.net'
        self.REQUEST_PATH = '/tapi/v3/'

    # Refresh value for tapi_nonce parameteter
    def __private_gettapinonce(self):
        return str(int(time.time()))

    def listsystemmessages(self, level=''):
        self.params = {
                'tapi_method': 'list_system_messages',
                'tapi_nonce': self.__private_gettapinonce(),
                'level': level # INFO=system informations WARNING=system warnings ERROR=system errors
                }
        #Make API call
        self.__private_apirequest()

    # Get user exchange account info
    def getaccountinfo(self):
        # Parameters
        self.params = {
                'tapi_method': 'get_account_info',
                'tapi_nonce': self.__private_gettapinonce()
                }
        # Make API call
        self.__private_apirequest()

    # Market buy order
    def placemarketbuyorder(self, coin_pair, cost):
        self.params = {
                'tapi_method': 'place_market_buy_order',
                'tapi_nonce': self.__private_gettapinonce(),
                'coin_pair': coin_pair,
                'cost': cost
                }
        # Make API call
        return self.__private_apirequest()

    # Market sell order
    def placemarketsellorder(self, coin_pair, quantity):
        self.params = {
                'tapi_method': 'place_market_sell_order',
                'tapi_nonce': self.__private_gettapinonce(),
                'coin_pair': coin_pair,
                'quantity': quantity
                }
        # Make API call
        self.__private_apirequest()

    # Buy order (coin quantity with limit price)
    def placebuyorder(self, coin_pair, quantity, limit_price):
        self.params = {
                'tapi_method': 'place_buy_order',
                'tapi_nonce': self.__private_gettapinonce(),
                'coin_pair': coin_pair, # Example: BRLBTC (use brazilian reais to buy Bitcoin)
                'quantity': quantity,
                'limit_price': limit_price
                }
        # Make API call
        self.__private_apirequest()

    # Sell order (coin quantity with limit price)
    def placesellorder(self, coin_pair, quantity, limit_price):
        self.params = {
                'tapi_method': 'place_sell_order',
                'tapi_nonce': self.__private_gettapinonce(),
                'coin_pair': coin_pair,
                'quantity': quantity,
                'limit_price': limit_price
                }
        # Make API call
        self.__private_apirequest()

    # Get order info
    def getorder(self, coin_pair, order_id):
        self.params = {
                'tapi_method': 'get_order',
                'tapi_nonce': self.__private_gettapinonce(),
                'coin_pair': coin_pair,
                'order_id': order_id
                }
        # Make API call
        self.__private_apirequest()

    # Cancel order
    def cancelorder(self, coin_pair, order_id):
        self.params = {
                'tapi_method': 'cancel_order',
                'tapi_nonce': self.__private_gettapinonce(),
                'coin_pair': coin_pair,
                'order_id': order_id
                }
        # Make API call
        self.__private_apirequest()

    # List user orders
    def listorders(
            self, 
            coin_pair,
            order_type = '', # 1=Buy order 2=sell order 
            status_list = [''], # 2=open 3=cancelled 4=filled
            has_fills = '', # false=not executed true=executed once or more
            from_id = '', # orders from the specified ID
            to_id = '', # orders to specified ID
            from_timestamp = '', # unix time
            to_timestamp = '' # unix time
            ):
        self.params = {
                'tapi_method': 'list_orders',
                'tapi_nonce': self.__private_gettapinonce(),
                'coin_pair': coin_pair,
                'order_type': order_type,
                'status_list': status_list,
                'has_fills': has_fills,
                'from_id': from_id,
                'to_id': to_id,
                'from_timestamp': from_timestamp,
                'to_timestamp': to_timestamp
                }
        # Make API call
        self.__private_apirequest()

    # List Mercado Bitcoin public orderbook
    def listorderbook(self, coin_pair, full = False):
        self.params = {
                'tapi_method': 'list_orderbook',
                'tapi_nonce': self.__private_gettapinonce(),
                'coin_pair': coin_pair,
                'full': full # false=list 20 buy & 20 sell orders max. true=list 500 buy & 500 sell orders max.
                }
        # Make API call
        self.__private_apirequest()

    # Withdraw (transfer) coin (crypto or brazilian reais (BRL))
    # Crypto or Brazilian Reais can only be transfered to a trusted (wallet) address or bank account
    # A trusted address or bank account must be added by the user on Mercado Bitcoin account setting
    # Crypto withdraw require e-mail confirmation by the user to be completed
    def withdraw_coin(
            self, 
            coin, 
            quantity,
            account_ref = '', # trusted bank account ID (required if coin is BRL)
            address = '', # trusted wallet address (required if cryptocoin)
            tx_fee = '', # mining fee for the transfer (required if cryptocoin),
            destination_tag = '', # required if coin is XRP
            description = '' # Optional description/comment for the withdraw/transfer (30 chars max)
            ):
        self.params = {
                'tapi_method': 'withdraw_coin',
                'tapi_nonce': self.__private_gettapinonce(),
                'coin': coin, # BRL BCH BTC LTC ETH XRP
                'quantity': quantity,
                'account_ref': account_ref,
                'address': address,
                'tx_fee': tx_fee,
                'destination_tag': destination_tag,
                'description': description
                }
        # Make API call
        self.__private_apirequest()

    # Get withdrawal info
    def getwithdrawal(self, coin, withdrawal_id):
        self.params = {
                'tapi_method': 'get_withdrawal',
                'tapi_nonce': self.__private_gettapinonce(),
                'coin': coin,
                'withdrawal_id': withdrawal_id
                }
        # Make API call
        self.__private_apirequest()

    # Setup API request with auth parameters
    def __private_setuprequest(self):
        # encode request parameters
        self.params = urlencode(self.params)
        # Generate MAC
        params_string = self.REQUEST_PATH + '?' + self.params
        H = hmac.new(bytes(self.MB_TAPI_SECRET, encoding='utf8'), digestmod=hashlib.sha512)
        H.update(params_string.encode('utf-8'))
        self.tapi_mac = H.hexdigest()
        # Define http headers
        self.headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'TAPI-ID': self.MB_TAPI_ID,
                'TAPI-MAC': self.tapi_mac
                }

        # Send API request
    def __private_apirequest(self):
        # setup request
        self.__private_setuprequest()
        # Make POST request
        try:
            conn = client.HTTPSConnection(self.REQUEST_HOST)
            conn.request("POST", self.REQUEST_PATH, self.params, self.headers)
            # Print response data to console
            response = conn.getresponse()
            response = response.read()
            response_json = json.loads(response)
            #print(json.dumps(response_json, indent=4))
            return response_json
        finally:
            if conn:
                conn.close()
