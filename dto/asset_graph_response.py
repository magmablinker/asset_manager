from dto.base_response import BaseResponse

class AssetGraphResponse(BaseResponse):
    def __init__(self):
        super().__init__()
        self.base64_img = ""
        self.asset = ""

    def serialize(self):
        return {
            "base64_img": self.base64_img.decode("utf-8"),
            "asset": self.asset,
            "infos": self.infos.serialize(),
            "response_code": self.response_code
        }
