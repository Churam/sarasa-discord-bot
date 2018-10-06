import discord
from discord.ext import commands
import os
from pybooru import Danbooru
from random import randint
from random import randrange
import random
import json
from random import choice
import requests
import asyncio

with open('api.json') as data_file:    
    data = json.load(data_file)

discord_api = data["API"][0]["discord"]
danbooru_api = data["API"][1]["danbooru"]

picbot = Danbooru('danbooru', username='Akeyro', api_key=danbooru_api)
client = commands.Bot(command_prefix='-', description="Sarasa picture bot" )
tag_blacklist = ["lolicon", "scat", "guro", "vore", "rape", "spoiler"]

@client.event
async def on_ready():
    await client.wait_until_ready()
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('Successfully launched the picbot')
    print('------')
    client.remove_command("help")



@client.command(description="Retrieve a random safe pic of the given tag on Danbooru",pass_context=True)
async def safe(ctx, *, message : str):
    m_channel = ctx.message.channel
    m_author = ctx.message.author
    message = message.replace(" ","_")
    await client.send_typing(m_channel)
    if message.endswith(" "):
        message = message[:-1]
    path = "./"
    max_limit = 200
    picture = picbot.post_list(tags=message+" rating:safe", limit=max_limit, random=True)
    pic_count = len(picture)
    if pic_count == 0:
        await client.say("There is no picture with this tag")

    else :
        random_pic = randint(0, pic_count - 1)
        picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
        pic_id = str(picture[random_pic]['id'])
        pic_show = picbot.post_show(pic_id)
        pic_url = "https://danbooru.donmai.us" + str(pic_show['file_url'])
        pic_source = str(pic_show['pixiv_id'])
        if pic_source == "None":
            pic_source = "<" + str(pic_show['source']) + ">"
        else:
            pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) + ">"
        dl = requests.get(pic_url)
        with open(path + str(picture[random_pic]['id'])+".jpg", "wb") as f:
            f.write(dl.content)
        picpath = "./"+str(picture[random_pic]['id'])+".jpg"
        m_content = "{}\nSource : {}".format(m_author.mention,pic_source)

        await client.send_file(ctx.message.channel, picpath, content=m_content)
        await asyncio.sleep(5)
        os.remove(path + str(picture[random_pic]['id'])+".jpg")

@client.command(description="Retrieve a random NSFW pic of the given tag on Danbooru",pass_context=True)
async def hentai(ctx, *, message : str):
    m_channel = ctx.message.channel
    channelname = m_channel.name
    m_server = ctx.message.server
    m_author = ctx.message.author
    blacklistcheck = False
    message = message.replace(" ","_")
    if message.endswith(" "):
        message = message[:-1]
    roleadd = discord.utils.get(m_server.roles, name="Apples")
    roleget = str(roleadd)

    if "nsfw" not in channelname:
        await client.say("Sorry, you can't do that here")

    elif message in tag_blacklist :
        await client.say("This tag is blacklisted.")

    else:
        max_limit = 100
        picture = picbot.post_list(tags=message+" rating:explicit", limit=max_limit, random=True)
        pic_count = len(picture)   
        path = "./"
        await client.send_typing(m_channel)
        if pic_count == 0:
            await client.say("There is no picture with this tag")

        else :
            while blacklistcheck is False :
                tagblacklist = False
                random_pic = randint(0, pic_count - 1)
                picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
                pic_id = str(picture[random_pic]['id'])
                pic_show = picbot.post_show(pic_id)
                pic_url = "https://danbooru.donmai.us" + str(pic_show['file_url'])
                pic_source = str(pic_show['pixiv_id'])
                pic_tags = str(pic_show['tag_string_general'])

                for i in tag_blacklist:
                    if i in pic_tags :
                        print("Blacklisted tag detected")
                        tagblacklist = True

                if tagblacklist is False :
                    blacklistcheck = True

            if pic_source == "None":
                pic_source = "<" + str(pic_show['source']) + ">"
            else:
                pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) +">"
            dl = requests.get(pic_url)
            with open(path + str(picture[random_pic]['id'])+".jpg", "wb") as f:
                f.write(dl.content)
            picpath = "./"+str(picture[random_pic]['id'])+".jpg"
            m_content = "{}\nSource : {}".format(m_author.mention,pic_source)
            
            await client.send_file(m_channel, picpath, content=m_content)
            await asyncio.sleep(5)
            os.remove(path + str(picture[random_pic]['id'])+".jpg")

@client.command(description="Recruit a Granblue Fantasy character from Safebooru !",pass_context=True)
async def gbf(ctx):
    m_channel = ctx.message.channel
    m_author = ctx.message.author
    await client.send_typing(m_channel)
    path = "./"
    max_limit = 200
    picture = picbot.post_list(tags="granblue_fantasy"+" rating:safe", limit=max_limit, random=True)
    pic_count = len(picture)
    if pic_count == 0:
        await client.say("There is no picture with this tag")

    else :
        random_pic = randint(0, pic_count - 1)
        picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
        pic_id = str(picture[random_pic]['id'])
        pic_show = picbot.post_show(pic_id)
        pic_url = "https://danbooru.donmai.us" + str(pic_show['file_url'])
        pic_source = str(pic_show['pixiv_id'])
        pic_chara = str(pic_show['tag_string_character'])
        if pic_source == "None" or pic_source == None:
            pic_source = "<" + str(pic_show['source']) + ">"
        if pic_show['source']== "None" or pic_show['source'] == None:
            pic_source = "Granblue Fantasy"
        else:
            pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) + ">"
        dl = requests.get(pic_url)
        with open(path + str(picture[random_pic]['id'])+".jpg", "wb") as f:
            f.write(dl.content)
        picpath = "./"+str(picture[random_pic]['id'])+".jpg"
        pic_chara = pic_chara.title()
        pic_chara = pic_chara.replace(" "," and ")
        pic_chara = pic_chara.replace("_"," ")
        if " (Granblue Fantasy)" in pic_chara:
            pic_chara = pic_chara.replace(" (Granblue Fantasy)","")
        if pic_chara.endswith(" "):
            pic_chara = pic_chara[:-1]   
        m_content="{} You recruited {} in your crew !\nSource : {}".format(m_author.mention, pic_chara, pic_source)
        
        await client.send_file(ctx.message.channel, picpath, content=m_content)
        await asyncio.sleep(5)
        os.remove(path + str(picture[random_pic]['id'])+".jpg")

@client.command(description="Construct a Kanmusu from the great land of Safebooru !",pass_context=True)
async def kanmusu(ctx):
    m_channel = ctx.message.channel
    m_author = ctx.message.author
    await client.send_typing(m_channel)
    path = "./"
    max_limit = 200
    picture = picbot.post_list(tags="Kantai_Collection"+" rating:safe", limit=max_limit, random=True)
    pic_count = len(picture)
    if pic_count == 0:
        await client.say("There is no picture with this tag")

    else :
        random_pic = randint(0, pic_count - 1)
        picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
        pic_id = str(picture[random_pic]['id'])
        pic_show = picbot.post_show(pic_id)
        pic_url = "https://danbooru.donmai.us" + str(pic_show['file_url'])
        pic_source = str(pic_show['pixiv_id'])
        pic_chara = str(pic_show['tag_string_character'])
        if pic_source == "None" or pic_source == None:
            pic_source = "<" + str(pic_show['source']) + ">"
        if pic_show['source']== "None" or pic_show['source'] == None:
            pic_source = "Kantai Collection"
        else:
            pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) + ">"
        dl = requests.get(pic_url)
        with open(path + str(picture[random_pic]['id'])+".jpg", "wb") as f:
            f.write(dl.content)
        picpath = "./"+str(picture[random_pic]['id'])+".jpg"
        pic_chara = pic_chara.title()
        pic_chara = pic_chara.replace(" "," and ")
        pic_chara = pic_chara.replace("_"," ")
        if " (Kantai Collection)" in pic_chara:
            pic_chara = pic_chara.replace(" (Kantai Collection)","")
        if pic_chara.endswith(" "):
            pic_chara = pic_chara[:-1]   
        m_content = "{} You constructed {} in your Naval Base !\nSource : {}".format(m_author.mention, pic_chara, pic_source)
        
        await client.send_file(ctx.message.channel, picpath, content=m_content)
        await asyncio.sleep(5)
        os.remove(path + str(picture[random_pic]['id'])+".jpg")

@client.command(description="Will your girl be SHINY ?",pass_context=True)
async def lovelive(ctx):
    m_channel = ctx.message.channel
    m_author = ctx.message.author
    await client.send_typing(m_channel)
    path = "./"
    max_limit = 200
    picture = picbot.post_list(tags="love_live!"+" rating:safe", limit=max_limit, random=True)
    pic_count = len(picture)
    if pic_count == 0:
        await client.say("There is no picture with this tag")

    else :
        random_pic = randint(0, pic_count - 1)
        picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
        pic_id = str(picture[random_pic]['id'])
        pic_show = picbot.post_show(pic_id)
        pic_url = "https://danbooru.donmai.us" + str(pic_show['file_url'])
        pic_source = str(pic_show['pixiv_id'])
        pic_chara = str(pic_show['tag_string_character'])
        if pic_source == "None" or pic_source == None:
            pic_source = "<" + str(pic_show['source']) + ">"
        if pic_show['source']== "None" or pic_show['source'] == None:
            pic_source = "Love Live!"
        else:
            pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) + ">"
        dl = requests.get(pic_url)
        with open(path + str(picture[random_pic]['id'])+".jpg", "wb") as f:
            f.write(dl.content)
        picpath = "./"+str(picture[random_pic]['id'])+".jpg"
        pic_chara = pic_chara.title()
        pic_chara = pic_chara.replace(" "," and ")
        pic_chara = pic_chara.replace("_"," ")
        if " (Love Live!)" in pic_chara:
            pic_chara = pic_chara.replace(" (Love Live!)","")
        if pic_chara.endswith(" "):
            pic_chara = pic_chara[:-1]   
        m_content = "{} You got {} !\nSource : {}".format(m_author.mention, pic_chara, pic_source)
        
        await client.send_file(ctx.message.channel, picpath, content=m_content)
        await asyncio.sleep(5)
        os.remove(path + str(picture[random_pic]['id'])+".jpg")

@client.command(description="Will your girl be SHINY ?",pass_context=True)
async def muse(ctx):
    m_channel = ctx.message.channel
    m_author = ctx.message.author
    await client.send_typing(m_channel)
    path = "./"
    max_limit = 200
    picture = picbot.post_list(tags="love_live!_school_idol_project"+" rating:safe", limit=max_limit, random=True)
    pic_count = len(picture)
    if pic_count == 0:
        await client.say("There is no picture with this tag")

    else :
        random_pic = randint(0, pic_count - 1)
        picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
        pic_id = str(picture[random_pic]['id'])
        pic_show = picbot.post_show(pic_id)
        pic_url = "https://danbooru.donmai.us" + str(pic_show['file_url'])
        pic_source = str(pic_show['pixiv_id'])
        pic_chara = str(pic_show['tag_string_character'])
        if pic_source == "None" or pic_source == None:
            pic_source = "<" + str(pic_show['source']) + ">"
        if pic_show['source']== "None" or pic_show['source'] == None:
            pic_source = "Love Live!"
        else:
            pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) + ">"
        dl = requests.get(pic_url)
        with open(path + str(picture[random_pic]['id'])+".jpg", "wb") as f:
            f.write(dl.content)
        picpath = "./"+str(picture[random_pic]['id'])+".jpg"
        pic_chara = pic_chara.title()
        pic_chara = pic_chara.replace(" "," and ")
        pic_chara = pic_chara.replace("_"," ")
        if " (Love Live!)" in pic_chara:
            pic_chara = pic_chara.replace(" (Love Live!)","")
        if pic_chara.endswith(" "):
            pic_chara = pic_chara[:-1]   
        m_content = "{} You got {} !\nSource : {}".format(m_author.mention, pic_chara, pic_source)
        
        await client.send_file(ctx.message.channel, picpath, content=m_content)
        await asyncio.sleep(5)
        os.remove(path + str(picture[random_pic]['id'])+".jpg")

@client.command(description="Will your girl be SHINY ?",pass_context=True)
async def aqours(ctx):
    m_channel = ctx.message.channel
    m_author = ctx.message.author
    await client.send_typing(m_channel)
    path = "./"
    max_limit = 200
    picture = picbot.post_list(tags="love_live!_sunshine!!"+" rating:safe", limit=max_limit, random=True)
    pic_count = len(picture)
    if pic_count == 0:
        await client.say("There is no picture with this tag")

    else :
        random_pic = randint(0, pic_count - 1)
        picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
        pic_id = str(picture[random_pic]['id'])
        pic_show = picbot.post_show(pic_id)
        pic_url = "https://danbooru.donmai.us" + str(pic_show['file_url'])
        pic_source = str(pic_show['pixiv_id'])
        pic_chara = str(pic_show['tag_string_character'])
        if pic_source == "None" or pic_source == None:
            pic_source = "<" + str(pic_show['source']) + ">"
        if pic_show['source']== "None" or pic_show['source'] == None:
            pic_source = "Love Live!"
        else:
            pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) + ">"
        dl = requests.get(pic_url)
        with open(path + str(picture[random_pic]['id'])+".jpg", "wb") as f:
            f.write(dl.content)
        picpath = "./"+str(picture[random_pic]['id'])+".jpg"
        pic_chara = pic_chara.title()
        pic_chara = pic_chara.replace(" "," and ")
        pic_chara = pic_chara.replace("_"," ")
        if " (Love Live!)" in pic_chara:
            pic_chara = pic_chara.replace(" (Love Live!)","")
        if pic_chara.endswith(" "):
            pic_chara = pic_chara[:-1]   
        m_content = "{} You got {} !\nSource : {}".format(m_author.mention, pic_chara, pic_source)
        
        await client.send_file(ctx.message.channel, picpath, content=m_content)
        await asyncio.sleep(5)
        os.remove(path + str(picture[random_pic]['id'])+".jpg")

@client.command(description="Summon a servant from Safebooru !",pass_context=True)
async def fate(ctx):
    m_channel = ctx.message.channel
    m_author = ctx.message.author
    path = "./"
    max_limit = 200
    picture = picbot.post_list(tags="Fate/Grand_Order"+" rating:safe", limit=max_limit, random=True)
    pic_count = len(picture)
    await client.send_typing(m_channel)
    if pic_count == 0:
        await client.say("There is no picture with this tag")

    else :
        random_pic = randint(0, pic_count - 1)
        picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
        pic_id = str(picture[random_pic]['id'])
        pic_show = picbot.post_show(pic_id)
        pic_url = "https://danbooru.donmai.us" + str(pic_show['file_url'])
        pic_source = str(pic_show['pixiv_id'])
        pic_chara = str(pic_show['tag_string_character'])
        if pic_source == "None" or pic_source == None:
            pic_source = "<" + str(pic_show['source']) + ">"
        if pic_show['source']== "None" or pic_show['source'] == None:
            pic_source = "Fate/Grand Order"
        else:
            pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) + ">"
        dl = requests.get(pic_url)
        with open(path + str(picture[random_pic]['id'])+".jpg", "wb") as f:
            f.write(dl.content)
        picpath = "./"+str(picture[random_pic]['id'])+".jpg"
        pic_chara = pic_chara.title()
        pic_chara = pic_chara.replace(" "," and ")
        pic_chara = pic_chara.replace("_"," ")
        if " (Fate/Grand Order)" in pic_chara :
            pic_chara = pic_chara.replace(" (Fate/Grand Order)","")
        if pic_chara.endswith(" "):
            pic_chara = pic_chara[:-1]   
        m_content= "{} You summoned {} !\nSource : {}".format(m_author.mention, pic_chara, pic_source)
        
        await client.send_file(ctx.message.channel, picpath, content=m_content)
        await asyncio.sleep(5)
        os.remove(path + str(picture[random_pic]['id'])+".jpg")

@client.command(description="Scout an Idol from Safebooru !",pass_context=True)
async def idol(ctx):
    m_channel = ctx.message.channel
    m_author = ctx.message.author
    await client.send_typing(m_channel)
    path = "./"
    max_limit = 200
    picture = picbot.post_list(tags="Idolmaster"+" rating:safe", limit=max_limit, random=True)
    pic_count = len(picture)
    if pic_count == 0:
        await client.say("There is no picture with this tag")

    else :
        random_pic = randint(0, pic_count - 1)
        picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
        pic_id = str(picture[random_pic]['id'])
        pic_show = picbot.post_show(pic_id)
        pic_url = "https://danbooru.donmai.us" + str(pic_show['file_url'])
        pic_source = str(pic_show['pixiv_id'])
        pic_chara = str(pic_show['tag_string_character'])
        if pic_source == "None" or pic_source == None:
            pic_source = "<" + str(pic_show['source']) + ">"
        if pic_show['source']== "None" or pic_show['source'] == None:
            pic_source = "Idolm@ster"
        else:
            pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) + ">"
        dl = requests.get(pic_url)
        with open(path + str(picture[random_pic]['id'])+".jpg", "wb") as f:
            f.write(dl.content)
        picpath = "./"+str(picture[random_pic]['id'])+".jpg"
        pic_chara = pic_chara.title()
        pic_chara = pic_chara.replace(" "," and ")
        pic_chara = pic_chara.replace("_"," ")
        if " (Idolmaster)" in pic_chara :
            pic_chara = pic_chara.replace(" (Idolmaster)","")
        if "Producer" in pic_chara:
            pic_chara = pic_chara.replace("Producer","")
        if pic_chara.endswith(" "):
            pic_chara = pic_chara[:-1]   
        m_content="{} You scouted {} in your production !\nSource : {}".format(m_author.mention, pic_chara, pic_source)
        
        await client.send_file(ctx.message.channel, picpath, content=m_content)
        await asyncio.sleep(5)
        os.remove(path + str(picture[random_pic]['id'])+".jpg")

# ----------------------------- Waifu/Husbando Commands ----------------------------- #

@client.command(description="Get a picture of one your waifu", pass_context=True)
async def waifu(ctx):
    m_channel = ctx.message.channel
    m_author = ctx.message.author
    m_author_id = m_author.id
    await client.send_typing(m_channel)
    with open('data.json') as json_file:
        datas = json.load(json_file)
    tag = choice(datas[m_author_id]["waifu"])
    tag = tag.replace(" ", "_")
    path = "./"
    max_limit = 200
    picture = picbot.post_list(tags=tag+" rating:safe", limit=max_limit, random=True)
    pic_count = len(picture)
    try :
        if pic_count == 0:
            await client.say("There is no picture with this tag")

        elif m_author_id not in datas :
            await client.say("You aren't registered. Please use **$register**.")

        elif tag is "" :
            await client.say("You have no waifu. Please register one with $register waifu")

        else :
            random_pic = randint(0, pic_count - 1)
            picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
            pic_id = str(picture[random_pic]['id'])
            pic_show = picbot.post_show(pic_id)
            pic_url = "https://danbooru.donmai.us" + str(pic_show['file_url'])
            pic_source = str(pic_show['pixiv_id'])
            if pic_source == "None":
                pic_source = "<" + str(pic_show['source']) + ">"
            else:
                pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) + ">"
            dl = requests.get(pic_url)
            with open(path + str(picture[random_pic]['id'])+".jpg", "wb") as f:
                f.write(dl.content)
            picpath = "./"+str(picture[random_pic]['id'])+".jpg"
            m_content = "{}\nSource : {}".format(m_author.mention,pic_source)

            await client.send_file(ctx.message.channel, picpath, content=m_content)
            await asyncio.sleep(5)
            os.remove(path + str(picture[random_pic]['id'])+".jpg")
    except :
        await client.say("An error occured while trying to get the picture.")

@client.command(description="Get a picture of one of your husbando", pass_context=True)
async def husbando(ctx):
    m_channel = ctx.message.channel
    m_author = ctx.message.author
    m_author_id = m_author.id
    await client.send_typing(m_channel)
    with open('data.json') as json_file:
        datas = json.load(json_file)
    tag = choice(datas[m_author_id]["husbando"])
    tag = tag.replace(" ", "_")
    path = "./"
    max_limit = 200
    picture = picbot.post_list(tags=tag+" rating:safe", limit=max_limit, random=True)
    pic_count = len(picture)
    try :
        if pic_count == 0:
            await client.say("There is no picture with this tag")
        elif m_author_id not in datas :
            await client.say("You aren't registered. Please use **$register**.")
        elif tag is "" :
            await client.say("You have no husbando. Please register one with $register husbando")

        else :
            random_pic = randint(0, pic_count - 1)
            picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
            pic_id = str(picture[random_pic]['id'])
            pic_show = picbot.post_show(pic_id)
            pic_url = "https://danbooru.donmai.us" + str(pic_show['file_url'])
            pic_source = str(pic_show['pixiv_id'])
            if pic_source == "None":
                pic_source = "<" + str(pic_show['source']) + ">"
            else:
                pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) + ">"
            dl = requests.get(pic_url)
            with open(path + str(picture[random_pic]['id'])+".jpg", "wb") as f:
                f.write(dl.content)
            picpath = "./"+str(picture[random_pic]['id'])+".jpg"
            m_content = "{}\nSource : {}".format(m_author.mention,pic_source)

            await client.send_file(ctx.message.channel, picpath, content=m_content)
            await asyncio.sleep(5)
            os.remove(path + str(picture[random_pic]['id'])+".jpg")
    except :
        await client.say("An error occured while trying to get the picture.")

@client.command(description="Get a lewd picture of one of your waifu", pass_context=True, aliases=["lw"])
async def lewdwaifu(ctx):
    m_channel = ctx.message.channel
    m_author = ctx.message.author
    m_author_id = m_author.id
    await client.send_typing(m_channel)
    with open('data.json') as json_file:
        datas = json.load(json_file)
    tag = choice(datas[m_author_id]["waifu"])
    tag = tag.replace(" ", "_")
    path = "./"
    max_limit = 200
    picture = picbot.post_list(tags=tag+" rating:explicit", limit=max_limit, random=True)
    pic_count = len(picture)
    try :
        if pic_count == 0:
            await client.say("There is no picture with this tag")

        elif m_author_id not in datas :
            await client.say("You aren't registered. Please use **$register**.")

        elif tag is "" :
            await client.say("You have no waifu. Please register one with $add waifu")

        elif "nsfw" not in ctx.message.channel.name :
            await client.say("Sorry you can't do that here.")

        else :
            blacklistcheck = False
            while blacklistcheck is False :
                tagblacklist = False
                random_pic = randint(0, pic_count - 1)
                picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
                pic_id = str(picture[random_pic]['id'])
                pic_show = picbot.post_show(pic_id)
                pic_url = "https://danbooru.donmai.us" + str(pic_show['file_url'])
                pic_source = str(pic_show['pixiv_id'])
                pic_tags = str(pic_show['tag_string_general'])

                for i in tag_blacklist:
                    if i in pic_tags :
                        print("Blacklisted tag detected")
                        tagblacklist = True

                if tagblacklist is False :
                    blacklistcheck = True

            if pic_source == "None":
                pic_source = "<" + str(pic_show['source']) + ">"
            else:
                pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) + ">"
            dl = requests.get(pic_url)
            with open(path + str(picture[random_pic]['id'])+".jpg", "wb") as f:
                f.write(dl.content)
            picpath = "./"+str(picture[random_pic]['id'])+".jpg"
            m_content = "{}\nSource : {}".format(m_author.mention,pic_source)

            await client.send_file(ctx.message.channel, picpath, content=m_content)
            await asyncio.sleep(5)
            os.remove(path + str(picture[random_pic]['id'])+".jpg")
    except :
        await client.say("An error occured while trying to get the picture.")

@client.command(description="Get a lewd picture of one of your husbando", pass_context=True)
async def lewdhusbando(ctx):
    m_channel = ctx.message.channel
    m_author = ctx.message.author
    m_author_id = m_author.id
    await client.send_typing(m_channel)
    with open('data.json') as json_file:
        datas = json.load(json_file)
    tag = choice(datas[m_author_id]["husbando"])
    tag = tag.replace(" ", "_")
    path = "./"
    max_limit = 200
    picture = picbot.post_list(tags=tag+" rating:explicit", limit=max_limit, random=True)
    pic_count = len(picture)
    try :
        if pic_count == 0:
            await client.say("There is no picture with this tag")
        elif m_author_id not in datas :
            await client.say("You aren't registered. Please use **$register**.")
        elif tag is "" :
            await client.say("You have no husbando. Please register one with $add husbando")

        elif "nsfw" not in ctx.message.channel.name :
            await client.say("Sorry you can't do that here.")

        else :
            blacklistcheck = False
            while blacklistcheck is False :
                tagblacklist = False
                random_pic = randint(0, pic_count - 1)
                picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
                pic_id = str(picture[random_pic]['id'])
                pic_show = picbot.post_show(pic_id)
                pic_url = "https://danbooru.donmai.us" + str(pic_show['file_url'])
                pic_source = str(pic_show['pixiv_id'])
                pic_tags = str(pic_show['tag_string_general'])

                for i in tag_blacklist:
                    if i in pic_tags :
                        print("Blacklisted tag detected")
                        tagblacklist = True

                if tagblacklist is False :
                    blacklistcheck = True

            if pic_source == "None":
                pic_source = "<" + str(pic_show['source']) + ">"
            else:
                pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) + ">"
            dl = requests.get(pic_url)
            with open(path + str(picture[random_pic]['id'])+".jpg", "wb") as f:
                f.write(dl.content)
            picpath = "./"+str(picture[random_pic]['id'])+".jpg"
            m_content = "{}\nSource : {}".format(m_author.mention,pic_source)

            await client.send_file(ctx.message.channel, picpath, content=m_content)
            await asyncio.sleep(5)
            os.remove(path + str(picture[random_pic]['id'])+".jpg")
    except :
        await client.say("An error occured while trying to get the picture.")



client.run(discord_api)