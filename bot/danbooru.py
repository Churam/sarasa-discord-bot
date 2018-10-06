import discord
from discord.ext import commands
import json
from pybooru import Danbooru
from random import randint, randrange, choice
import random
import os

#Load Danbooru API key
with open('api.json') as api_file:    
	api_key = json.load(api_file)

#Load the API Key and the Danbooru module
danbooru_api = api_key["API"][1]["danbooru"]
picbot = Danbooru('danbooru', username='Akeyro', api_key=danbooru_api)

#Danbooru tags to blacklist for the NSFW picture search commands
tag_blacklist = ["lolicon", "scat", "guro", "vore", "rape", "spoiler", "peeing", "pee", "bestiality", "shota", "loli", 'shotacon', "furry"] 


def usrdata(userid):
	return "./users/{}/userdata.json".format(userid)


#Add user to the users folder
def adduser(userid):
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
			usrdata["waifu"] = []
			usrdata["husbando"] = []
			usrdata["spark"] = {"crystals" : 0, "tickets" : 0, "10tickets" : 0}
			json.dump(usrdata, x, indent=2, ensure_ascii=False)


#Simplify the creation of Embeds
def embedpic(title, pic_url, description=None, url=None, author=None, footer=None, color=0x8c4e68):
	em_color = discord.Colour(color)
	em = discord.Embed(title=title, description=description , url=url, colour=em_color)
	em.set_image(url=pic_url)
	em.set_author(name=author)
	if footer is None:
		pass
	else:
		em.set_footer(text=footer)
	return em

#Simplify the picture search
def picturesearch(tag, suffix):
	tag = str(tag)
	suffix = str(suffix)
	max_limit = 200
	picture = picbot.post_list(tags=tag +" rating:safe", limit=max_limit, random=True)
	pic_count = len(picture)
	
	while True:
		try:
			random_pic = randint(0, pic_count - 1)
			picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
			pic_id = str(picture[random_pic]['id'])
			pic_show = picbot.post_show(pic_id)

			if pic_show['file_url'].startswith("http://") or pic_show['file_url'].startswith("https://") :
				pic_url = pic_show['file_url']
			else :
				pic_url = "https://danbooru.donmai.us{}".format(pic_show['file_url'])

			pic_source = str(pic_show['pixiv_id'])
			pic_chara = str(pic_show['tag_string_character'])
			pic_author = pic_show['tag_string_artist']
		except:
			continue
		break
	if pic_source == "None" or pic_source == None:
		pic_source = str(pic_show['source'])
	elif pic_show['source']== "None" or pic_show['source'] == None:
		pic_source = "No source"
	else:
		pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) + ">"
	pic_chara = pic_chara.title()
	pic_chara = pic_chara.replace(" "," and ")
	pic_chara = pic_chara.replace("_"," ")
	if " {}".format(suffix) in pic_chara:
		pic_chara = pic_chara.replace(" {}".format(suffix),"")
	if pic_chara.endswith(" "):
		pic_chara = pic_chara[:-1]

	pic_result = {"pic_chara" : pic_chara, "pic_source" : pic_source, "picture_link" : picture_link, "pic_url" : pic_url, "pic_author" : pic_author}
	return pic_result


#Commands

class Danbooru():
	def __init__(self, bot):
		self.client = bot

	@commands.command(description="Retrieve a random safe pic of the given tag on Danbooru",pass_context=True)
	async def safe(self, ctx, *, message=None):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		await self.client.send_typing(m_channel)
		path = "./"
		max_limit = 200

		if message is None :
			picture = picbot.post_list(tags="order:rank"+" rating:safe", limit=max_limit)
		else :
			message = str(message)
			message = message.replace(" ","_")
			if message.endswith(" "):
				message = message[:-1]
			picture = picbot.post_list(tags=message+" rating:safe", limit=max_limit, random=True)

		pic_count = len(picture)
		if pic_count == 0:
			await self.client.say("There is no picture with this tag")

		else :
			while True:
				try:
					random_pic = randint(0, pic_count - 1)
					picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
					pic_id = str(picture[random_pic]['id'])
					pic_show = picbot.post_show(pic_id)
					if pic_show['file_url'].startswith("http://") or pic_show['file_url'].startswith("https://") :
						pic_url = pic_show['file_url']
					else :
						pic_url = "https://danbooru.donmai.us{}".format(pic_show['file_url'])
					pic_source = str(pic_show['pixiv_id'])
					pic_author = pic_show['tag_string_artist']
				except:
					continue
				break
			if pic_source == "None":
				pic_source = "<" + str(pic_show['source']) + ">"
			else:
				pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) + ">"
			em_color = discord.Colour(0x63f94f)
			if message is None :
					em = discord.Embed(title="Random popular picture", description=pic_source , url=picture_link, colour=em_color)
			else :
				em = discord.Embed(title=message.replace("_"," "), description=pic_source , url=picture_link, colour=em_color)
			em.set_image(url=pic_url)
			em.set_author(name=m_author.name)
			em.set_footer(text=pic_author.replace("_", " "))
			await self.client.say(embed=em)

	@commands.command(description="Retrieve a random NSFW pic of the given tag on Danbooru",pass_context=True)
	async def hentai(self, ctx, *, message=None):
		m_channel = ctx.message.channel
		channelname = m_channel.name
		m_server = ctx.message.server
		m_author = ctx.message.author
		blacklistcheck = False
		path = "./"

		if "nsfw" not in channelname:
			await self.client.say("Sorry, you can't do that here")

		else:
			max_limit = 200
			blacklist = False
			if message is None :
				picture = picbot.post_list(tags="order:rank"+" rating:explicit", limit=max_limit)
				pic_count = len(picture)

			elif message.lower() in tag_blacklist :
				await self.client.say("This tag is blacklisted.")
				blacklist = True

			else :
				message = str(message)
				message = message.replace(" ","_")
				if message.endswith(" "):
					message = message[:-1]
				picture = picbot.post_list(tags=message+" rating:explicit", limit=max_limit, random=True)
				pic_count = len(picture)


			if blacklist is True :
				pass

			elif pic_count == 0:
				await self.client.say("There is no picture with this tag")

			else :
				
				await self.client.send_typing(m_channel)
				while blacklistcheck is False :
					tagblacklist = False
					counter = 0
					while True and counter < 5:
						try:
							random_pic = randint(0, pic_count - 1)
							picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
							pic_id = str(picture[random_pic]['id'])
							pic_show = picbot.post_show(pic_id)
							pic_author = pic_show['tag_string_artist']
							if pic_show['file_url'].startswith("http://") or pic_show['file_url'].startswith("https://") :
								pic_url = pic_show['file_url']
							else :
								pic_url = "https://danbooru.donmai.us{}".format(pic_show['file_url'])
							pic_source = str(pic_show['pixiv_id'])
							pic_tags = str(pic_show['tag_string_general'])
						except:
							continue
						break

					for i in tag_blacklist:
						if i in pic_tags :
							tagblacklist = True
							counter += 1

					if tagblacklist is False :
						blacklistcheck = True
				

				if counter == 5 :
					await self.client.say("No suitable picture found.")

				else :
					if pic_source == "None":
						pic_source = "<" + str(pic_show['source']) + ">"
					else:
						pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) +">"

					em_color = discord.Colour(0xEb5e88)
					if message is None :
						em = discord.Embed(title="Random popular picture", description=pic_source , url=picture_link, colour=em_color)
					else :
						em = discord.Embed(title=message.replace("_"," "), description=pic_source , url=picture_link, colour=em_color)
					em.set_image(url=pic_url)
					em.set_author(name=m_author.name)
					em.set_footer(text=pic_author.replace("_", " "))
					await self.client.say(embed=em)


#Series picture search
	@commands.command(description="Recruit a Granblue Fantasy character from Safebooru !",pass_context=True)
	async def gbf(self, ctx):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		await self.client.send_typing(m_channel)
		em_color = discord.Colour(0x777fc6)
		pic_result = picturesearch("Granblue_Fantasy", "(Granblue Fantasy)") 
		em = discord.Embed(title=pic_result["pic_chara"], description=pic_result["pic_source"] , url=pic_result["picture_link"], colour=em_color)
		em.set_image(url=pic_result["pic_url"])
		em.set_author(name=m_author.name)
		em.set_footer(text=pic_result["pic_author"].replace("_", " "))
		await self.client.say(embed=em)

	@commands.command(description="Construct a Kanmusu from the great land of Safebooru !",pass_context=True)
	async def kanmusu(self, ctx):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		await self.client.send_typing(m_channel)
		em_color = discord.Colour(0x777fc6)
		pic_result = picturesearch("Kantai_Collection", "(Kantai Collection)") 
		em = discord.Embed(title=pic_result["pic_chara"], description=pic_result["pic_source"] , url=pic_result["picture_link"], colour=em_color)
		em.set_image(url=pic_result["pic_url"])
		em.set_author(name=m_author.name)
		em.set_footer(text=pic_result["pic_author"].replace("_", " "))
		await self.client.say(embed=em)


	@commands.command(description="Construct a T-Doll from the wastelands of Girls' Frontline !",pass_context=True)
	async def tdoll(self, ctx):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		await self.client.send_typing(m_channel)
		em_color = discord.Colour(0x777fc6)
		pic_result = picturesearch("Girls_Frontline", "(Girls Frontline)") 
		em = discord.Embed(title=pic_result["pic_chara"], description=pic_result["pic_source"] , url=pic_result["picture_link"], colour=em_color)
		em.set_image(url=pic_result["pic_url"])
		em.set_author(name=m_author.name)
		em.set_footer(text=pic_result["pic_author"].replace("_", " "))
		await self.client.say(embed=em)

	@commands.command(description="Will your girl be SHINY ?",pass_context=True)
	async def lovelive(self, ctx):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		await self.client.send_typing(m_channel)
		em_color = discord.Colour(0x777fc6)
		pic_result = picturesearch("Love_Live!", "(Love Live!)") 
		em = discord.Embed(title=pic_result["pic_chara"], description=pic_result["pic_source"] , url=pic_result["picture_link"], colour=em_color)
		em.set_image(url=pic_result["pic_url"])
		em.set_author(name=m_author.name)
		em.set_footer(text=pic_result["pic_author"].replace("_", " "))
		await self.client.say(embed=em)

	@commands.command(description="Will your girl be SHINY ?",pass_context=True)
	async def muse(self, ctx):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		await self.client.send_typing(m_channel)   
		em_color = discord.Colour(0x777fc6)
		pic_result = picturesearch("Love_live!_school_idol_project", "(Love Live!)") 
		em = discord.Embed(title=pic_result["pic_chara"], description=pic_result["pic_source"] , url=pic_result["picture_link"], colour=em_color)
		em.set_image(url=pic_result["pic_url"])
		em.set_author(name=m_author.name)
		em.set_footer(text=pic_result["pic_author"].replace("_", " "))
		await self.client.say(embed=em)

	@commands.command(description="Will your girl be SHINY ?",pass_context=True)
	async def aqours(self, ctx):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		await self.client.send_typing(m_channel)  
		em_color = discord.Colour(0x777fc6)
		pic_result = picturesearch("Love_Live!_Sunshine!!", "(Love Live!)") 
		em = discord.Embed(title=pic_result["pic_chara"], description=pic_result["pic_source"] , url=pic_result["picture_link"], colour=em_color)
		em.set_image(url=pic_result["pic_url"])
		em.set_author(name=m_author.name)
		em.set_footer(text=pic_result["pic_author"].replace("_", " "))
		await self.client.say(embed=em)

	@commands.command(description="Summon a servant from Safebooru !",pass_context=True)
	async def fate(self, ctx):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		await self.client.send_typing(m_channel)
		em_color = discord.Colour(0x777fc6)
		pic_result = picturesearch("Fate/Grand_Order", "(Fate/Grand Order)") 
		em = discord.Embed(title=pic_result["pic_chara"], description=pic_result["pic_source"] , url=pic_result["picture_link"], colour=em_color)
		em.set_image(url=pic_result["pic_url"])
		em.set_author(name=m_author.name)
		em.set_footer(text=pic_result["pic_author"].replace("_", " "))
		await self.client.say(embed=em)

	@commands.command(description="Construct an Azure Lane shipgirl !",pass_context=True)
	async def al(self, ctx):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		await self.client.send_typing(m_channel)
		em_color = discord.Colour(0x777fc6)
		pic_result = picturesearch("Azur_Lane", "(Azur Lane)") 
		em = discord.Embed(title=pic_result["pic_chara"], description=pic_result["pic_source"] , url=pic_result["picture_link"], colour=em_color)
		em.set_image(url=pic_result["pic_url"])
		em.set_author(name=m_author.name)
		em.set_footer(text=pic_result["pic_author"].replace("_", " "))
		await self.client.say(embed=em)

	@commands.command(description="Scout an Idol from Safebooru !",pass_context=True)
	async def idol(self, ctx):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		await self.client.send_typing(m_channel)
		em_color = discord.Colour(0x777fc6)
		pic_result = picturesearch("Idolmaster", "(Idolmaster)")
		if "Producer" in pic_result["pic_chara"]:
			pic_result["pic_chara"] = pic_result["pic_chara"].replace("Producer","")
		em = discord.Embed(title=pic_result["pic_chara"], description=pic_result["pic_source"] , url=pic_result["picture_link"], colour=em_color)
		em.set_image(url=pic_result["pic_url"])
		em.set_author(name=m_author.name)
		em.set_footer(text=pic_result["pic_author"].replace("_", " "))
		await self.client.say(embed=em)


#Waifu/Husbando commands 
	@commands.group(pass_context=True)
	async def add(self, ctx):
		m_author = ctx.message.author
		m_author_id = str(m_author.id)
		await self.client.send_typing(ctx.message.channel)
		if ctx.invoked_subcommand is None:
			await self.client.say("Available subcommands : `waifu` `husbando`")


	@add.command(pass_context=True, name="waifu")
	async def _waifu(self, ctx, *, waifuname : str):
		m_author = ctx.message.author
		m_author_id = ctx.message.author.id
		adduser(m_author_id)
		path = "./"
		if waifuname.endswith(" "):
			waifuname = waifuname[:-1]
		waifuname_format = waifuname.lower()
		waifuname_format = waifuname_format.title()
		waifuname_format = waifuname_format.replace("_", " ")
		waifuname = waifuname.replace(" ", "_")
		with open('./users/{}/userdata.json'.format(m_author_id)) as json_file:
			datas = json.load(json_file)
		picture = picbot.post_list(tags=waifuname+" rating:safe", limit=200, random=True)
		pic_count = len(picture)
		if pic_count == 0:
			await self.client.say("There is no waifu with this tag.")

		elif waifuname_format in datas["waifu"] :
				await self.client.say("This character is alrleady in your Waifu list.")

		else :
			while True:
				try:
					random_pic = randint(0, pic_count - 1)
					picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
					pic_id = str(picture[random_pic]['id'])
					pic_show = picbot.post_show(pic_id)
					if pic_show['file_url'].startswith("http://") or pic_show['file_url'].startswith("https://") :
						pic_url = pic_show['file_url']
					else :
						pic_url = "https://danbooru.donmai.us{}".format(pic_show['file_url'])
					pic_source = str(pic_show['pixiv_id'])
					pic_author = pic_show['tag_string_artist']
				except:
					continue
				break
			if pic_source == "None":
				pic_source = "<" + str(pic_show['source']) + ">"
			else:
				pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) + ">"
			em_color = discord.Colour(0xff6868)
			em = discord.Embed(title=waifuname_format, description="Successfully added {} in your Waifu list".format(waifuname_format) , url=picture_link, colour=em_color)
			em.set_image(url=pic_url)
			em.set_author(name=m_author.name)
			em.set_footer(text=pic_author.replace("_", " "))
			await self.client.say(embed=em)
			with open('./users/{}/userdata.json'.format(m_author_id), mode='w', encoding='utf-8') as json_file:
				datas["waifu"].append(waifuname_format)
				json.dump(datas, json_file, indent=2)

	@add.command(pass_context=True, name="husbando")
	async def _husbando(self, ctx, *, husbandoname : str):
		m_author = ctx.message.author
		m_author_id = ctx.message.author.id
		adduser(m_author_id)
		path = "./"
		if husbandoname.endswith(" "):
			husbandoname = husbandoname[:-1]
		husbandoname_format = husbandoname.lower()
		husbandoname_format = husbandoname_format.title()
		husbandoname_format = husbandoname_format.replace("_", " ")
		husbandoname = husbandoname.replace(" ", "_")
		with open('./users/{}/userdata.json'.format(m_author_id)) as json_file:
			datas = json.load(json_file)

		if husbandoname_format in datas["husbando"] :
			await self.client.say("This character is already in your Husbando list.")

		else :
			picture = picbot.post_list(tags=husbandoname+" rating:safe", limit=200, random=True)
			pic_count = len(picture)
			if pic_count == 0:
				await self.client.say("There is no husbando with this tag.")

			else :
				while True:
					try:
						random_pic = randint(0, pic_count - 1)
						picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
						pic_id = str(picture[random_pic]['id'])
						pic_show = picbot.post_show(pic_id)
						if pic_show['file_url'].startswith("http://") or pic_show['file_url'].startswith("https://") :
							pic_url = pic_show['file_url']
						else :
							pic_url = "https://danbooru.donmai.us{}".format(pic_show['file_url'])
						pic_source = str(pic_show['pixiv_id'])
						pic_author = pic_show['tag_string_artist']
					except:
						continue
					break
				if pic_source == "None":
					pic_source = "<" + str(pic_show['source']) + ">"
				else:
					pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) + ">"
				em_color = discord.Colour(0x777fc6)
				em = discord.Embed(title=husbandoname_format, description="Successfully added {} in your Husbando list".format(husbandoname_format) , url=picture_link, colour=em_color)
				em.set_image(url=pic_url)
				em.set_author(name=m_author.name)
				em.set_footer(text=pic_author.replace("_", " "))
				await self.client.say(embed=em)
				with open('./users/{}/userdata.json'.format(m_author_id), mode='w', encoding='utf-8') as json_file:
					datas["husbando"].append(husbandoname_format)
					json.dump(datas, json_file, indent=2)

	@commands.group(description="Remove a waifu or husbando from your list", pass_context=True)
	async def remove(self, ctx):
		if ctx.invoked_subcommand is None:
			await self.client.say("Available subcommands : `waifu` `husbando`")

	@remove.command(name="waifu", pass_context=True)
	async def remwaifu(self, ctx,* , waifuname : str):
		m_author = ctx.message.author
		m_author_id = m_author.id
		with open('./users/{}/userdata.json'.format(m_author_id)) as json_file:
			datas = json.load(json_file)
		waifuname_format = waifuname.lower()
		waifuname_format = waifuname_format.title()
		waifuname_format = waifuname_format.replace("_", " ")
		if waifuname_format not in datas["waifu"]:
			await self.client.say("This waifu isn't in your list.")

		else :
			with open('./users/{}/userdata.json'.format(m_author_id), mode='w', encoding='utf-8') as json_file:
				datas["waifu"].remove(waifuname_format)
				json.dump(datas, json_file, indent=2)
			await self.client.say("Successfully removed **{}** from your Waifu list.".format(waifuname_format))

	@remove.command(name="husbando", pass_context=True)
	async def remhusbando(self, ctx,* , husbandoname : str):
		m_author = ctx.message.author
		m_author_id = m_author.id
		with open('./users/{}/userdata.json'.format(m_author_id)) as json_file:
			datas = json.load(json_file)
		husbandoname_format = husbandoname.lower()
		husbandoname_format = husbandoname_format.title()
		husbandoname_format = husbandoname_format.replace("_", " ")
		if husbandoname_format not in datas["husbando"]:
			await self.client.say("This husbando isn't in your list.")

		else :
			with open('./users/{}/userdata.json'.format(m_author_id), mode='w', encoding='utf-8') as json_file:
				datas["husbando"].remove(husbandoname_format)
				json.dump(datas, json_file, indent=2)
			await self.client.say("Successfully removed **{}** from your Husbando list.".format(husbandoname_format))

	@commands.command(description="Get a picture of one your waifu", pass_context=True, aliases=["w"])
	async def waifu(self, ctx, nb=1):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		m_author_id = m_author.id
		await self.client.send_typing(m_channel)
		with open('./users/{}/userdata.json'.format(m_author_id)) as json_file:
			datas = json.load(json_file)
		path = "./"
		max_limit = 200
		if nb > 5 :
			await self.client.say("You can only request up to 5 pictures at once.")
		else :
			for i in range(nb) :
				tag = choice(datas["waifu"])
				picture = picbot.post_list(tags=tag.replace(" ", "_")+" rating:safe", limit=max_limit)
				pic_count = len(picture)
				print(picture)
				if pic_count == 0:
					await self.client.say("There is no picture with this tag, the tag `{}` might have changed.".format(tag))

				elif tag is "" :
					await self.client.say("You have no waifu. Please register one with $add waifu")

				else :
					while True :
						try :
							random_pic = randint(0, pic_count - 1)
							picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
							pic_id = str(picture[random_pic]['id'])
							pic_show = picbot.post_show(pic_id)
							if pic_show['file_url'].startswith("http://") or pic_show['file_url'].startswith("https://") :
								pic_url = pic_show['file_url']
							else :
								pic_url = "https://danbooru.donmai.us{}".format(pic_show['file_url'])
							pic_source = str(pic_show['pixiv_id'])
							pic_author = pic_show["tag_string_artist"]
						except :
							continue
						break

					if pic_source == "None":
						pic_source = "<" + str(pic_show['source']) + ">"
					else:
						pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) + ">"
					try :
						await self.client.say(embed=embedpic(title=tag, description=pic_source, url=picture_link, pic_url=pic_url, author=m_author.name, footer=pic_author.replace("_", " "), color=0xff6868))
					except Exception as e:
						print(e)
						print("Couldn't send picture : tag : {}\npic_source : {}\npic_link : {}\npic_url : {}\nmsg_author : {}\npic_author : {}".format(tag,pic_source,picture_link,pic_url,m_author.name,pic_author))

	@commands.command(description="Get a picture of one of your husbando", pass_context=True, aliases=["h"])
	async def husbando(self, ctx, nb=1):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		m_author_id = m_author.id
		await self.client.send_typing(m_channel)
		with open('./users/{}/userdata.json'.format(m_author_id)) as json_file:
			datas = json.load(json_file)
		path = "./"
		max_limit = 200
		if nb > 5 :
			await self.client.say("You can only request up to 5 pictures at once.")
		else :
			for i in range(nb):
				tag = choice(datas["husbando"])
				picture = picbot.post_list(tags=tag.replace(" ", "_")+" rating:safe", limit=max_limit, random=True)
				pic_count = len(picture)

				if pic_count == 0:
					await self.client.say("There is no picture with this tag, the tag `{}` might have changed.".format(tag))

				elif tag is "" :
					await self.client.say("You have no husbando. Please register one with $add husbando")

				else :
					while True :
						try :
							random_pic = randint(0, pic_count - 1)
							picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
							pic_id = str(picture[random_pic]['id'])
							pic_show = picbot.post_show(pic_id)
							if pic_show['file_url'].startswith("http://") or pic_show['file_url'].startswith("https://") :
								pic_url = pic_show['file_url']
							else :
								pic_url = "https://danbooru.donmai.us{}".format(pic_show['file_url'])
							pic_source = str(pic_show['pixiv_id'])
							pic_author = pic_show['tag_string_artist']
						except :
							continue
						break
					if pic_source == "None":
						pic_source = "<" + str(pic_show['source']) + ">"
					else:
						pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) + ">"

					em_color = discord.Colour(0x777fc6)
					em = discord.Embed(title=tag, description=pic_source , url=picture_link, colour=em_color)
					em.set_image(url=pic_url)
					em.set_author(name=m_author.name)
					em.set_footer(text=pic_author.replace("_", " "))
					try :
						await self.client.say(embed=embedpic(title=tag, description=pic_source, url=picture_link, pic_url=pic_url, author=m_author.name, footer=pic_author.replace("_", " "), color=0x777fc6))
					except Exception as e:
						print(e)
						print("Couldn't send picture : tag : {}\npic_source : {}\npic_link : {}\npic_url : {}\nmsg_author : {}\npic_author : {}".format(tag,pic_source,picture_link,pic_url,m_author.name,pic_author))



	@commands.command(description="Get a lewd picture of one of your waifu", pass_context=True, aliases=["lw"])
	async def lewdwaifu(self, ctx, nb=1):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		m_author_id = m_author.id
		await self.client.send_typing(m_channel)
		rating = choice(["e","q"])
		with open('./users/{}/userdata.json'.format(m_author_id)) as json_file:
			datas = json.load(json_file)
		path = "./"
		max_limit = 200
		if nb > 5 :
			await self.client.say("You can only request up to 5 pictures at once.")
		else :
			for i in range(nb):
				tag = choice(datas["waifu"])
				picture = picbot.post_list(tags=tag.replace(" ", "_") + " rating:{}".format(rating), limit=max_limit)
				pic_count = len(picture)
				print(picture)
				if pic_count == 0:
					await self.client.say("There is no picture with this tag, the tag `{}` might have changed.".format(tag))

				elif tag is "" :
					await self.client.say("You have no waifu. Please register one with $add waifu")

				elif "nsfw" not in ctx.message.channel.name :
					await self.client.say("Sorry you can't do that here.")

				else :
					blacklistcheck = False
					counter = 0
					while blacklistcheck is False and counter < 5:
						tagblacklist = False
						while True :
							try :
								random_pic = randint(0, pic_count - 1)
								picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
								pic_id = str(picture[random_pic]['id'])
								pic_show = picbot.post_show(pic_id)
								if pic_show['file_url'].startswith("http://") or pic_show['file_url'].startswith("https://") :
									pic_url = pic_show['file_url']
								else :
									pic_url = "https://danbooru.donmai.us{}".format(pic_show['file_url'])
								pic_source = str(pic_show['pixiv_id'])
								pic_tags = str(pic_show['tag_string_general'])
								pic_author = pic_show['tag_string_artist']
							except:
								continue
							break

						for i in tag_blacklist:
							if i in pic_tags :
								print("Blacklisted tag detected : {} for the tag {}".format(i,tag))
								tagblacklist = True
								counter +=1

						if tagblacklist is False :
							blacklistcheck = True

					if counter == 5 :
						await self.client.say("No suitable picture found.")

					else :

						if pic_source == "None":
							pic_source = "<" + str(pic_show['source']) + ">"
						else:
							pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) + ">"

						em_color = discord.Colour(0x8c4e68)
						em = discord.Embed(title=tag, description=pic_source , url=picture_link, colour=em_color)
						em.set_image(url=pic_url)
						em.set_author(name=m_author.name)
						em.set_footer(text=pic_author.replace("_", " "))
						try :
							await self.client.say(embed=em)
						except Exception as e:
							print(e)
							print("Couldn't send picture : tag : {}\npic_source : {}\npic_link : {}\npic_url : {}\nmsg_author : {}\npic_author : {}".format(tag,pic_source,picture_link,pic_url,m_author.name,pic_author))


	@commands.command(description="Get a lewd picture of one of your husbando", pass_context=True, aliases=["lh"])
	async def lewdhusbando(self, ctx, nb=1):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		m_author_id = m_author.id
		await self.client.send_typing(m_channel)
		rating = choice(["explicit","questionable"])
		with open('./users/{}/userdata.json'.format(m_author_id)) as json_file:
			datas = json.load(json_file)

		path = "./"
		max_limit = 200
		if nb > 5 :
			await self.client.say("You can only request up to 5 pictures at once.")
		else :
			for i in range(nb):
				tag = choice(datas["husbando"])
				picture = picbot.post_list(tags=tag.replace(" ", "_")+" rating:{}".format(rating), limit=max_limit, random=True)
				pic_count = len(picture)

				if pic_count == 0:
					await self.client.say("There is no picture with this tag, the tag `{}` might have changed.".format(tag))
				elif tag is "" :
					await self.client.say("You have no husbando. Please register one with $add husbando")

				elif "nsfw" not in ctx.message.channel.name :
					await self.client.say("Sorry you can't do that here.")

				else :
					blacklistcheck = False
					counter = 0
					while blacklistcheck is False and counter < 5:
						tagblacklist = False
						while True :
							try:
								random_pic = randint(0, pic_count - 1)
								picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
								pic_id = str(picture[random_pic]['id'])
								pic_show = picbot.post_show(pic_id)
								if pic_show['file_url'].startswith("http://") or pic_show['file_url'].startswith("https://") :
									pic_url = pic_show['file_url']
								else :
									pic_url = "https://danbooru.donmai.us{}".format(pic_show['file_url'])
								pic_source = str(pic_show['pixiv_id'])
								pic_tags = str(pic_show['tag_string_general'])
								pic_author = pic_show['tag_string_artist']
							except:
								continue
							break

						for i in tag_blacklist:
							if i in pic_tags :
								print("Blacklisted tag detected : {} for the tag {}".format(i,tag))
								tagblacklist = True
								counter += 1

						if tagblacklist is False :
							blacklistcheck = True


					if counter == 5 :
						await self.client.say("No suitable picture found.")

					else :

						if pic_source == "None":
							pic_source = "<" + str(pic_show['source']) + ">"
						else:
							pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) + ">"

						em_color = discord.Colour(0x8c4e68)
						em = discord.Embed(title=tag, description=pic_source , url=picture_link, colour=em_color)
						em.set_image(url=pic_url)
						em.set_author(name=m_author.name)
						em.set_footer(text=pic_author.replace("_", " "))
						try :
							await self.client.say(embed=em)
						except Exception as e:
							print(e)
							print("Couldn't send picture : tag : {}\npic_source : {}\npic_link : {}\npic_url : {}\nmsg_author : {}\npic_author : {}".format(tag,pic_source,picture_link,pic_url,m_author.name,pic_author))


	@commands.command(description="List your waifus", pass_context=True, aliases=["wl"])
	async def waifulist(self, ctx, mention = None):
		if mention is None :
			m_author = ctx.message.author
		else :
			m_author = ctx.message.mentions[0]

		with open(usrdata(m_author.id)) as fp:
			data = json.load(fp)
		waifu_list = data["waifu"]

		text = "__{}'s Waifu list__ :\n```diff\n".format(m_author.mention)
		charcount = len(text)
		trigger = False
		total_char = 0

		for i in waifu_list :
			charcount += len(i)
			total_char += len(i)
			if charcount < 2000 :
				text += "+ {}\n".format(i.replace("_"," "))
				charcount += len(i.replace("_"," "))
			else :
				trigger = True
				text += "\n- For a total of {} Waifu(s)\n```".format(len(waifu_list))
				await self.client.say(text)
				text = "```diff\n"
				charcount = len(text)

		if trigger is False :
			text += "\n- For a total of {} Waifu(s)\n```".format(len(waifu_list))
			await self.client.say(text)

	@commands.command(description="List your husbandos", pass_context=True, aliases=["hl"])
	async def husbandolist(self, ctx, mention = None):
		if mention is None :
			m_author = ctx.message.author
		else :
			m_author = ctx.message.mentions[0]

		with open(usrdata(m_author.id)) as fp:
			data = json.load(fp)
		waifu_list = data["husbando"]
		
		text = "__{}'s Husbando list__ :\n```diff\n".format(m_author.mention)
		charcount = len(text)
		trigger = False
		total_char = 0

		for i in waifu_list :
			charcount += len(i)
			total_char += len(i)
			if charcount < 2000 :
				text += "+ {}\n".format(i.replace("_"," "))
				charcount += len(i.replace("_"," "))
			else :
				trigger = True
				text += "\n- For a total of {} Husbando(s)\n```".format(len(waifu_list))
				await self.client.say(text)
				text = "```diff\n"
				charcount = len(text)

		if trigger is False :
			text += "\n- For a total of {} Husbando(s)\n```".format(len(waifu_list))
			await self.client.say(text)
			

def setup(bot):
	bot.add_cog(Danbooru(bot))