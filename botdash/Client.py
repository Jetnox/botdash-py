import discord
import requests
import time
import threading
import asyncio
import ujson as json
import socketio as io
from .lib import ValueModel

class Client:
    def __init__(self, token: str, return_value: bool = False, debug: bool = False, client: discord.Client = None):
        self.token = token
        self.debug = debug
        self.uri = "https://botdash.pro/api/v2"
        self.socketUri = "http://mars.skyswift.eu:7562/"
        self.return_value = return_value # set to true if default NEEDS to be <RESPONSE_JSON?>.json.value
        self.socket = io.Client()
        self.discord = client
        self.cache = {}
        self.modelCache = {}
        self.threads = []
        self.events = []
    
        self.util_setInterval(self.syncToSocket, 60) # every minute sync servers and cool stuff
        self.util_setInterval(self.updateCache, 60 * 50) # every 50 min update cache (in case of a desync during interruptions etc)

        @self.socket.on("trigger")
        def trigger(data):
            self.emit("trigger", data)

        @self.socket.on("change")
        def change(data):
            if self.debug:
                self.__log(f"Change: {data}")
            guild_id = data["guild"]
            key = data["key"]
            value = data["value"]

            if guild_id in self.cache:
                self.cache[guild_id][key] = value

            self.emit("change", data)

        @self.socket.on("error")
        def error(data):
            if self.debug:
                self.__log("BotDash Error (SIO): " +  data)
            
        @self.socket.on("connect")
        def connect():
            self.syncToSocket()
            self.updateCache()

        @self.socket.on("cache")
        def cache(data):
            self.cache = {}
            self.modelCache = {}
            
            for setting in data["settings"]:
                self.modelCache[setting["database"]] = setting["default"]

            for meta in data["meta"]:
                guild_id = meta["guild"]
                if guild_id not in self.cache:
                    self.cache[guild_id] = {}
                self.cache[guild_id][meta["key"]] = meta["value"]
            
        self.socket.connect(self.socketUri + "?authToken=" + self.token)
    
    def __log(self, message: str):
        print(f"[Botdash.py Client] {message}")
    
    def syncToSocket(self):
        if self.discord is None:
            return
        
        while not self.discord.is_ready():
            time.sleep(1)
        
        guilds = []
        for guild in self.discord.guilds:
            channels = []
            roles = []
            for channel in guild.channels:
                channels.append({
                    "id": str(channel.id),
                    "name": channel.name,
                    "type": channel.type[1],
                    "position": channel.position,
                    "category": channel.category.name if channel.category is not None else None,
                })
            
            for role in guild.roles:
                roles.append({
                    "id": str(role.id),
                    "name": role.name,
                    "color": role.color.value,
                    "hoist": role.position,
                })
            
            guilds.append({
                "id": str(guild.id),
                "channels": channels,
                "roles": roles,
            })

        try:
            self.socket.emit("sync", {
                "bot": {
                    "connected": True,
                    "id": str(self.discord.user.id),
                    "name": self.discord.user.name,
                    "avatar": "https://cdn.discordapp.com" + self.discord.user.avatar_url._url,
                    "discriminator": self.discord.user.discriminator
                },
                "guilds": guilds
            })
        except AttributeError:
            self.socket.emit("sync", {
                "bot": {
                    "connected": True,
                    "id": str(self.discord.user.id),
                    "name": self.discord.user.name,
                    "avatar": "https://cdn.discordapp.com" + self.discord.user.avatar.url._url,
                    "discriminator": self.discord.user.discriminator
                },
                "guilds": guilds
            })
        
    def util_setInterval(self, func, interval): 
        def func_wrapper(): 
            self.threads = [t for t in self.threads if t.is_alive()]
            self.util_setInterval(func, interval) 
            func()
        thread = threading.Timer(interval, func_wrapper)
        thread.daemon = True # python is actual dogwater
        thread.start()
        self.threads.append(thread)
        return thread
    
    def getUsingRest(self, guild_id: str, key: str):
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
    
    def updateCache(self):
        self.socket.emit("cache")
    
    def get(self, guild_id: str, key: str):
        defaultModel = {}
        guild_id = str(guild_id)
        if key in self.modelCache:
            defaultModel["code"] = -1
            defaultModel["msg"] = "OK, Using Defaults"
            defaultModel["json"] = {}
            defaultModel["json"]["value"] = self.modelCache[key]
        else:
            self.__log(f"Key {key} not found in dashboard configuration, Please check the edit page to see if the key exists.")
            defaultModel["code"] = -2
            defaultModel["msg"] = "Key not found, not present in dashboard; Check your dashboard edit page to see if the key is present."
            defaultModel["json"] = {}
            defaultModel["json"]["value"] = None
            
        if guild_id in self.cache:
            if key in self.cache[guild_id]:
                modelFound = {}
                modelFound["code"] = 0
                modelFound["msg"] = "OK, Found in Cache"
                modelFound["json"] = {}
                modelFound["json"]["value"] = self.cache[guild_id][key]
                if self.return_value: return modelFound["json"]["value"]
                else: return ValueModel(modelFound)
            else:
                if self.return_value: return defaultModel["json"]["value"]
                else: return ValueModel(defaultModel)
        else:
            if self.return_value: return defaultModel["json"]["value"]
            else: return ValueModel(defaultModel)
    
    def on(self, event: str):
        def decorator(func):
            self.events.append({
                "event": event,
                "func": func
            })
            return func
        return decorator
    
    def emit(self, event: str, data):
        for event in self.events:
            if event["event"] == event["event"]:
                asyncio.run(event["func"](data))

    def set(self, guild_id: str, key: str, value: str):
        self.socket.emit("set", {
            "guild": str(guild_id),
            "key": key,
            "value": value
        })
