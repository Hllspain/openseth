import asyncio
import random

import discord
from discord.ext import commands

from yaml import load
from yaml import CLoader as Loader

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot('¿', intents=intents)


with open("config.yml") as f:
    config = load(f.read(), Loader=Loader)

discord_token = config["bot"]["discord_token"]


async def send_user_dm(user, message):
    try:
        await user.send(message)
        print(message)
    except AttributeError as e:
        print("es un bot", e)


@bot.command()
@commands.has_role("Administrador")
async def add_role(ctx: commands.Context, new_role: discord.Role, to: str, role: discord.Role):
    for member in ctx.guild.members:
        if role in member.roles:
            print(f"adding member {member.name} with role {role.name} to role {new_role.name}")
            await member.add_roles(new_role)


@bot.command()
@commands.has_role("Administrador")
async def spam_user(ctx: commands.Context, target: discord.User, message: str):
    await ctx.send(f"sending message to @{target.id}")
    await send_user_dm(target, message)
    await ctx.send(f"Done spam sent to {target.name}")


@bot.command()
@commands.has_role("Administrador")
async def spam_role(ctx: commands.Context, target: discord.Role, message: str):
    num_users = 0
    await ctx.send(f"Yes Sir")
    for user in ctx.guild.members:
        if target in user.roles:
            welcome = f"hola {user.name}"
            await send_user_dm(user, welcome)
            await send_user_dm(user, message)
            await asyncio.sleep(3)
            num_users += 1
            # await asyncio.sleep(random.choice([40, 60]))

    await ctx.send(f"Done spam sent to {num_users} users")

bot.run(discord_token)
