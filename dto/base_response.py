class BaseResponse():
    def __init__(self):
        self.infos = ResponseInfos()
        self.response_code = 200

    def serialize(self):
        return {
            "infos": self.infos.serialize(),
            "response_code": self.response_code
        }


class ResponseInfos():
    def __init__(self):
        self.errors = []
        self.infos = []
        self.messages = []
    
    def add_error(self, error: str):
        self.errors.append(error)

    def add_info(self, info: str):
        self.infos.append(info)

    def add_message(self, message: str):
        self.messages.append(message)

    @property
    def has_error(self):
        return len(self.errors) > 0

    @property
    def has_info(self):
        return len(self.infos) > 0

    @property
    def has_message(self):
        return len(self.messages) > 0

    def serialize(self):
        return {
            "errors": self.errors,
            "infos": self.infos,
            "messages": self.messages,
            "has_error": self.has_error,
            "has_info": self.has_info,
            "has_message": self.has_message,
        }

