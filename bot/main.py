import re

import discord
import requests
import webhook_listener
import discord
from discord.ext import commands

from yaml import load
from yaml import CLoader as Loader

# This bot requires the members and reactions intents.

intents = discord.Intents.default()
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix='¡', description="LOL", intents=intents)


def process_post_request(request, *args, **kwargs):

    body_raw = request.body.read(int(request.headers['Content-Length'])) if int(request.headers.get('Content-Length', 0)) > 0 else '{}'

    print(body_raw)
    print(
        "Received request:\n"
        + "Method: {}\n".format(request.method)
        + "Headers: {}\n".format(request.headers)
        + "Args (url path): {}\n".format(args)
        + "Keyword Args (url parameters): {}\n".format(kwargs)
        + "Body: {}".format(
            request.body.read(int(request.headers["Content-Length"]))
            if int(request.headers.get("Content-Length", 0)) > 0
            else ""
        )
    )

    # Process the request!
    # ...

    return


class OpenSethClient(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.config = kwargs['config']
        
        self.bot_events = None
        self.bot_ready = False
        self.message_id = 820436177148575744

        self.session = requests.Session()

        self.webhooks = webhook_listener.Listener(port=8013, handlers={"POST": process_post_request})
        self.webhooks.start()

    @bot.event
    async def on_ready(self):
        print('Logged in as {} id {}'.format(self.user.name, self.user.id))

        self.bot_ready = True

    async def on_message(self, message):
        if not self.bot_ready:
            return

        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!notify'):
            data = re.findall('"([^"]*)"', message.content)
            if data:
                await message.reply('Would you like to notify about an event?\nPlease enter event from list:', mention_author=True)

        elif message.content.startswith('!create'):
            data = re.findall('"([^"]*)"', message.content)
            if len(data) == 3:
                await message.reply('New event created: {} on {} at {}'.format(data[0], data[1], data[2]), mention_author=True)

        elif message.content.startswith('!help'):
            await message.reply('Create a new event\nExample: "!create "World Event" "31/03/2021" "18:30"', mention_author=True)

    async def on_raw_reaction_add(self, payload):
        if not self.bot_ready:
            return
        
        message_id = payload.message_id
        
        if message_id != self.message_id:
            return
        
        member = payload.member
        user_id = payload.user_id
        data = {'payload': payload}

        print("Add notification for user_id {}".format(user_id))
        self.session.post("http://127.0.0.1:8000/events/", data=data)
        
    async def on_raw_reaction_remove(self, payload):
        if not self.bot_ready:
            return
        
        message_id = payload.message_id
        
        if message_id != self.message_id:
            return
        
        member = payload.member
        user_id = payload.user_id
        
        print("Remove notification for user_id {}".format(user_id))


def main():

    with open("config.yml") as f:
        config = load(f.read(), Loader=Loader)

    discord_token = config["bot"]["discord_token"]

    client = OpenSethClient(intents=intents, config=config)
    client.run(discord_token)


if __name__ == '__main__':
    main()
