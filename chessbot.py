# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 13:29:54 2019

@author: ckche
"""

# Load the token
file = open('token.txt', 'r')
TOKEN = file.readline()
file.close()

# Bot stuff
import discord
from discord.ext.commands import Bot
from discord.ext import commands

BOT_PREFIX = ('!')

client = Bot(command_prefix=BOT_PREFIX)

@client.command(
        name="createGroup",
        brief="Creates a new user group. (group names must be one word)",
        aliases=['create_group', 'CreateGroup', 'creategroup', 'cg'],
        pass_context=True)
@commands.has_any_role('Mod', 'Admin', 'Supreme Overlord')
async def createGroup(context, groupName):
    #perms = discord.Permissions(mentionable=True)
    await client.create_role(context.message.author.server, name=groupName, mentionable=True)    
    await client.send_message(context.message.channel, 'Group created!')

@client.command(
        name="joinGroup",
        brief="Join a group.",
        aliases=['joingroup', 'JouGroup', 'jg', 'join_group'],
        pass_context=True)
async def joinGroup(context, groupName):
    
    user = context.message.author
    role = discord.utils.get(user.server.roles, name=groupName)
    await client.add_roles(user, role)
    await client.send_message(context.message.channel, 'Group joined!')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)