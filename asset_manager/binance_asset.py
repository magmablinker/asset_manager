import os
import json
from binance import Client
from datetime import datetime
from asset_manager.util.util import Util

'''
Represents a Binance crypto asset
'''
class BinanceAsset(object):
    def __init__(self, asset: str, amount: float, debug_mode=False):
        self.asset = asset
        self.amount = amount
        self.symbol_balance = 0
        self.debug_mode = debug_mode

    def write(self, client: Client):
        symbol = f"{self.asset}USDT"
        symbol_ticker = client.get_symbol_ticker(symbol=symbol)
        self.symbol_balance = self.amount * float(symbol_ticker['price'])
        
        self.print(f"[{self.asset}] {Util.round(self.symbol_balance)} USDT")

        output_file = f"data/assets/{self.asset}.json"

        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        output_data = {
            "timestamp": timestamp,
            "balance": self.symbol_balance
        }

        if not os.path.exists(output_file) or not os.path.isfile(output_file):
            output = {
                "data": [],
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


    def load_asset_data(self):
        output_file = f"data/assets/{self.asset}.json"

        with open(output_file, "r") as f:
            return json.load(f)["data"]
