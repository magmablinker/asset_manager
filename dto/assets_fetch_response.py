from dto.base_response import BaseResponse
from asset_manager.binance_asset import BinanceAsset
from asset_manager.util.util import Util

class AssetsFetchResponse(BaseResponse):
    def __init__(self):
        super().__init__()

        self.assets = []

    def add_asset(self, asset: BinanceAsset):
        self.assets.append({
            "name": asset.asset,
            "balance": f"{Util.round(asset.symbol_balance)} {asset.pair_asset}"
        })

    def serialize(self):
        return {
            "assets": self.assets,
            "infos": self.infos.serialize(),
            "response_code": self.response_code
        }
