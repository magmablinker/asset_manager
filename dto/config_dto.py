from dto.base_response import BaseResponse

'''
Never do this but idc :D
'''
class ConfigDto(BaseResponse):
    def __init__(self):
        super().__init__()
        
        self.config = {
            "api_key": "",
            "api_secret": "",
            "debug": False,
            "asset_blacklist": []
        }

    def serialize(self):
        return {
            "config": self.config,
            "infos": self.infos.serialize(),
            "response_code": self.response_code
        }
