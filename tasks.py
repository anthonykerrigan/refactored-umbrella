import os
import json
import requests
from dotenv import load_dotenv
import pyxivapi
#from pyxivapi import Filter, Sort
import tasks
import random
import sqlite3

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
    await message.channel.send(character)
    await client.session.close()

async def roll(message):
    print(message)
    content = message.content.split(' ')[1]  
    parts = content.split('d')
    if len(parts) != 2 or not parts[1].isdigit() or (parts[0] and not parts[0].isdigit()):
        await message.channel.send("Invalid Command!")
        return
    number_of_dice = int(parts[0]) if parts[0] else 1
    sides = int(parts[1])
    rolled_value = [random.randint(1, sides) for _ in range(number_of_dice)]
    total = sum(rolled_value)
    await message.channel.send(f"You rolled *{rolled_value}* for a total of ***{total}***!") 

async def characters(message):
    user_name = message.author.name
    conn = sqlite3.connect('data/characters.db')
    cursor = conn.cursor()
    cursor.execute('SELECT c.* FROM user_characters uc INNER JOIN characters c ON uc.character_id = c.id WHERE uc.user_id =?', (user_name,))
    characters = cursor.fetchall()
    await message.channel.send(f"I found these characters for you! {characters}")

async def characteradd(message): 
    user_name = message.author.name 
    display_name = message.author.display_name if message.author.display_name != user_name else user_name
    user_input = message.content[len('!characteradd '):]
    input_values = [value.strip() for value in user_input.split(',')]
    if len(input_values) == 6:
        conn = sqlite3.connect('data/characters.db')
        cursor = conn.cursor()
        cursor.execute('SELECT user_name FROM users WHERE user = ?', (user_name,) )
        db_user = cursor.fetchall()
        name = input_values[0]
        race = input_values[1]
        char_class = input_values[2]
        level = input_values[3]
        hp = input_values[4]
        ac = input_values[5]
        if not db_user: 
            cursor.execute ('INSERT INTO users (user, user_name, modified) VALUES (?,?,date(CURRENT_TIMESTAMP))',(user_name, display_name))
            conn.commit()
        cursor.execute('INSERT INTO characters (name, race, class, level, hp, ac) VALUES(?,?,?,?,?,?)',(name, race, char_class, level, hp, ac))
        conn.commit()
        cursor.execute('INSERT INTO user_characters (user_id, character_id) VALUES (?, (SELECT ID FROM characters WHERE name = ?))',(user_name, name))
        conn.commit()
        await message.channel.send(f'I\'ve added {name} for you!')
    else: await message.channel.send(f'Invallid command! Please ensure you use the correct format !characteradd Name, Race, Class, Level, HP, AC')
    ()