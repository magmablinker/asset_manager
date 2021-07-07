import os
import json
from binance import Client
from datetime import datetime

'''
Represents a Binance crypto asset
'''
class BinanceAsset():
    def __init__(self, asset: str, amount: float, client: Client, debug_mode=False):
        self.asset = asset
        self.amount = amount
        self.client = client
        self.symbol_balance = 0
        self.debug_mode = debug_mode

    def write(self):
        symbol = f"{self.asset}USDT"
        symbol_ticker = self.client.get_symbol_ticker(symbol=symbol)
        self.symbol_balance = self.amount * float(symbol_ticker['price'])

        balance_rounded = "{:.2f}".format(self.symbol_balance)
        
        self.print(f"[{self.asset}] {balance_rounded} USDT")

        output_file = f"data/assets/{self.asset}.json"

        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        output_data = {
            "timestamp": timestamp,
            "balance": self.symbol_balance
        }

        if not os.path.exists(output_file) or not os.path.isfile(output_file):
            output = {
                "data": [],
                "initial_value": ""
            }
        else:
            with open(output_file) as f:
                output = json.load(f)
            
        output["data"].append(output_data)

        with open(output_file, "w+") as f:
            json.dump(output, f, indent=4)

    def print(self, text: str):
        if self.debug_mode:
            print(text)
