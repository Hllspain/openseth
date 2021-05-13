import asyncio
import random
from pprint import pprint

import discord
from discord import NotFound, Forbidden
from discord.ext import commands
from discord.utils import get

from yaml import load
from yaml import Loader

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
            # welcome = f"hola {user.name}"
            # await send_user_dm(user, welcome)

            try:
                await send_user_dm(user, message)
            except Exception as e:
                await ctx.send(f"error for user {user} {e}")
                with open("error.log") as log_f:
                    log_f.write(f"{user}\n")

            with open("ok.log") as log_f:
                log_f.write(f"{user}\n")

            await ctx.send(f"Sent message to {user}")
            await asyncio.sleep(10)
            num_users += 1
            # await asyncio.sleep(random.choice([40, 60]))

    await ctx.send(f"Done spam sent to {num_users} users")


@bot.command(pass_context=True)
@commands.has_role("Administrador")
async def get_members(ctx, channel: discord.TextChannel, message_id: int, role: discord.Role):
    try:
        msg = await channel.fetch_message(message_id)

        pprint(msg)

        reactions = msg.reactions

        print(reactions)

        for reactor in reactions:
            if str(reactor) == '👍':
                print(reactor)
                print("users")

                async for user in reactor.users():
                    pass
                    # await user.add_roles(role)

            # reactors = await client(reactor)
            # #from here you can do whatever you need with the member objects
            # for member in reactors
            #     print(member.name)
    except NotFound:
        print("not found")

bot.run(discord_token)
