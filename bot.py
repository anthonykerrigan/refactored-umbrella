# bot.py
import os
import discord
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
from dotenv import load_dotenv
import tasks
import ffxiv.news

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
FACTS_API = os.getenv('FACTS_API_ID')
BOT_PREFIX = os.getenv('BOT_PREFIX')

client = discord.Client(intents=intents)

    # Read the commands from the text file
with open('commands.txt', 'r') as f:
    commands = [line.strip() for line in f]

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
    # Don't process the message if it was sent by the bot
    if message.author == client.user:
        return

    # Check if the message contains any of the commands
    for command in commands:
        if command in message.content:
            # Execute the corresponding function from the tasks module
            await getattr(tasks, command[1:])(message)

client.run(TOKEN)