import os
import json
from binance import Client
from datetime import datetime
from asset_manager.util.util import Util
from dto.binance_asset_profits import BinanceAssetProfits

'''
Represents a Binance crypto asset
'''
class BinanceAsset(object):
    def __init__(self, asset: str, amount: float, pair_asset: str, debug=False):
        self.asset = asset
        self.amount = amount
        self.symbol_balance = 0
        self.debug = debug
        self.output_file = f"data/assets/{self.asset}.json"
        self.pair_asset = pair_asset

    def write(self, client: Client):
        self._get_symbol_balance(client)

        output = self._get_output()
            
        output["data"].append(self._get_output_data())

        self._write_output(output)

    def load_asset_data(self):
        output_file = f"data/assets/{self.asset}.json"

        if not os.path.exists(output_file) or not os.path.isfile(output_file):
            raise ValueError(f"No asset data for asset {self.asset} found")

        with open(output_file, "r") as f:
            return json.load(f)["data"]

    def to_graph(self):
        x_axis = []
        y_axis = []

        balances = self._get_output()["data"]

        for entry in balances:
            y_axis.append(float(entry["balance"]))
            x_axis.append(datetime.strptime(entry["timestamp"], "%Y-%m-%dT%H:%M:%S").strftime("%d.%m.%Y"))
        
        self.print(f"Creating diagram for {self.asset}")
        Util.plot(x_axis, y_axis, f"{self.asset} Worth Over Time", "Timestamp", "Balance", f"img/{self.asset}")

    def get_profits(self) -> BinanceAssetProfits:
        profits = BinanceAssetProfits()
        asset_data = self.load_asset_data()
        
        if len(asset_data) < 1:
            self.print(f"[?] Skipping asset {self.asset}, no data available")
            return profits

        profits.initial_asset_data = asset_data[0]["balance"]
        profits.latest_asset_data = asset_data[len(asset_data) - 1]["balance"]

        return profits

    def _get_symbol_balance(self, client: Client):
        symbol = f"{self.asset}{self.pair_asset}"
        symbol_ticker = client.get_symbol_ticker(symbol=symbol)
        self.symbol_balance = self.amount * float(symbol_ticker['price'])
        
        self.print(f"[{self.asset}] {Util.round(self.symbol_balance)} USDT")

    def _get_output(self):
        if not os.path.exists(self.output_file) or not os.path.isfile(self.output_file):
            return {
                "data": [],
            }
        else:
            with open(self.output_file) as f:
                return json.load(f)

    def _get_output_data(self):
        return  {
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "balance": self.symbol_balance
        }

    def _write_output(self, output):
        with open(self.output_file, "w+") as f:
            json.dump(output, f, indent=4)

    def print(self, text: str):
        if self.debug:
            print(text)
