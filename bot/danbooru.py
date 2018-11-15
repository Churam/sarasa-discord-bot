import discord
from discord.ext import commands
import json
from pybooru import Danbooru, PybooruHTTPError
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
'''
Pretty straightforward, creates a simplle embed out of the parameters you feed it.

title : Title of the embed
pic_url : The url of the previewed picture (Needs to be a direct URL)
description : Description of the embed
url : If you want your title to be clickable and redirect to some web adress
author : Appears above the Title field
footer : Text to write at the very bottom of the embed
color : Color to display along with the embed (In Hexadecimal)
'''
def embedpic(title, pic_url, description=None, url=None, author=None, footer=None, color=0x8c4e68):
	em_color = discord.Colour(color)
	em = discord.Embed(title=title, description=description , url=url, colour=em_color)
	em.set_image(url=pic_url)
	if author is not None :
		em.set_author(name=author)
	if footer is not None :
		em.set_footer(text=footer)
	return em

def blacklistcheck(tags):
	for i in tag_blacklist :
		if i in tags :
			return True
	return False

#Simplify the picture search
'''
This function is the "main" function of this module, it handles most of the picture searching needs.
I'll roughly explain what each parameters do.

tag : The tag to search. It's required for the function to work. Note that it doesn't need to be formatted for Danbooru's needs, it's handled in the "#Tag formatting" part.
nsfw : If we want to include NSFW pictures in the results
nsfw_only : If we ONLY want NSFW pictures in the results
suffix : If you're looking for pictures of a same serie and want to get rid of the serie suffix in the characters' names
blacklist : If you want to check the result post's tags through blacklistcheck() to check for any unwanted tags
isRandom : If we want the 100 posts to be random instead of in chronological order
embed : If we want the post to return an embed instead of a dict (Mainly used with embedpic() for less code clutter)
embed_color : Specify a color for the embed (In Hexadecimal)
'''
async def picturesearch(tag, nsfw = False, nsfw_only = False, suffix = None, blacklist = True, isRandom = False, embed = False, embed_color = 0x777fc6):
	max_limit = 100
	rating = "safe"

	#Tag formatting
	if tag is None :
		tag = "order:rank"
	while tag.endswith(" ") :
		tag = tag[:-1]
	if " " in tag :
		tag = tag.replace(" ", "_")

	tag_search = tag + " rating:{}".format(rating)

	if nsfw_only is True :
		rating = random.choice(["questionable","explicit"])
		tag_search = tag + " rating:{}".format(rating)
	elif nsfw is True:
		tag_search = tag

	posts = picbot.post_list(
		tags = tag_search, 
		limit = max_limit, 
		random = isRandom)
	pic_count = len(posts)
	if pic_count == 0 :
		return -1
	random_pic = randint(0, pic_count - 1)
	
	pic_id = str(posts[random_pic]['id'])
	pic_show = picbot.post_show(pic_id)
	pic_tags = pic_show["tag_string_general"].split(' ')

	if blacklist is True and blacklistcheck(pic_tags):
		for i in range(0,6):
			if i == 5 :
				return None;
			random_pic = randint(0, pic_count - 1)
			pic_show = picbot.post_show(pic_id)
			pic_tags = pic_show["tag_string_general"].split(' ')
			if not blacklistcheck(pic_tags) :
				break

	if pic_show['file_url'].startswith("http://") or pic_show['file_url'].startswith("https://") :
		pic_url = pic_show['file_url']
	else :
		pic_url = "https://danbooru.donmai.us{}".format(pic_show['file_url'])

	post_link = "https://danbooru.donmai.us/posts/" + str(posts[random_pic]['id'])
	pic_source = str(pic_show['pixiv_id'])
	pic_chara = str(pic_show['tag_string_character'].title().replace(" "," and ").replace("_"," "))
	pic_author = pic_show['tag_string_artist'].replace("_", " ")

	if pic_source == "None" or pic_source == None:
		pic_source = str(pic_show['source'])
	elif pic_show['source']== "None" or pic_show['source'] == None:
		pic_source = "No source"
	else:
		pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(pic_show['pixiv_id']) + ">"

	if " {}".format(suffix) in pic_chara and suffix != None:
		pic_chara = pic_chara.replace(" {}".format(suffix),"")

	if pic_chara.endswith(" "):
		pic_chara = pic_chara[:-1]

	if tag == "order:rank":
		title = "Recent popular picture"
	else :
		title = tag.replace("_", " ")

	if embed is True :
		em = embedpic(
			title = title,
			pic_url = pic_url,
			description = pic_source,
			url=post_link,
			footer=pic_author,
			color=embed_color
			)
		return em
	else :
		pic_result = {"pic_chara" : pic_chara, "pic_source" : pic_source, "picture_link" : post_link, "pic_url" : pic_url, "pic_author" : pic_author}
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
		await self.client.say(
			embed = await picturesearch(tag = message, embed = True, embed_color = 0x75ff89)
			)

	@commands.command(description="Retrieve a random NSFW pic of the given tag on Danbooru",pass_context=True)
	async def hentai(self, ctx, *, message = None):
		m_channel = ctx.message.channel
		channelname = m_channel.name
		m_server = ctx.message.server
		m_author = ctx.message.author
		await self.client.send_typing(m_channel)
		if "nsfw" not in channelname:
			await self.client.say("Sorry, you can't do that here")
		else :
			em = await picturesearch(tag = message, nsfw_only = True, embed = True, embed_color = 0xff6ddf)
			if em is None :
				await self.client.say("No suitable pictures found.")
			else :
				await self.client.say(embed=em)

#Series picture search
	@commands.command(description="Recruit a Granblue Fantasy character from Safebooru !",pass_context=True)
	async def gbf(self, ctx):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		await self.client.send_typing(m_channel)
		await self.client.say(
			embed = await picturesearch(tag = "Granblue_Fantasy", suffix = "(Granblue Fantasy)", embed = True)
			)

	@commands.command(description="Construct a Kanmusu from the great land of Safebooru !",pass_context=True)
	async def kanmusu(self, ctx):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		await self.client.send_typing(m_channel)
		await self.client.say(
			embed = await picturesearch(tag = "Kantai_Collection", suffix = "(Kantai Collection)", embed = True) 
			)


	@commands.command(description="Construct a T-Doll from the wastelands of Girls' Frontline !",pass_context=True)
	async def tdoll(self, ctx):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		await self.client.send_typing(m_channel) 
		await self.client.say(
			embed = await picturesearch(tag = "Girls_Frontline", suffix = "(Girls Frontline)", embed = True)
			)

	@commands.command(description="Will your girl be SHINY ?",pass_context=True)
	async def lovelive(self, ctx):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		await self.client.send_typing(m_channel)
		await self.client.say(
			embed = await picturesearch(tag = "Love_Live!", suffix = "(Love Live!)", embed = True)
			)

	@commands.command(description="Will your girl be SHINY ?",pass_context=True)
	async def muse(self, ctx):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		await self.client.send_typing(m_channel)    
		await self.client.say(
			embed = await picturesearch(tag = "Love_live!_school_idol_project", suffix = "(Love Live!)", embed = True)
			)

	@commands.command(description="Will your girl be SHINY ?",pass_context=True)
	async def aqours(self, ctx):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		await self.client.send_typing(m_channel)  
		await self.client.say(
			embed = await picturesearch(tag = "Love_Live!_Sunshine!!", suffix = "(Love Live!)", embed = True)
			)

	@commands.command(description="Summon a servant from Safebooru !",pass_context=True)
	async def fate(self, ctx):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		await self.client.send_typing(m_channel)
		await self.client.say(
			embed = await picturesearch(tag = "Fate/Grand_Order", suffix = "(Fate/Grand Order)", embed = True)
			)

	@commands.command(description="Construct an Azure Lane shipgirl !",pass_context=True)
	async def al(self, ctx):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		await self.client.send_typing(m_channel) 
		await self.client.say(
			embed = await picturesearch(tag = "Azur_Lane", suffix = "(Azur Lane)", embed = True)
			)

	@commands.command(description="Scout an Idol from Safebooru !",pass_context=True)
	async def imas(self, ctx):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		await self.client.send_typing(m_channel)
		await self.client.say(
			embed = await picturesearch(tag = "Idolmaster", suffix = "(Idolmaster)", embed = True)
			)

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
		while waifuname.endswith(" "):
			waifuname = waifuname[:-1]
		waifuname_format = waifuname.lower().title().replace("_", " ")
		with open('./users/{}/userdata.json'.format(m_author_id)) as json_file:
			datas = json.load(json_file)

		if waifuname_format in datas["waifu"] :
				await self.client.say("This character is already in your Waifu list.")
		elif "*" in waifuname :
			await self.client.say("Please avoid using wildcards (*).")
		else :
			em = await picturesearch(tag = waifuname, embed = True, embed_color = 0xff6868)
			if em == -1 :
				await self.client.say("There is no waifu with this tag.")
			else :
				em.description = "Successfully added {} in your Waifu list".format(waifuname_format)
				em.set_author(name=m_author.name)
				await self.client.say(embed=em)
				with open('./users/{}/userdata.json'.format(m_author_id), mode='w', encoding='utf-8') as json_file:
					datas["waifu"].append(waifuname_format)
					json.dump(datas, json_file, indent=2)

	@add.command(pass_context=True, name="husbando")
	async def _husbando(self, ctx, *, husbandoname : str):
		m_author = ctx.message.author
		m_author_id = ctx.message.author.id
		adduser(m_author_id)
		while husbandoname.endswith(" "):
			husbandoname = husbandoname[:-1]
		husbandoname_format = husbandoname.lower().title().replace("_", " ")
		with open('./users/{}/userdata.json'.format(m_author_id)) as json_file:
			datas = json.load(json_file)

		if husbandoname_format in datas["husbando"] :
				await self.client.say("This character is already in your husbando list.")
		elif "*" in husbandoname :
			await self.client.say("Please avoid using wildcards (*).")
		else :
			em = await picturesearch(tag = husbandoname, embed = True, embed_color = 0x777fc6)
			if em == -1 :
				await self.client.say("There is no husbando with this tag.")
			else :
				em.description = "Successfully added {} in your husbando list".format(husbandoname_format)
				em.set_author(name=m_author.name)
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
		if nb > 5 :
			await self.client.say("You can only request up to 5 pictures at once.")
		else :
			for i in range(nb) :
				tag = choice(datas["waifu"])
				if tag is "" :
					await self.client.say("You have no waifu. Please register one with $add waifu")

				em = await picturesearch(tag = tag, embed = True, embed_color = 0xff6868)
				em.set_author(name = m_author.name)
				if em == -1:
					await self.client.say("There is no picture with this tag, the tag `{}` might have changed.".format(tag))
				elif em is None :
					await self.client.say("No suitable picture found")
				else :
					await self.client.say(embed=em)

	@commands.command(description="Get a picture of one of your husbando", pass_context=True, aliases=["h"])
	async def husbando(self, ctx, nb=1):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		m_author_id = m_author.id
		await self.client.send_typing(m_channel)
		with open('./users/{}/userdata.json'.format(m_author_id)) as json_file:
			datas = json.load(json_file)
		if nb > 5 :
			await self.client.say("You can only request up to 5 pictures at once.")
		else :
			for i in range(nb) :
				tag = choice(datas["husbando"])
				if tag is "" :
					await self.client.say("You have no husbando. Please register one with $add husbando")

				em = await picturesearch(tag = tag, embed = True, embed_color = 0xab61d3)
				em.set_author(name = m_author.name)
				if em == -1:
					await self.client.say("There is no picture with this tag, the tag `{}` might have changed.".format(tag))
				elif em is None :
					await self.client.say("No suitable picture found")
				else :
					await self.client.say(embed=em)

	@commands.command(description="Get a lewd picture of one of your waifu", pass_context=True, aliases=["lw"])
	async def lewdwaifu(self, ctx, nb=1):
		m_channel = ctx.message.channel
		m_author = ctx.message.author
		m_author_id = m_author.id
		await self.client.send_typing(m_channel)
		with open('./users/{}/userdata.json'.format(m_author_id)) as json_file:
			datas = json.load(json_file)
		if nb > 5 :
			await self.client.say("You can only request up to 5 pictures at once.")
		else :
			for i in range(nb) :
				tag = choice(datas["waifu"])
				if tag is "" :
					await self.client.say("You have no waifu. Please register one with $add waifu")

				em = await picturesearch(tag = tag, nsfw_only = True, embed = True, embed_color = 0xff6868)
				em.set_author(name = m_author.name)
				if em == -1:
					await self.client.say("There is no picture with this tag, the tag `{}` might have changed.".format(tag))
				elif em is None :
					await self.client.say("No suitable picture found")
				else :
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
		with open('./users/{}/userdata.json'.format(m_author_id)) as json_file:
			datas = json.load(json_file)
		if nb > 5 :
			await self.client.say("You can only request up to 5 pictures at once.")
		else :
			for i in range(nb) :
				tag = choice(datas["husbando"])
				if tag is "" :
					await self.client.say("You have no husbando. Please register one with $add husbando")

				em = await picturesearch(tag = tag, nsfw_only = True, embed = True, embed_color = 0xab61d3)
				em.set_author(name = m_author.name)
				if em == -1:
					await self.client.say("There is no picture with this tag, the tag `{}` might have changed.".format(tag))
				elif em is None :
					await self.client.say("No suitable picture found")
				else :
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