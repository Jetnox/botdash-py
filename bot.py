import discord
import botdash
import time

DISCORD_TOKEN = "haha"
BOTDASH_TOKEN = "you thought"

intents = discord.Intents.all()
client = discord.Client(intents=intents)
dashboard = botdash.Client(
    token=BOTDASH_TOKEN,
    return_value=True,
    debug=True,
    client=client
)

@dashboard.on("change")
async def change(data):
    # THIS SHOULD ALWAYS BE ASYNC!!!

    #{ key, value, oldValue, guild }
    # Key is the key / database ID of the setting.
    # Value is the new value of the setting.
    # oldValue is the old value of the setting.
    # guild is the guild ID of the guild the setting was changed for.
    return

@dashboard.on("trigger")
async def trigger(data):
    # THIS SHOULD ALWAYS BE ASYNC!!!

    # { name, currentSave, guildId }
    # Name is the key / database ID of the setting.
    # currentSave is the current state/save of the page | [ { Key: Value }, { Key: Value } ]
    # guildId is the guild ID of the guild the trigger is for.
    return

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    if msg.content.startswith('!get'):

        start_time = time.time()
        value = dashboard.get(msg.guild.id, "prefix")
        end_time = time.time()

        start_time_two = time.time()
        valueTwo = dashboard.getUsingRest(msg.guild.id, "prefix")
        end_time_two = time.time()

        await msg.channel.send(f"```Prefix NEW Method: {value} - Time: {end_time - start_time}\nPrefix OLD Method: {valueTwo} - Time: {end_time_two - start_time_two}```")
    if msg.content.startswith('!set'):
        dashboard.set(msg.guild.id, "prefix", msg.content[4:])
        await msg.channel.send(f"Set prefix to {msg.content[4:]}")


client.run(DISCORD_TOKEN)