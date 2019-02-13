# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 13:29:54 2019

@author: ckche
"""
import requests
import json

# Load the token
file = open('token.txt', 'r')
TOKEN = file.readline()
file.close()

# Load the api key
file = open('apiKey.txt', 'r')
API_KEY = file.readline()
file.close()

# Bot stuff
import discord
from discord.ext.commands import Bot
from discord.ext import commands

BOT_PREFIX = ('!')

client = Bot(command_prefix=BOT_PREFIX)

@client.command(
        name="createGroup",
        brief="Creates a new user group. Group names must be one word. This command can only be run by a Mod or higher.",
        aliases=['create_group', 'CreateGroup', 'creategroup', 'cg'],
        pass_context=True)
@commands.has_any_role('Mod', 'Admin', 'Supreme Overlord')
async def createGroup(context, groupName):
    await client.create_role(context.message.author.server, name=groupName, mentionable=True)    
    await client.send_message(context.message.channel, 'Group created!')

@client.command(
        name="joinGroup",
        brief="Join a group. Note: You cannot join a group above member with this command.",
        aliases=['joingroup', 'JouGroup', 'jg', 'join_group'],
        pass_context=True)
async def joinGroup(context, groupName):
    user = context.message.author
    role = discord.utils.get(user.server.roles, name=groupName)
    await client.add_roles(user, role)
    await client.send_message(context.message.channel, 'Group joined!')

@client.command(
    name="meme",
    brief="Given a search term find a random relevant meme. Or just get a random one if no search term is given.",
    aliases=['Meme', 'MEME'],
    pass_context=True
)
async def meme(context, searchText="None"):
    # Get the gif
    payload = {
        'api_key': API_KEY,
        'tag': searchText
    }
    if searchText == "None":
        payload.pop('q')

    response = requests.get('https://api.giphy.com/v1/gifs/random', params=payload)
    data = json.loads(response.text)

    url = data['data']['embed_url']
    
    # Respond
    user = context.message.author
    channel = client.get_channel('454407729587552266') #  Memes channel # 543884296239448079 Test Channel

    embed = discord.Embed()
    embed.set_image(url=url)

    await client.send_message(channel, user.mention)
    await client.send_message(channel, url)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)