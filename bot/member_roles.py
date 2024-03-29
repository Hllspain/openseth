
import time
import discord
from discord.utils import get

from yaml import load
from yaml import Loader

with open("config.yml") as f:
    config = load(f.read(), Loader=Loader)

discord_token = config["bot"]["discord_token"]

guild_id = config["bot"]["guild"]

log_chat_id = config["bot"]["chat_id"]
welcome_chat_id = config["bot"]["welcome_chat_id"]

roles_id = config["bot"]["roles"]
welcome_msg = config["bot"]["welcome_msg"]
boot_msg = config["bot"]["boot_msg"]

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True


client = discord.Client(intents=intents)
    

@client.event
async def on_ready():
    channel = client.get_channel(log_chat_id)
    await channel.send(eval(boot_msg))


@client.event
async def on_member_remove(member):
    channel = client.get_channel(log_chat_id)
        
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    await channel.send(f"{current_time} <-- Miembro <@{member.id}> {member} se fue.")

@client.event
async def on_member_update(before, after):
    
    guild = client.get_guild(guild_id)
    channel = client.get_channel(log_chat_id)
    welcome_room = client.get_channel(welcome_chat_id)
    
    if before.pending == True and after.pending == False:
        
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        
        for role_id in roles_id:
            role = get(guild.roles, id=role_id)
        
            if role is not None:
                # await channel.send(f"\t<@{role_id}>")
                await after.add_roles(role)

        await channel.send(f"{current_time} --> Nuevo miembro <@{after.id}>")
        await welcome_room.send(eval(welcome_msg))

client.run(discord_token)
