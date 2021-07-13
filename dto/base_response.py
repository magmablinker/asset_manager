class BaseResponse():
    def __init__(self):
        self.infos = ResponseInfos()
        self.response_code = 200

    def serialize(self):
        return {
            "infos": self.infos,
            "response_code": self.response_code
        }


class ResponseInfos():
    def __init__(self):
        self.errors = []
        self.infos = []
    
    def add_error(self, error: str):
        self.errors.append(error)

    def add_info(self, info: str):
        self.infos.append(info)

    def has_error(self):
        return len(self.errors) > 0

    def serialize(self):
        return {
            "errors": self.errors,
            "infos": self.infos,
            "has_error": self.has_error()
        }

