class ValueModel:
    def __init__(self, data):
        self.raw = data

        self.code = data["code"]
        self.msg = data["msg"]
        try: self.value = data["json"]["value"]
        except: self.value = None
        try: self.data = data["json"]["value"]
        except: self.data = None
    