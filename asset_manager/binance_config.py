import os
import json

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