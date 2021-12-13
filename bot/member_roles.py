
import time
import discord
from discord.utils import get

from yaml import load
from yaml import Loader

with open("config.yml") as f:
    config = load(f.read(), Loader=Loader)

discord_token = config["bot"]["discord_token"]
guild_id = config["bot"]["guild"]
roles_id = config["bot"]["roles"]
welcome_msg = config["bot"]["welcome"]

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True


client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_member_update(before, after):
    if before.pending == True and after.pending == False:
        
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print(f"{current_time} Adding {after} new role")
        
        guild = client.get_guild(guild_id)
        for role_id in roles_id:
            role = get(guild.roles, id=role_id)
        
            if role is not None:
                print(f"\t{role}")
                await after.add_roles(role)
            
        await after.send(welcome_msg)

client.run(discord_token)
