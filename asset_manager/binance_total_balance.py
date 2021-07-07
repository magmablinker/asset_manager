import os
import json
from datetime import datetime

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
