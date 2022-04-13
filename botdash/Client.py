import requests
import ujson as json
from .lib import ValueModel

class Client:
    def __init__(self, token: str, return_value: bool = False, debug: bool = False):
        self.token = token
        self.debug = debug
        self.uri = "https://botdash.pro/api/v2"
        self.return_value = return_value # set to true if default NEEDS to be <RESPONSE_JSON?>.json.value

    def __log(self, message: str):
        print(f"[Botdash.py Client] {message}")

    def get(self, guild_id: str, key: str):
        res = requests.get(
            f"{self.uri}/value/{key}/{guild_id}", 
            headers={
                "Authorization": self.token
            }     
        )

        if self.debug:
            self.__log(res.text)

        bd = json.loads(res.text)

        if bd["code"] != 200:
            raise Exception(f"BotDash Error: [{bd['code']}] {bd['msg']}")
        else: 
            if self.return_value: return bd["json"]["value"]
            else: return ValueModel(bd)
        

        
