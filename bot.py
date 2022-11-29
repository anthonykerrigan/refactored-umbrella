# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    #guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild: '
        f'{guild.name}(id: {guild.id})\n'
        f'{client.user.name} has connected to Discord!'
    )

@client.event
async def on_member_join(member):
    channels = client.get_all_channels
    channel = channels['General']
    await message.channel.send(
        f'Hi {member.name}! Welcome to Kab\'s useless attempt at making a bot!'
    )   


@client.event
async def on_message(message): 
    if message.author == client.user:
        return

    

client.run(TOKEN)