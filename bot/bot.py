import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from datetime import datetime
from time import sleep
import os
import sys
import asyncio
import pprint
from random import randint, randrange
import random
import requests
import json
import logging
import PIL
from PIL import ImageFont, Image, ImageDraw
from os import listdir
from os.path import isfile, join
from random import choice
import urllib
import textwrap
from io import BytesIO
from pathlib import Path
from math import ceil
import sqlite3
import database.database as db

#enable the logger
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


'''
Commented until each modules are rewritten for discordpy rewrite
'''
#Extensions to load when starting the bot
#startup_extensions = ["gacha", "reddit", "danbooru", "misc", "hanapara", "goal", "wiki"] 

startup_extensions = ["danbooru", "misc", "hanapara"]

#Load the Discord API Key
with open('api.json') as api_file:    
    api_key = json.load(api_file)
discord_api = api_key["API"]["discord"]

'''
MOVE THAT TO A CONFIG FILE
'''
ownerid = 90878360053366784

description = "Zooey discord bot, breaker of Balance"
client = commands.Bot(command_prefix='$', description=description)

client.pm_help = True #Send the help message in PM

@client.event
async def on_ready():
    await client.wait_until_ready()
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(activity=discord.Game(name="Lite Mode"))

#IGNORE COMMAND NOT FOUND ERRORS
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

@client.event
async def on_message(message):
    await db.adduser(message.author.id) #Add the user if he's not registered
    #if "loli" in message.content.lower() :
    #			await client.add_reaction(message, "\U0001F693")
    await client.process_commands(message) #Keep on_message from blocking the function calls

@client.command(description="Check if the bot is active", hidden=True)
async def active(ctx):
    print("Command received")
    await ctx.send("Yes ? Do you need me ?")

@client.command(description="Restarts the bot", hidden=True)
async def restart(ctx):
    if ctx.author.id == ownerid:
        print("Restarting the bot")
        msg="Restarting the bot"
        await ctx.send(msg)
        os.execl(sys.executable, sys.executable, *sys.argv)

    else:
        msg="What are you trying to do ?! Idiot !"
        await ctx.send(msg)

@client.command(aliases=["cg"], hidden=True)
async def changegame(ctx,*, text):
    if ctx.author.id != ownerid :
        return
    await client.change_presence(activity=discord.Game(name=text))

@client.command(hidden=True)
async def load(ctx, extension_name : str):
    """Loads an extension."""
    if ctx.author.id != ownerid :
        return
    try:
        client.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} loaded.".format(extension_name))

@client.command(hidden=True)
async def unload(ctx, extension_name : str):
    """Unloads an extension."""
    if ctx.author.id != ownerid :
        return
    client.unload_extension(extension_name)
    await ctx.send("{} unloaded.".format(extension_name))


@client.command(hidden=True)
async def reload(ctx, extension_name : str):
    """Loads an extension."""
    if ctx.author.id != ownerid :
        return
    client.unload_extension(extension_name)
    try:
        client.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} reloaded.".format(extension_name))



#Load the extensions 

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            client.load_extension(extension)
            print('Loaded extension {}'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))



client.run(discord_api)
