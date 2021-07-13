from dto.binance_asset_profits import BinanceAssetProfits
from dto.base_response import BaseResponse

class AssetProfitsResponse(BaseResponse):
    def __init__(self):
        super().__init__()
        self.asset_profits = BinanceAssetProfits()

    def serialize(self):
        return {
            "asset_profits": self.asset_profits.serialize(),
            "infos": self.infos.serialize(),
            "response_code": self.response_code
        }