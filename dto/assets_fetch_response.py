from dto.base_response import BaseResponse

class AssetsFetchResponse(BaseResponse):
    def __init__(self):
        super().__init__()

        self.assets = []

    def add_asset(self, asset_name: str, asset_balance: float, symbol: str):
        self.assets.append({
            "name": asset_name,
            "balance": f"{asset_balance} {symbol}"
        })

    def serialize(self):
        return {
            "assets": self.assets,
            "infos": self.infos.serialize(),
            "response_code": self.response_code
        }
