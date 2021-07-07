import os
import json
from binance import Client
from pprint import pprint
from datetime import datetime

'''
Class to load the required variables to access the Binance API
'''
class BinanceConfig():
    def __init__(self, file_path):
        if not os.path.exists(file_path):
            raise ValueError(f"Binance config file {file_path} not found")

        with open(file_path, "r") as f:
            config = json.load(f)

            self.api_key = config["binance_api_key"]
            self.api_secret = config["binance_api_secret"]


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
        
        self.print(f"{self.asset} => {self.symbol_balance} USDT")

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


'''
Represents the total balance of all binance crypto assets
'''
class BinanceTotalBalance():
    def __init__(self):
        self.total_balance = 0

    def add_symbol_balance(self, symbol_balance: float):
        self.total_balance += symbol_balance

    def write(self):
        total_output_file = f"data/total_balance.json"

        if not os.path.exists(total_output_file) or not os.path.isfile(total_output_file):
            total_output = {
                "balances": []
            }
        else:
            with open(total_output_file) as f:
                total_output = json.load(f)

        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        total_output["balances"].append({
            "timestamp": timestamp,
            "balance": self.total_balance
        })

        with open(total_output_file, "w+") as f:
            json.dump(total_output, f, indent=4)


'''
Helper class to run through the process of fetching necessary data
'''
class AssetManager():
    def __init__(self, binance_config_path: str, debug_mode=False):
        self.binance_config = BinanceConfig(binance_config_path)
        self.binance_total_balance = BinanceTotalBalance()
        self.debug_mode = debug_mode

    def run(self):
        client = Client(self.binance_config.api_key, self.binance_config.api_secret)
        account = client.get_account()

        for balance in account["balances"]:
            free = float(balance["free"])

            if free > 0 and balance['asset'] != "USDT":
                binance_asset = BinanceAsset(balance["asset"], free, client, self.debug_mode)

                binance_asset.write()

                self.binance_total_balance.add_symbol_balance(binance_asset.symbol_balance)

        self.binance_total_balance.write()
                
        self.print(f"Total Balance: ~{self.binance_total_balance.total_balance} USDT")

    def print(self, text: str):
        if self.debug_mode:
            print(text)
            

def main():
    asset_manager = AssetManager("config/config.json", True)
    asset_manager.run()

if __name__ == '__main__':
    main()
