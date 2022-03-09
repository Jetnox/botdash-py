from itsdangerous import json
import requests
import ujson as json

class Client:
    def __init__(self, token: str):
        self.token = token
        self.uri = "https://botdash.pro/api/v2"

    def get(self, guild_id: str, key: str):
        res = requests.get(
            f"{self.uri}/value/{key}/{guild_id}", 
            headers={
                "Authorization": self.token
            }     
        )

        return json.loads(res.text)