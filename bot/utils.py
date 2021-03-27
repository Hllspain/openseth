from time import sleep
from discord_webhook import DiscordWebhook, DiscordEmbed


class WebHookUtils:
    """" https://github.com/lovvskillz/python-discord-webhook """
    @staticmethod
    def send_webhook():
        webhook = DiscordWebhook(url="your webhook url", username="New Webhook Username")

        embed = DiscordEmbed(
            title="Embed Title", description="Your Embed Description", color='03b2f8'
        )
        embed.set_author(
            name="Author Name",
            url="https://github.com/lovvskillz",
            icon_url="https://avatars0.githubusercontent.com/u/14542790",
        )
        embed.set_footer(text="Embed Footer Text")
        embed.set_timestamp()
        # Set `inline=False` for the embed field to occupy the whole line
        embed.add_embed_field(name="Field 1", value="Lorem ipsum", inline=False)
        embed.add_embed_field(name="Field 2", value="dolor sit", inline=False)
        embed.add_embed_field(name="Field 3", value="amet consetetur")
        embed.add_embed_field(name="Field 4", value="sadipscing elitr")

        webhook.add_embed(embed)
        response = webhook.execute()

    @staticmethod
    def edit_weebhook():
        webhook = DiscordWebhook(url='your webhook url', content='Webhook content before edit')
        sent_webhook = webhook.execute()
        webhook.content = 'After Edit'
        sleep(10)
        sent_webhook = webhook.edit(sent_webhook)

    @staticmethod
    def delete_webhook():
        webhook = DiscordWebhook(url='your webhook url', content='Webhook Content')
        sent_webhook = webhook.execute()
        sleep(10)
        webhook.delete(sent_webhook)