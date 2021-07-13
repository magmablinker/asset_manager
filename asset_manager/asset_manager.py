from asset_manager.binance_config import BinanceConfig
from asset_manager.binance_asset import BinanceAsset
from asset_manager.binance_total_balance import BinanceTotalBalance
from binance import Client
from colorama import init, Fore
from asset_manager.util.util import Util

'''
Helper class to run through the process of fetching necessary data
'''
class AssetManager(object):
    def __init__(self, binance_config_path: str, pair_asset: str):
        init()

        self.binance_config = BinanceConfig(binance_config_path)
        self.binance_total_balance = BinanceTotalBalance()
        self.debug = self.binance_config.debug
        self.pair_asset = pair_asset
        self.ignore_assets = [ self.pair_asset ] + self.binance_config.asset_blacklist # Add assets here to ignore them => we always have to ignore the pair_asset
        self.client = Client(self.binance_config.api_key, self.binance_config.api_secret)
        assets = self.client.get_account()

        # Load all assets that have a non zero balance and are
        # not in the "asset blacklist"
        self.assets = []
        self.binance_assets = []

        for asset in assets["balances"]:
            free = float(asset["free"])

            if free > 0 and not asset["asset"] in self.ignore_assets:
                self.binance_assets.append(BinanceAsset(asset["asset"], free, self.pair_asset, self.debug))
            
    def run(self):
        for binance_asset in self.binance_assets:
            binance_asset.write(self.client)

            self.binance_total_balance.add_symbol_balance(binance_asset.symbol_balance)
            
        self.binance_total_balance.write()

        self.print(f"Total Balance: {Util.round(self.binance_total_balance.total_balance)} USDT")
        self.print("")

    def calculate_profits_from_inital_per_asset(self):
        for binance_asset in self.binance_assets:
            profits = binance_asset.get_profits()
            
            color = Fore.RED if profits.is_at_loss else Fore.GREEN

            self.print("+=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=+")
            self.print(f"[{binance_asset.asset}]")
            self.print(f"Inital Captured Value: {Util.round(profits.initial_asset_data)} USDT") 
            self.print(f"Last Captured Value: {Util.round(profits.latest_asset_data)} USDT")         
            self.print(f"{color}{profits.amount}{Fore.RESET} USDT | {color}{profits.percent}{Fore.RESET}%")
            self.print(f"Currently at {color}{profits.text}{Fore.RESET}")
            self.print("+=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=+")  
            self.print("")

    def print(self, text: str):
        if self.debug:
            print(text)