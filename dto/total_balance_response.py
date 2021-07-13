from dto.base_response import BaseResponse
from datetime import datetime

class TotalBalanceResponse(BaseResponse):
    def __init__(self):
        super().__init__()
        self.total_balance = 0
        self.timestamp = datetime.now()

    def serialize(self):
        return {
            "total_balance": self.total_balance,
            "timestamp": self.timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
            "infos": self.infos.serialize(),
            "response_code": self.response_code
        }
