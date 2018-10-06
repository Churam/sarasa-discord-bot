import discord
from discord.ext import commands
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

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


#Extensions to load when starting the bot
startup_extensions = ["gacha", "reddit", "danbooru", "misc", "hanapara", "goal", "wiki"]


#Load the Discord API Key
with open('api.json') as api_file:    
    api_key = json.load(api_file)
discord_api = api_key["API"][0]["discord"]



description = "Sarasa bot for Hanapara, please give me plenty of cake !"
client = commands.Bot(command_prefix='$', description=description )
bot_dir = "."
os.chdir(bot_dir)
ownerid = '90878360053366784'
gw_server_id = "246519048559394817"

client.pm_help = True #Send the help message in PM
hanapara_server = 0 
general_channel = 0
gw_st = 0
scam_on = 0

    
def adduser(userid, username):
    if not os.path.exists("./users/{}/".format(userid)) :
        os.makedirs("./users/{}/".format(userid))
        with open('./users/{}/userdata.json'.format(userid), 'xt', encoding="UTF-8") as f:
            f.write('{}')
            f.close()
        with open('./users/{}/userdata.json'.format(userid)) as fp:
            usrdata = json.load(fp)

        with open('./users/{}/userdata.json'.format(userid),'w', encoding="UTF-8") as x:
            usrdata["username"] = ""
            usrdata["title"] = ""
            usrdata["aboutme"] = ""
            usrdata["money"] = 0
            usrdata["waifu"] = ""
            usrdata["husbando"] = ""
            usrdata["spark"] = {"crystals" : 0, "tickets" : 0, "10tickets" : 0}
            json.dump(usrdata, x, indent=2, ensure_ascii=False)

def usrdata(userid):
    return "./users/{}/userdata.json".format(userid)

@client.event
async def on_ready():
    await client.wait_until_ready()
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    global hanapara_server
    global general_channel
    general_channel = client.get_channel(id='246519048559394817')
    hanapara_server = client.get_server(id='246519048559394817')


@client.event
async def on_message(message):
    adduser(message.author.id, message.author.name) #Add the user if he's not registered
    #if "loli" in message.content.lower() :
    #			await client.add_reaction(message, "\U0001F693")
    await client.process_commands(message)

@client.command(description="Check if the bot is active")
async def active():
    print("Command received")
    await client.say("Yes ? Do you need me ?")

@client.command(description="Restarts the bot", pass_context=True)
async def restart(ctx):
    if ctx.message.author.id == ownerid:
        print("Restarting the bot")
        msg="Restarting the bot"
        await client.say(msg)
        os.execl(sys.executable, sys.executable, *sys.argv)

    else:
        msg="What are you trying to do ?! Idiot !"
        await client.say(msg)

@client.command(pass_context=True,aliases=["cg"])
async def changegame(ctx,*, text):
    uid = ctx.message.author.id
    if uid not in ownerid :
        pass
    else :
        await client.change_presence(game=discord.Game(name=text))

@client.command()
async def load(extension_name : str):
    """Loads an extension."""
    try:
        client.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await client.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await client.say("{} loaded.".format(extension_name))

@client.command()
async def unload(extension_name : str):
    """Unloads an extension."""
    client.unload_extension(extension_name)
    await client.say("{} unloaded.".format(extension_name))


@client.command()
async def reload(extension_name : str):
    """Loads an extension."""
    client.unload_extension(extension_name)
    try:
        client.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await client.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await client.say("{} reloaded.".format(extension_name))



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
