from asset_manager.binance_config import BinanceConfig
from asset_manager.binance_asset import BinanceAsset
from asset_manager.binance_total_balance import BinanceTotalBalance
from binance import Client

'''
Helper class to run through the process of fetching necessary data
'''
class AssetManager():
    def __init__(self, binance_config_path: str, debug_mode=False):
        self.binance_config = BinanceConfig(binance_config_path)
        self.binance_total_balance = BinanceTotalBalance()
        self.debug_mode = debug_mode
        self.ignore_assets = [ "USDT" ] # Add assets here to ignore them

    def run(self):
        client = Client(self.binance_config.api_key, self.binance_config.api_secret)
        account = client.get_account()

        for balance in account["balances"]:
            free = float(balance["free"])

            if free > 0 and not balance['asset'] in self.ignore_assets:
                binance_asset = BinanceAsset(balance["asset"], free, client, self.debug_mode)

                binance_asset.write()

                self.binance_total_balance.add_symbol_balance(binance_asset.symbol_balance)

        self.binance_total_balance.write()

        total_balance_rounded = "{:.2f}".format(self.binance_total_balance.total_balance)
        self.print(f"Total Balance: {total_balance_rounded} USDT")

    def print(self, text: str):
        if self.debug_mode:
            print(text)