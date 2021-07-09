import os
import json

'''
Class to load the required variables to access the Binance API
'''
class BinanceConfig(object):
    def __init__(self, file_path):
        if not os.path.exists(file_path):
            raise ValueError(f"Binance config file {file_path} not found")

        self.file_path = file_path

        self._load_config()

    def _load_config(self):
        with open(self.file_path, "r") as f:
            config = json.load(f)

            if "api_key" not in config:
                raise ValueError(f"Config file {self.file_path} doesn't contain the required object key 'api_key'")

            if "api_secret" not in config:
                raise ValueError(f"Config file {self.file_path} doesn't contain the required object key 'api_key'")

            self.api_key = config["api_key"]
            self.api_secret = config["api_secret"]