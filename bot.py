# bot.py
import os
import discord
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
from dotenv import load_dotenv
import tasks

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
FACTS_API = os.getenv('FACTS_API_ID')
BOT_PREFIX = os.getenv('BOT_PREFIX')

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    #guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild: \n'
        f'{guild.name}(id: {guild.id})\n'
        f'{client.user.name} has connected to Discord!'
    )

@client.event
async def on_member_join(member):
    channels = client.get_all_channels
    channel = channels['General']
    await discord.Message.channel.send(
        f'Hi {member.name}! Welcome to Kab\'s useless attempt at making a bot!'
    )
    print("Message Sent")   

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        facts = message.content.find("fact")
        if facts == 0:
            facts = message.content
        match message.content:
            case facts():
                print("Received Fact message: ", message.content)
                await tasks.fact(message)
            case "!joke":
                print("Received Joke message: ", message.content)
                await tasks.joke(message)
            case "Hi":
                print("Received Hi message: ", message.content)
                await tasks.hello(message)
            case _:
                print("Received message: ", message.content)

client.run(TOKEN)