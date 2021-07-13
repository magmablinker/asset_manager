from dto.base_response import BaseResponse

class AssetResponse(BaseResponse):
    def __init__(self):
        super().__init__()
        self.asset_data = []
        self.assets = []

    def serialize(self):
        return {
            "asset_data": self.asset_data,
            "assets": self.assets,
            "infos": self.infos.serialize(),
            "response_code": self.response_code
        }
