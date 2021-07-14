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

            if "debug" not in config:
                config["debug"] = False

            if "asset_blacklist" not in config:
                raise ValueError(f"Config file {self.file_path} doesn't contain the required object key 'asset_blacklist'")

            self.api_key = config["api_key"]
            self.api_secret = config["api_secret"]
            self.debug = config["debug"]
            self.asset_blacklist = config["asset_blacklist"]

    def save_config(self):
        with open(self.file_path, "r+") as f:
            config = json.load(f)

            config["api_key"] = self.api_key
            config["api_secret"] = self.api_secret
            config["debug"] = self.debug
            config["asset_blacklist"] = self.asset_blacklist

            f.seek(0)
            
            json.dump(config, f, indent=4)

            f.truncate()
