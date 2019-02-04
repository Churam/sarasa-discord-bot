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
import sqlite3

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

startup_extensions = ["danbooru", "misc"]

#Load the Discord API Key
with open('api.json') as api_file:    
    api_key = json.load(api_file)
discord_api = api_key["API"][0]["discord"]

'''
MOVE THAT TO A CONFIG FILE
'''
ownerid = 90878360053366784

description = "Sarasa bot for Hanapara, please give me plenty of cake !"
client = commands.Bot(command_prefix='$', description=description)

client.pm_help = True #Send the help message in PM

   
#db connection
dbcon = sqlite3.connect("./database/sarasa_db.sqlite3")
curs = dbcon.cursor()

'''
def old_adduser(userid, username):
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
            usrdata["waifu"] = []
            usrdata["husbando"] = []
            usrdata["spark"] = {"crystals" : 0, "tickets" : 0, "10tickets" : 0}
            json.dump(usrdata, x, indent=2, ensure_ascii=False)
'''

async def check_user(uid):
    curs.execute("SELECT uid FROM main WHERE uid = (?)", (uid,))
    exists = curs.fetchone()
    if exists :
        return False
    else :
        return True

async def adduser(userid) :
    if await check_user(userid) :
        title = ""
        about_me = ""
        money = 0
        gbf_name = ""
        profile_mode = "still"
        waifu = []
        husbando = []
        datas = [userid, title, about_me, money, gbf_name, profile_mode, json.dumps(userdata['waifu']), json.dumps(userdata['husbando']), None, None]
        curs.execute('INSERT INTO main VALUES (?,?,?,?,?,?,?,?,?,?)', datas)
        db.commit()
    else :
        pass

def usrdata(userid):
    return "./users/{}/userdata.json".format(userid)

@client.event
async def on_ready():
    await client.wait_until_ready()
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    await adduser(message.author.id) #Add the user if he's not registered
    #if "loli" in message.content.lower() :
    #			await client.add_reaction(message, "\U0001F693")
    await client.process_commands(message) #Keep on_message from blocking the function calls

@client.command(description="Check if the bot is active")
async def active(ctx):
    print("Command received")
    await ctx.send("Yes ? Do you need me ?")

@client.command()
async def ctxtest(ctx):
	await ctx.send("{} {}".format(ctx.author.name, ctx.author.id))

@client.command(description="Restarts the bot")
async def restart(ctx):
    if ctx.author.id == ownerid:
        print("Restarting the bot")
        msg="Restarting the bot"
        await ctx.send(msg)
        os.execl(sys.executable, sys.executable, *sys.argv)

    else:
        msg="What are you trying to do ?! Idiot !"
        await ctx.send(msg)

@client.command(aliases=["cg"])
async def changegame(ctx,*, text):
    if ctx.author.id != ownerid :
        pass
    else :
        await client.change_presence(activity=discord.Game(name=text))

@client.command()
async def load(ctx, extension_name : str):
    """Loads an extension."""
    try:
        client.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} loaded.".format(extension_name))

@client.command()
async def unload(ctx, extension_name : str):
    """Unloads an extension."""
    client.unload_extension(extension_name)
    await ctx.send("{} unloaded.".format(extension_name))


@client.command()
async def reload(ctx, extension_name : str):
    """Loads an extension."""
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
