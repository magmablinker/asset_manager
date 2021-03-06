import os
import json
from datetime import datetime
from asset_manager.util.util import Util
from dto.binance_asset_profits import BinanceAssetProfits

'''
Represents the total balance of all binance crypto assets
'''
class BinanceTotalBalance(object):
    def __init__(self):
        self.total_balance = 0
        self.total_output_file = f"data/total_balance.json"

    def add_symbol_balance(self, symbol_balance: float):
        self.total_balance += symbol_balance

    def write(self):
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        total_output = self._get_total_output()

        total_output["balances"].append({
            "timestamp": timestamp,
            "balance": self.total_balance
        })

        self._write_total_output(total_output)

    def get_total_balance(self):
        total_balances = self._get_total_output()

        if len(total_balances["balances"]) < 1:
            raise ValueError("No total balances found")
        
        return total_balances["balances"][-1]

    def _get_total_output(self):
        if not os.path.exists(self.total_output_file) or not os.path.isfile(self.total_output_file):
            return {
                "balances": []
            }
        else:
            with open(self.total_output_file) as f:
                return json.load(f)

    def _write_total_output(self, total_output):
        with open(self.total_output_file, "w+") as f:
            json.dump(total_output, f, indent=4)

    def to_graph(self):
        x_axis = []
        y_axis = []

        balances = self._get_total_output()["balances"]

        for entry in balances:
            y_axis.append(float(entry["balance"]))
            x_axis.append(datetime.strptime(entry["timestamp"], "%Y-%m-%dT%H:%M:%S").strftime("%d.%m.%Y"))

        Util.plot(x_axis, y_axis, "Total Balance Over Time", "Timestamp", "Balance", "img/total_balance")

    
    def get_all_entries(self):
        return self._get_total_output()["balances"]
    
    def get_profits(self) -> BinanceAssetProfits:
        profits = BinanceAssetProfits()
        asset_data = self._get_total_output()["balances"]
        
        if len(asset_data) < 1:
            return profits

        profits.initial_asset_data = asset_data[0]["balance"]
        profits.latest_asset_data = asset_data[len(asset_data) - 1]["balance"]

        return profits
