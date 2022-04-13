# BotDash.py

https://botdash.pro

---

## Get started

```py
from botdash import Client

dash = Client(
    token="TOKEN_HERE",
    return_value=False, # Set to true
    debug=False # Use this for debugging
)
val = dash.get("GUILD_ID_HERE", "DATABASE_ID_HERE").value # REMOVE .value if "return_value" is True

print(val)
```