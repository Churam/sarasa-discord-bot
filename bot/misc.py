from __future__ import unicode_literals

import discord
from discord.ext import commands
import asyncio
import json
from random import randrange
import random
from pybooru import Danbooru
import requests
import os
import shutil
import youtube_dl
import datetime
from PIL import ImageFont, Image, ImageDraw
from io import BytesIO
import requests

with open("api.json") as f :
    api = json.load(f)

ocr_key = api[0]["ocr"]

class ytdl_logger(object):
	def debug(self, msg):
		pass

	def warning(self, msg):
		pass

	def error(self, msg):
		print(msg)


def ytdl_hook(d):
	if d['status'] == 'finished':
		text = "Done downloading, now converting ..."
		filename = d['filename']
		return [text, filename]


def replaceMultiple(mainString, toBeReplaces, newString):
	# Iterate over the strings to be replaced
	for elem in toBeReplaces :
		# Check if string is in the main string
		if elem in mainString :
			# Replace the string
			mainString = mainString.replace(elem, newString)
	
	return  mainString


#For OCR translations

def ocr(url, overlay=False, api_key=ocr_key, language='eng'):
	""" OCR.space API request with remote file.
		Python3.5 - not tested on 2.7
	:param url: Image url.
	:param overlay: Is OCR.space overlay required in your response.
					Defaults to False.
	:param api_key: OCR.space API key.
					Defaults to 'helloworld'.
	:param language: Language code to be used in OCR.
					List of available language codes can be found on https://ocr.space/OCRAPI
					Defaults to 'en'.
	:return: Result in JSON format.
	"""

	payload = {'url': url,
			   'isOverlayRequired': overlay,
			   'apikey': api_key,
			   'language': language,
			   }
	r = requests.post('https://api.ocr.space/parse/image',
					  data=payload,
					  )
	return r.content.decode()


#Load Danbooru API key
with open('api.json') as api_file:    
	api_key = json.load(api_file)

#Load the API Key and the Danbooru module
danbooru_api = api_key["API"][1]["danbooru"]
dpic = Danbooru('danbooru', username='Akeyro', api_key=danbooru_api)


#Create embed objetc
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


class Misc():
	def __init__(self, bot):
		self.client = bot


	@commands.command(description="You don't really want to use it. Really. Trust me.")
	async def ome(self, ctx):
		await ctx.send("***BODY ONCE TOLD ME***", file=discord.File("./why/helpme.png"))


	@commands.command(description="Format the picture with the given source.", aliases=["s"])
	async def source(self, ctx, source_url : str, pic_link=None):
		m_author = ctx.message.author

		if pic_link is not None :
			pic_link = str(pic_link)

			if not source_url.startswith("http://") and not source_url.startswith("https://"):
				msg = await ctx.send("The source you provided isn't a valid URL, please make sure it starts with http or https")
				await asyncio.sleep(10)
				await msg.delete()

			elif pic_link.startswith("http://") and not pic_link.startswith("https://"): 
				msg = await ctx.send("The provided direct url to the picture is not valid.")
				await asyncio.sleep(10)
				await msg.delete()

			else :
				#Embed Object
				source_em = embedpic(title=None, pic_url=pic_link)
				source_em.set_author(name="Picture submitted by {}".format(m_author.display_name), icon_url=m_author.avatar_url)
				source_em.add_field(name="Source", value=source_url)

				#Send the Embed Object
				await ctx.send(embed=source_em)

				#Delete the user message
				await ctx.message.delete()

		#If no attachment is found
		elif pic_link is None :
			if "danbooru.donmai.us" in source_url or "safebooru.donmai.us" :

				if "http://" in source_url :
					post_id = source_url.replace("http://", "")

				elif "https://" in source_url :
					post_id = source_url.replace("https://", "")


				#Removes the non-digits characters from the URL to isolate the post ID
				if "danbooru.donmai.us" in source_url :
					post_id = post_id.replace("danbooru.donmai.us/posts/", "") 
					post_id = int(float(post_id))

				elif "safebooru.donmai.us" in source_url :
					post_id = post_id.replace("safebooru.donmai.us/posts/", "") 
					post_id = int(float(post_id))

				#Generate the danbooru post object
				#danbooru post
				dpost = dpic.post_show(post_id)
				pic_link = str(dpost["large_file_url"])
				pic_link = pic_link.replace("//data","/data")
				print(pic_link)
				pic_source = str(dpost['pixiv_id'])

				#Get the source
				if pic_source == "None" or pic_source == None:
					pic_source = str(dpost['source'])
				elif dpost['source']== "None" or dpost['source'] == None:
					pic_source = "No source"
				else:
					pic_source = "<https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(dpost['pixiv_id']) + ">"

				#Embed Object
				source_em = embedpic(title=None, pic_url=pic_link)
				source_em.set_author(name="Picture submitted by {}".format(m_author.display_name), icon_url=m_author.avatar_url)
				source_em.add_field(name="Source", value=pic_source)

				#Send the Embed Object
				await ctx.send(embed=source_em)

				#Delete the user message
				await ctx.message.delete()

			else  :
				msg = await client.say("Please attach a picture to your message.")
				await asyncio.sleep(10)
				await msg.delete()




	@commands.command()
	async def userid(self, ctx, mention = None):
		if mention is None :
			m_author = ctx.message.author

		else :
			m_author = ctx.message.mentions[0]

		await ctx.send("`{}`".format(m_author.id))


	@commands.command()
	async def icon(self, ctx, mention = None):
		if mention is None :
			m_author = ctx.message.author

		else :
			m_author = ctx.message.mentions[0]

		await ctx.send(embed=embedpic(pic_url=m_author.avatar_url, url=m_author.avatar_url, author=m_author.name, title=None))


	@commands.command(description="Duel someone")
	async def duel(self, ctx):
		m_author = ctx.message.author
		opponent = ctx.message.mentions[0]
		duelists = [m_author.display_name, opponent.display_name]
		winner = randrange(0,2)

		with open("duel.json") as fp:
			deathlist = json.load(fp)
			deathlist_len = len(deathlist["deathlist"])
			death_number = randrange(0,deathlist_len)
			death = deathlist["deathlist"][death_number]

		result = "\n{} {}\n\n\U0001F3C6 {} won. \U0001F3C6".format(duelists[1-winner], death.replace("[opponent]",duelists[winner]), duelists[winner])

		await ctx.send("\U00002694 {} dueled {} ! \U00002694 \n{}".format(m_author.display_name, opponent.display_name, result))


	@commands.command(description="Ask something to the bot", aliases=["?"])
	async def ask(self, ctx):
		answerlist = ["Yes", "No", "Maybe", "No way", "For sure", "Of course", "No chance", "Absolutely", "Perhaps", "Possibly", "Nope"]
		await ctx.send(random.choice(answerlist))


	@commands.command(description="Rate the given argument")
	async def rate(self, ctx, *,arg : str):
		randnumber = randrange(0,102)
		if randnumber < 101:
			await ctx.send("I give **{}** a rate of {}/100".format(arg,randnumber))
		elif randnumber == 101 :
			await ctx.send("**{}** is overrated".format(arg))

	@commands.command(description="Make a dice roll")
	async def roll(self,ctx, dice = 6):
		randnumber = randrange(1, dice+1)
		if dice > 1000 :
			pass
		else :
			await ctx.send("{} rolled {}".format(ctx.message.author.display_name, randnumber))


	@commands.command(description="Choose from a list of things")
	async def choose(self,ctx,*, string : str):
		if "," in string :
			wordlist = string.split(",")
		else :
			wordlist = string.split()
		choice = random.choice(wordlist)
		while choice.startswith(" ") :
			choice = choice[1:]
		await ctx.send("I choose {}.".format(choice))


	@commands.command(description="Let Sarasa inspire you.", aliases=["iq", "inspirationalquote", "inspire"])
	async def inspirationalQuote(self, ctx):
		quote_request = requests.get("http://inspirobot.me/api?generate=true")
		quote_url = quote_request.text
		quote_em = embedpic(title=None, author=ctx.message.author.display_name, pic_url=quote_url, footer="From inspirobot.me")
		await ctx.send(embed=quote_em)

	@commands.command(description="Let Sarasa inspire you. Christmas version.", aliases=["xq"])
	async def xmasQuote(self, ctx):
		quote_request = requests.get("http://inspirobot.me/api?generate=true&season=xmas")
		quote_url = quote_request.text
		quote_em = embedpic(title=None, author=ctx.message.author.display_name, pic_url=quote_url, footer="From inspirobot.me")
		await ctx.send(embed=quote_em)

	@commands.command(description="Mix two nicknames together", aliases=["ship"])
	async def mix(self, ctx, nick1 : str, nick2 : str):
		letters1 = list(nick1)
		del letters1[-1]
		letters2 = list(nick2)
		del letters2[0]

		nick1_sets = []
		nick1_len = len(letters1)

		counter1 = 0
		while counter1 < nick1_len-1 :
			if not bool(nick1_sets) :
				nick1_sets.append(letters1[0] + letters1[1])
			else :
				nick1_sets.append(nick1_sets[counter1-1] + letters1[counter1+1])
			counter1 +=1


		nick2_sets = []
		nick2_len = len(letters2)

		counter2 = 0
		while counter2 < nick2_len-1 :
			if not bool(nick2_sets) :
				nick2_sets.append(letters2[-2] + letters2[-1])
			else :
				nick2_sets.append(letters2[-2-counter2] + nick2_sets[counter2-1])
			counter2 +=1

		part1 = random.choice(nick1_sets)
		part2 = random.choice(nick2_sets)
		result = part1 + part2
		result = result.lower().title()

		await ctx.send(result)


	@commands.command(description="Remix then Mix two nicknames together", aliases=["mix2"])
	async def remix2(self, ctx, nick1 : str, nick2 : str):
		letters1 = list(nick1)

		result1 = []

		while bool(letters1) :
			random_letter = random.choice(letters1)
			result1.append(random_letter)
			letters1.remove(random_letter)
		

		letters2 = list(nick2)
		result2 = []

		while bool(letters2) :
			random_letter = random.choice(letters2)
			result2.append(random_letter)
			letters2.remove(random_letter)

		nick1_sets = []
		nick1_len = len(result1)

		counter1 = 0
		while counter1 < nick1_len-1 :
			if not bool(nick1_sets) :
				nick1_sets.append(result1[0] + result1[1])
			else :
				nick1_sets.append(nick1_sets[counter1-1] + result1[counter1+1])
			counter1 +=1
			print(nick1_sets)


		nick2_sets = []
		nick2_len = len(result2)

		counter2 = 0
		while counter2 < nick2_len-1 :
			if not bool(nick2_sets) :
				nick2_sets.append(result2[-2] + result2[-1])
			else :
				nick2_sets.append(result2[-2-counter2] + nick2_sets[counter2-1])
			counter2 +=1
			print(nick2_sets)

		part1 = random.choice(nick1_sets)
		part2 = random.choice(nick2_sets)
		result = part1 + part2
		result = result.lower().title()

		await ctx.send(result)

	@commands.command(description="Remix a string of text")
	async def remix(self, ctx, *, text : str):
		letters = list(text)
		len_text = len(letters)
		result = ""

		while bool(letters) :
			random_letter = random.choice(letters)
			result += random_letter
			letters.remove(random_letter)

		await ctx.send(result.lower().title())

	#OCR
	@commands.command(description="Run OCR on a picture to get the text written on a picture", aliases=["ocr"])
	async def OCR(self, ctx, language="eng" , url=None):
		if url is None :
			print(ctx.message.attachments[0].url)
			request = ocr(url=ctx.message.attachments[0].url, language=language)
		else :
			request=ocr(url)
		jsonparse = json.loads(request)
		result = jsonparse["ParsedResults"][0]["ParsedText"]
		await ctx.send(result)

	@commands.command(description="When someone really likes something")
	async def love(self, ctx, mention, *, text : str):
		m_author = ctx.message.mentions[0]

		font = ImageFont.truetype(font="./fonts/animeace2_bld.ttf", size=26, encoding="unic")

		icon_response = requests.get(m_author.avatar_url)

		canvas = Image.open("./misc/sword_template.jpg")
		canvas.convert("RGBA")
		icon = Image.open(BytesIO(icon_response.content))
		icon.thumbnail((150,150),Image.BICUBIC)

		canvas.paste(icon, (221,2))

		W, H = (198, 55)
		TextCanvas = Image.new("RGBA",(W,H), (255,255,255,0))

		DrawText = ImageDraw.Draw(TextCanvas)
		w, h = DrawText.textsize(text, font)
		if w > W :
			font = ImageFont.truetype(font="./fonts/animeace2_bld.ttf", size=20, encoding="unic")
			w, h = DrawText.textsize(text, font)
		DrawText.text(((W-w)/2,((H-h)/2)-13), text, fill="black", font=font)
		canvas.paste(TextCanvas, (621,336), TextCanvas)

		canvas.save("{}.jpg".format(m_author.id))
		await ctx.send(file=discord.File("{}.jpg".format(m_author.id)))
		os.remove("{}.jpg".format(m_author.id))

	@commands.command(description="When it's time for something")
	async def its(self, ctx, *, text : str):
		m_author = ctx.message.author

		font = ImageFont.truetype(font="./fonts/animeace2_reg.ttf", size=35, encoding="unic")

		icon_response = requests.get(m_author.avatar_url)

		canvas = Image.open("./misc/its_template.jpg")
		canvas.convert("RGBA")
		icon = Image.open(BytesIO(icon_response.content))
		icon.thumbnail((90,90),Image.BICUBIC)

		canvas.paste(icon, (300,84))

		W, H = (179, 49)
		TextCanvas = Image.new("RGBA",(W,H), (255,255,255,0))

		DrawText = ImageDraw.Draw(TextCanvas)
		w, h = DrawText.textsize(text, font)
		print(w)

		if w >= 290 :
			font = ImageFont.truetype(font="./fonts/animeace2_reg.ttf", size=20, encoding="unic")
			w, h = DrawText.textsize(text, font)
		elif w >= 200 :
			font = ImageFont.truetype(font="./fonts/animeace2_reg.ttf", size=25, encoding="unic")
			w, h = DrawText.textsize(text, font)
		DrawText.text(((W-w)/2,((H-h)/2)-8), text, fill="black", font=font)
		canvas.paste(TextCanvas, (60,69), TextCanvas)

		DrawText2 = ImageDraw.Draw(canvas)
		font = ImageFont.truetype(font="./fonts/animeace2_reg.ttf", size=13, encoding="unic")
		DrawText2.text((117,330), m_author.display_name, fill="black", font=font)

		canvas.save("{}.jpg".format(m_author.id))
		await ctx.send(file = discord.File("{}.jpg".format(m_author.id)))
		os.remove("{}.jpg".format(m_author.id))

	@commands.command(description="Tells you when you joined a server")
	async def when(self,ctx):
		m_author = ctx.message.author
		jointime = m_author.joined_at

		joinday = jointime.day
		joinmonth = jointime.month
		joinyear = jointime.year

		await ctx.send("You joined this server the {}/{}/{}".format(joinday,joinmonth,joinyear))

def setup(bot):
	bot.add_cog(Misc(bot))
