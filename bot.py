# bot.py
import os
import requests
import re
import json
import discord
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
from dotenv import load_dotenv

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
    #print(message)
    if message.author == client.user:
        return
    if message.content == "Hi":
        #print(message)
        await message.channel.send("Hello")
        print("THERE! I said Hi! Are you proud of me!?")
    if message.content.find('fact') != -1:
        print("fact found")
        limit = 1 
        api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
        response = requests.get(api_url, headers={'X-Api-Key': FACTS_API})
        parsed = response.json()
        if response.status_code == requests.codes.ok:
            await message.channel.send("Did you know " + parsed[0]['fact'])
            print("Okay random fact sent")
        else:
            print("Error:", response.status_code, response.text)
    if message.content == "!joke":
        limit = 1
        api_url = 'https://api.api-ninjas.com/v1/jokes?limit={}'.format(limit)
        response = requests.get(api_url, headers={'X-Api-Key': FACTS_API})
        parsed = response.json()
        if response.status_code == requests.codes.ok:
            await message.channel.send(parsed[0]['joke'])
        else:
            print("Error:", response.status_code, response.text)

    

client.run(TOKEN)