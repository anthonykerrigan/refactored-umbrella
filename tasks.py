import os
import json
import requests
from dotenv import load_dotenv
import pyxivapi
#from pyxivapi import Filter, Sort
import tasks
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
FACTS_API = os.getenv('FACTS_API_ID')
BOT_PREFIX = os.getenv('BOT_PREFIX')
LODESTONE_API_KEY = os.getenv('LODESTONE_TOKEN')

async def hello(message):
    await message.channel.send("Hello")
    print("THERE! I said Hi! Are you proud of me!?")


async def joke(message):
    limit = 1
    api_url = 'https://api.api-ninjas.com/v1/jokes?limit={}'.format(limit)
    response = requests.get(api_url, headers={'X-Api-Key': FACTS_API})
    parsed = response.json()
    if response.status_code == requests.codes.ok:
        await message.channel.send(parsed[0]['joke'])
    else:
        print("Error:", response.status_code, response.text)
#asas
async def fact(message):
    limit = 1 
    api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
    response = requests.get(api_url, headers={'X-Api-Key': FACTS_API})
    parsed = response.json()
    if response.status_code == requests.codes.ok:
        await message.channel.send("Did you know " + parsed[0]['fact'])
        print("Okay random fact sent")
    else:
        print("Error:", response.status_code, response.text)

async def news(message):
    url="https://na.lodestonenews.com/feed/na.xml"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == requests.codes.ok:
        await message.channel.send(response)
        print("News Delivered")
    else:
        print("Error", response.status_code, response.text  )

async def charactersearch(message): 
    client = pyxivapi.XIVAPIClient(api_key=LODESTONE_API_KEY)
    world = 'Sophia'
    forename = 'Kabaneku'
    surname = 'Lightstorm'
    character = await client.character_search(
        world=world,
        forename=forename,
        surname=surname
    )
async def roll(message):
    content = message.content.split(' ')[1]  # Assuming the dice command is the second part of the message
    parts = content.split('d')
    if len(parts) != 2 or not parts[1].isdigit() or (parts[0] and not parts[0].isdigit()):
        await message.channel.send("Invalid Command!")
        return
    number_of_dice = int(parts[0]) if parts[0] else 1
    sides = int(parts[1])
    rolled_value = [random.randint(1, sides) for _ in range(number_of_dice)]
    total = sum(rolled_value)
    await message.channel.send(f"You rolled *{rolled_value}* for a total of ***{total}***!")  # Fixed typo: channgel to channel
    
    await message.channel.send(character)
    await client.session.close()