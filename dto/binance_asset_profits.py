from asset_manager.util.util import Util

class BinanceAssetProfits():
    def __init__(self):
        self.initial_asset_data = 0
        self.latest_asset_data = 0

    @property
    def is_at_loss(self):
        return self.latest_asset_data < self.initial_asset_data

    @property
    def amount(self):
        return Util.round(self.latest_asset_data - self.initial_asset_data) if self.initial_asset_data != 0 and self.latest_asset_data != 0 else 0

    @property
    def percent(self):
        return Util.round(((self.latest_asset_data - self.initial_asset_data) / self.initial_asset_data) * 100)  if self.initial_asset_data != 0 and self.latest_asset_data != 0 else 0
    
    @property
    def text(self):
        return "Loss" if self.is_at_loss else "Profits"

    def serialize(self):
        return {
            "is_at_loss": self.is_at_loss,
            "initial_asset_data": self.initial_asset_data,
            "latest_asset_data": self.latest_asset_data,
            "amount": self.amount,
            "percent": self.percent,
            "text": self.text
        }