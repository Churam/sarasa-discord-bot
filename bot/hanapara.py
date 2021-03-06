import discord
from discord.ext import commands
import textwrap
from pathlib import Path
import json
import os
from PIL import ImageFont, Image, ImageDraw
from os import listdir
from os.path import isfile, join
import requests
from io import BytesIO
from datetime import datetime
import asyncio


#Server id for the Contributioncheck command
gw_server_id = "246519048559394817"


def font(name = "rg" ,font_size = 24):
	if name is "lt" :
		return ImageFont.truetype(font="./fonts/Aller_Lt.ttf", size=font_size, encoding="unic")
	elif name is "rg" :
		return ImageFont.truetype(font="./fonts/Aller_Rg.ttf", size=font_size, encoding="unic")
	elif name is "bd" :
		return ImageFont.truetype(font="./fonts/Aller_Bd.ttf", size=font_size, encoding="unic")

#To avoid having to write the same path all the time
def usrdata(userid):
	return "./users/{}/userdata.json".format(userid)

def server_file_exists(server_id) :
	serv_path = Path("./servers/{}.json".format(server_id))
	if serv_path.exists() :
		return True
	else :
		return False

def create_server_file(server_id, message) :
	server = message.server
	if server_file_exists(server_id) == False :
		with open("./servers/{}.json".format(server_id), 'w') as fc :
					server_infos = {"name" : server.name, "gw" : False}
					json.dump(server_infos, fc, indent = 4)


#Processes animated profiles
def processImage(m_author, infile):
	with open("./users/{}/userdata.json".format(m_author.id)) as fp:
		userdata = json.load(fp)
	try:
		im = Image.open(infile)
	except IOError:
		print("Cant load", infile)
	i = 0
	frames = []
	new_frames = []
	mypalette = im.getpalette()
	gifduration = im.info['duration']

	try:
		while 1:
			im.putpalette(mypalette)
			new_im = Image.new("RGBA", im.size)
			new_im.paste(im)
			frames.append(new_im)

			i += 1
			im.seek(im.tell() + 1)

	except EOFError:
		pass # end of sequence

	nickname = m_author.display_name

	title = userdata["title"]
	if title is "" :
		title = " "
	crystals = userdata["spark"]["crystals"]
	tix = userdata["spark"]["tickets"]
	tentix = userdata["spark"]["10tickets"]
	total_progress = (crystals + (tix*300) + (tentix*3000))/900
	money = userdata["money"]
	aboutme_txt = userdata["aboutme"]
	response = requests.get(m_author.avatar_url)

	for i in frames :
		
		canvas = Image.new("RGBA",(600,600),color=(255, 255, 255, 255))

		#Background
		background = i
		baseheight = 600
		hpercent = (baseheight/float(background.size[1]))
		wsize = int((float(background.size[0])*float(hpercent)))
		background = background.resize((wsize,baseheight), Image.BICUBIC)
		canvas.paste(background,(int((600-background.size[0])/2),0))
		canvas.paste(background,(int((600-background.size[0])/2),0))

		#Body transparent white Background
		bodycanvas = Image.new("RGBA",(600,600),color=(255, 255, 255, 0))
		bodysize = [0,200,600,600]
		body = ImageDraw.Draw(bodycanvas, mode="RGBA")
		body.rectangle(bodysize, fill=(255,255,255,127))
		canvas.alpha_composite(bodycanvas)

		#Body white boxes
		boxcanvas = Image.new("RGBA",(600,600),color=(255, 255, 255, 0))
		boxsize = [25,391,300,523]
		box = ImageDraw.Draw(boxcanvas, mode="RGBA")
		box.rectangle(boxsize, fill=(255,255,255,75))
		box2size = [358,391,580,523]
		box2 = ImageDraw.Draw(boxcanvas, mode="RGBA")
		box2.rectangle(box2size, fill=(255,255,255,75))

		#Spark Progress "Progress bar" BG
		progressbox = ImageDraw.Draw(boxcanvas, mode="RGBA")
		progressbox.rectangle([25,560,305,595], fill=(255,255,255,75))

		canvas.alpha_composite(boxcanvas)


		#Body Separator (White line)
		separator1 = ImageDraw.Draw(canvas, mode="RGBA")
		separator1.rectangle([0,198,600,202], fill=(255,255,255,255))

		#Icon
		icon = Image.open(BytesIO(response.content))
		icon.convert("RGBA")
		if icon.size[0] < 150 or icon.size[1] < 150 :
			icon = icon.resize((150,150), Image.BICUBIC)
		else :
			icon.thumbnail((150,150),Image.BICUBIC)

		bigsize = (icon.size[0] * 3, icon.size[1] * 3)
		mask = Image.new('L', bigsize, 0)
		draw = ImageDraw.Draw(mask) 
		draw.ellipse((0, 0) + bigsize, fill=255)
		mask = mask.resize(icon.size, Image.BICUBIC)
		icon.putalpha(mask)

		#Iconborder
		iconmask = Image.open("./assets/mask.png").convert('L')
		border = Image.new("RGBA",(1500,1500),(255,255,255,255))
		border.putalpha(iconmask)
		border.thumbnail((150,150), Image.BICUBIC)
		icon.paste(border,(0,0), border)

		canvas.paste(icon,(225,125), icon)

		#Separators (Black lines)
		separator2 = ImageDraw.Draw(canvas, mode="RGBA")
		separator2.rectangle([18,380,300,381], fill=(0,0,0,255))
		separator2.rectangle([352,380,600,381], fill=(0,0,0,255))
		separator2.rectangle([18,554,600,555], fill=(0,0,0,255))

		#Spark Progress bar
		progressbar = ImageDraw.Draw(canvas, mode="RGBA")
		if total_progress <= 100 :
			progressbar.rectangle([30,564,30+(270*(total_progress/100)),590], fill=(66,134,244,255))
		elif total_progress > 100 :
			progressbar.rectangle([30,564,300,590], fill=(66,134,244,255))


		#CurrencyIcons
		crystal_icon = Image.open("./assets/crystal.jpg")
		tix_icon = Image.open("./assets/ticket.png")
		tentix_icon = Image.open("./assets/10ticket.jpg")

		crystal_icon.thumbnail((25,25), Image.BICUBIC)
		tix_icon.thumbnail((25,25), Image.BICUBIC)
		tentix_icon.thumbnail((25,25), Image.BICUBIC)

		canvas.paste(crystal_icon,(376,565))
		canvas.paste(tix_icon,(471,565))
		canvas.paste(tentix_icon,(541,565))

		#Nickname
		nicknamecanvas = Image.new("RGBA",(600,40),color=(255, 255, 255, 0))
		nickname_text = ImageDraw.Draw(nicknamecanvas)
		w, h = draw.textsize(nickname, font=font("bd",32))
		nickname_text.text(((600-w)/2,(40-h)/2), nickname, fill="black", font=font("bd",32))
		canvas.alpha_composite(nicknamecanvas,(0,275))

		#title
		titlecanvas = Image.new("RGBA",(600,28),color=(255, 255, 255, 0))
		title_text = ImageDraw.Draw(titlecanvas)
		w, h = draw.textsize(title, font=font("lt",24))
		title_text.text(((600-w)/2,(28-h)/2), title, fill="black", font=font("lt",24))
		canvas.alpha_composite(titlecanvas,(0,307))

		#Categories
		drawtext = ImageDraw.Draw(canvas)
		drawtext.text((18,352),"Information", fill="black" ,font=font("rg",26))
		drawtext.text((352,352),"About me", fill="black" ,font=font("rg",26))
		drawtext.text((18,523),"Spark progression", fill="black" ,font=font("rg",25))

		#Information text
		drawtext.text((30,393),"Currency", fill="black" ,font=font("lt",24))
		drawtext.text((195,393),"{}".format(money), fill="black" ,font=font("lt",24))
		flower = Image.open("./assets/flower.png").convert("RGBA")
		flower.thumbnail((23,23),Image.BICUBIC)
		canvas.paste(flower,(270,394),flower)

		#Spark progression text
		drawtext.text((307,565), "{}%".format(int(total_progress)), fill="black",font=font("lt",23))
		drawtext.text((403,565), "{}".format(crystals), fill="black",font=font("lt",21))
		drawtext.text((498,565), "{}".format(tix), fill="black",font=font("lt",21))
		drawtext.text((569,565), "{}".format(tentix), fill="black",font=font("lt",22))

		#About Me text
		offset = 0
		linewidth = 30
		aboutme_wrap = textwrap.wrap(aboutme_txt, width=linewidth)

		for i in range(len(aboutme_wrap)) :
			while font("lt",20).getsize(aboutme_wrap[i])[0] >= 200 :
				linewidth -= 1
				aboutme_wrap = textwrap.wrap(aboutme_txt, width=linewidth)

		for line in aboutme_wrap:
			drawtext.text((365, 391+offset), line, font=font("lt",20), fill="black")
			offset += font("lt",20).getsize(line)[1]
			offset += 2

		canvas.thumbnail((300,300), Image.ANTIALIAS)
		new_frames.append(canvas)

	return {'gif': new_frames,'duration': gifduration}


class Hanapara():
	def __init__(self, bot):
		self.client = bot


	@commands.command(description="Show your profile", aliases=["p"], pass_context=True)
	async def profile(self, ctx, mention = None):

		if mention is None :
			m_author = ctx.message.author

		else :
			m_author = ctx.message.mentions[0]

		m_channel = ctx.message.channel
		await self.client.send_typing(m_channel)

		with open('./users/{}/userdata.json'.format(m_author.id)) as n:
			userdata = json.load(n)

		nickname = m_author.display_name

		title = userdata["title"]
		if title is "" :
			title = " "
		crystals = userdata["spark"]["crystals"]
		tix = userdata["spark"]["tickets"]
		tentix = userdata["spark"]["10tickets"]
		total_progress = (crystals + (tix*300) + (tentix*3000))/900
		money = userdata["money"]
		aboutme_txt = userdata["aboutme"]
		response = requests.get(m_author.avatar_url)
		if userdata.get("profile_mode") is None :
			with open("./users/{}/userdata.json".format(m_author.id),'w', encoding="UTF-8") as s:
				userdata["profile_mode"] = "still"
				json.dump(userdata,s, indent=2)

		if "still" in userdata["profile_mode"] :

			canvas = Image.new("RGBA",(600,600),color=(255, 255, 255, 255))

			#Check if the user already has a background picture, if not use the default one.
			bg_path = Path("./users/{}/bg.jpg".format(m_author.id))
			if bg_path.is_file():
				background = Image.open("./users/{}/bg.jpg".format(m_author.id))
			else :
				background = Image.open("./assets/bg.png")
			canvas.paste(background,(int((600-background.size[0])/2),0))

			#Body transparent white Background
			bodycanvas = Image.new("RGBA",(600,600),color=(255, 255, 255, 0))
			bodysize = [0,200,600,600]
			body = ImageDraw.Draw(bodycanvas, mode="RGBA")
			body.rectangle(bodysize, fill=(255,255,255,127))
			canvas.alpha_composite(bodycanvas)

			#Body white boxes
			boxcanvas = Image.new("RGBA",(600,600),color=(255, 255, 255, 0))
			boxsize = [25,391,300,523]
			box = ImageDraw.Draw(boxcanvas, mode="RGBA")
			box.rectangle(boxsize, fill=(255,255,255,75))
			box2size = [358,391,580,523]
			box2 = ImageDraw.Draw(boxcanvas, mode="RGBA")
			box2.rectangle(box2size, fill=(255,255,255,75))

			#Spark Progress "Progress bar" BG
			progressbox = ImageDraw.Draw(boxcanvas, mode="RGBA")
			progressbox.rectangle([25,560,305,595], fill=(255,255,255,75))

			canvas.alpha_composite(boxcanvas)


			#Body Separator (White line)
			separator1 = ImageDraw.Draw(canvas, mode="RGBA")
			separator1.rectangle([0,198,600,202], fill=(255,255,255,255))

			#Icon
			icon = Image.open(BytesIO(response.content))
			icon.convert("RGBA")
			if icon.size[0] < 150 or icon.size[1] < 150 :
				icon = icon.resize((150,150), Image.BICUBIC)
			else :
				icon.thumbnail((150,150),Image.BICUBIC)

			bigsize = (icon.size[0] * 3, icon.size[1] * 3)
			mask = Image.new('L', bigsize, 0)
			draw = ImageDraw.Draw(mask) 
			draw.ellipse((0, 0) + bigsize, fill=255)
			mask = mask.resize(icon.size, Image.BICUBIC)
			icon.putalpha(mask)

			#Iconborder
			iconmask = Image.open("./assets/mask.png").convert('L')
			border = Image.new("RGBA",(1500,1500),(255,255,255,255))
			border.putalpha(iconmask)
			border.thumbnail((150,150), Image.BICUBIC)
			icon.paste(border,(0,0), border)

			canvas.paste(icon,(225,125), icon)

			#Separators (Black lines)
			separator2 = ImageDraw.Draw(canvas, mode="RGBA")
			separator2.rectangle([18,380,300,381], fill=(0,0,0,255))
			separator2.rectangle([352,380,600,381], fill=(0,0,0,255))
			separator2.rectangle([18,554,600,555], fill=(0,0,0,255))

			#Spark Progress bar
			progressbar = ImageDraw.Draw(canvas, mode="RGBA")
			if total_progress <= 100 :
				progressbar.rectangle([30,564,30+(270*(total_progress/100)),590], fill=(66,134,244,255))
			elif total_progress > 100 :
				progressbar.rectangle([30,564,300,590], fill=(66,134,244,255))


			#CurrencyIcons
			crystal_icon = Image.open("./assets/crystal.jpg")
			tix_icon = Image.open("./assets/ticket.png")
			tentix_icon = Image.open("./assets/10ticket.jpg")

			crystal_icon.thumbnail((25,25), Image.BICUBIC)
			tix_icon.thumbnail((25,25), Image.BICUBIC)
			tentix_icon.thumbnail((25,25), Image.BICUBIC)

			canvas.paste(crystal_icon,(376,565))
			canvas.paste(tix_icon,(471,565))
			canvas.paste(tentix_icon,(541,565))

			#Nickname
			nicknamecanvas = Image.new("RGBA",(600,40),color=(255, 255, 255, 0))
			nickname_text = ImageDraw.Draw(nicknamecanvas)
			w, h = draw.textsize(nickname, font=font("bd",32))
			nickname_text.text(((600-w)/2,(40-h)/2), nickname, fill="black", font=font("bd",32))
			canvas.alpha_composite(nicknamecanvas,(0,275))

			#title
			titlecanvas = Image.new("RGBA",(600,28),color=(255, 255, 255, 0))
			title_text = ImageDraw.Draw(titlecanvas)
			w, h = draw.textsize(title, font=font("lt",24))
			title_text.text(((600-w)/2,(28-h)/2), title, fill="black", font=font("lt",24))
			canvas.alpha_composite(titlecanvas,(0,307))

			#Categories
			drawtext = ImageDraw.Draw(canvas)
			drawtext.text((18,352),"Information", fill="black" ,font=font("rg",26))
			drawtext.text((352,352),"About me", fill="black" ,font=font("rg",26))
			drawtext.text((18,523),"Spark progression", fill="black" ,font=font("rg",25))

			#Information text
			drawtext.text((30,393),"Currency", fill="black" ,font=font("lt",24))
			drawtext.text((195,393),"{}".format(money), fill="black" ,font=font("lt",24))
			flower = Image.open("./assets/flower.png").convert("RGBA")
			flower.thumbnail((23,23),Image.BICUBIC)
			canvas.paste(flower,(270,394),flower)

			#Spark progression text
			drawtext.text((307,565), "{}%".format(int(total_progress)), fill="black",font=font("lt",23))
			drawtext.text((403,565), "{}".format(crystals), fill="black",font=font("lt",21))
			drawtext.text((498,565), "{}".format(tix), fill="black",font=font("lt",21))
			drawtext.text((569,565), "{}".format(tentix), fill="black",font=font("lt",22))

			#About Me text
			offset = 0
			linewidth = 30
			fontsize = 20
			aboutme_wrap = textwrap.wrap(aboutme_txt, width=linewidth)

			for i in range(len(aboutme_wrap)) :
				while font("lt",fontsize).getsize(aboutme_wrap[i])[0] >= 200 :
					linewidth -= 1
					aboutme_wrap = textwrap.wrap(aboutme_txt, width=linewidth)

			for line in aboutme_wrap:
				drawtext.text((365, 391+offset), line, font=font("lt",20), fill="black")
				offset += font("lt",20).getsize(line)[1]
				offset += 2


			canvas.thumbnail((300,300), Image.BICUBIC)
			canvas.save("{}.png".format(m_author.id))
			await self.client.send_file(m_channel,"{}.png".format(m_author.id))
			await asyncio.sleep(15)
			os.remove("{}.png".format(m_author.id))

		elif "animated" in userdata["profile_mode"]:
			#Check if bg exists
			bg_path = Path("./users/{}/bg.gif".format(m_author.id))
			if bg_path.is_file():
				background = Image.open("./users/{}/bg.gif".format(m_author.id))
			else :
				background = Image.open("./assets/bg.gif")

			gif = processImage(m_author, bg_path)
			gif_duration = gif['duration']
			gif = gif["gif"]
			gifcanvas = gif[0]
			del gif[0]
			gifcanvas.save("{}.gif".format(m_author.id), save_all=True, append_images=gif, loop=99, duration=gif_duration)
			await self.client.send_file(ctx.message.channel,"{}.gif".format(m_author.id))
			await asyncio.sleep(15)
			os.remove("{}.gif".format(m_author.id))

	@commands.group(description="Set of command to customize one's profile.",name="set")
	async def _set(self):
		pass

	@_set.command(description="Set a background (Will be resized to a height of 600px )\nAdd reset or default to reset your background", pass_context=True, name="background", aliases=["bg"])
	async def _background(self, ctx, link = None):
		m_author = ctx.message.author
		m_channel = ctx.message.channel
		try :
			attachment = ctx.message.attachments
			bg_url = attachment[0]['url']
			#print(attachment[0]['url'])
			response = requests.get(bg_url)
			bg = Image.open(BytesIO(response.content))
			print(bg_url)
			if bg_url.endswith(".gif") :
				dl = requests.get(bg_url)
				with open("./users/{}/bg.gif".format(m_author.id), "wb") as f:
					f.write(dl.content)

			else :
				baseheight = 600
				hpercent = (baseheight/float(bg.size[1]))
				wsize = int((float(bg.size[0])*float(hpercent)))
				bg = bg.resize((wsize,baseheight), Image.BICUBIC)

				bg.convert('RGB').save('./users/{}/bg.jpg'.format(m_author.id))

			msg = "\U00002611 Your background has been successfully changed." 
			await self.client.say(msg)
		except IndexError :
			if link is None :
				await self.client.say("\U0000274E Please attach a picture to your message or send a link.")

			elif link.endswith(".jpg") or link.endswith(".png") and link.startswith("http") :
				bg_url = link
				response = requests.get(bg_url)
				bg = Image.open(BytesIO(response.content))

				baseheight = 600
				hpercent = (baseheight/float(bg.size[1]))
				wsize = int((float(bg.size[0])*float(hpercent)))
				bg = bg.resize((wsize,baseheight), Image.BICUBIC)

				bg.convert('RGB').save('./users/{}/bg.jpg'.format(m_author.id))
				await self.client.say("\U00002611 Your background has been successfully changed.")

			elif link.endswith(".gif"):
				dl = requests.get(link)
				with open("./users/{}/bg.gif".format(m_author.id), "wb") as f:
					f.write(dl.content)
				await self.client.say("\U00002611 Your background has been successfully changed.")


			elif link.startswith("default") or link.startswith("reset") :
				os.remove("./users/{}/bg.jpg".format(m_author.id))
				await self.client.say("\U00002611 Your background has been successfully reset.")

			

	@_set.command(description="Change your profile message", aliases=["am","about"], pass_context=True)
	async def _aboutme(self, ctx, *, msg):
		m_author = ctx.message.author
		m_channel = ctx.message.channel
		with open("./users/{}/userdata.json".format(m_author.id)) as fp:
			data = json.load(fp)

		linewidth = 30
		aboutme_txt = msg
		aboutme_wrap = textwrap.wrap(aboutme_txt, width=linewidth)

		for i in range(len(aboutme_wrap)) :
			while font("lt",1).getsize(aboutme_wrap[i])[0] >= 200 :
				linewidth -= 1
				aboutme_wrap = textwrap.wrap(aboutme_txt, width=linewidth)

		if len(aboutme_wrap) > 6 :
			await self.client.say("\U0000274E Your message is too long")

		else :
			with open("./users/{}/userdata.json".format(m_author.id), 'w', encoding="UTF-8") as f:
				data["aboutme"] = msg
				json.dump(data,f, ensure_ascii=False, indent=2)
			msg = "\U00002611 Your profile has been successfully changed." 
			await self.client.say(msg)

		
	@_set.command(description="Change someone's title (Admin only)", pass_context=True, name="title")
	async def _title(self, ctx, mention, *, msg):
		m_author = ctx.message.author
		mention = ctx.message.mentions[0]
		author_permissions = m_author.permissions_in(ctx.message.channel)
		if author_permissions.administrator :
			with open("./users/{}/userdata.json".format(mention.id)) as fp:
				data = json.load(fp)
			with open("./users/{}/userdata.json".format(mention.id), "w", encoding="UTF-8") as f:
				data["title"] = msg
				json.dump(data,f, indent=2)
			await self.client.say("{}'s title successfully set to **{}**".format(mention.mention, msg))
		else :
			await self.client.say("\U0000274E You don't have the right to do that.")


	@_set.command(description="Change your profile's background to be still or animated", pass_context=True, name="mode")
	async def _mode(self, ctx, mode):
		m_author = ctx.message.author
		with open('./users/{}/userdata.json'.format(m_author.id)) as fp:
			data = json.load(fp)

		if "animated" in mode or "gif" in mode or "GIF" in mode :
			with open('./users/{}/userdata.json'.format(m_author.id),'w', encoding="UTF-8") as f:
				data["profile_mode"] = "animated"
				json.dump(data,f, indent=2)
			await self.client.say("\U00002611 Your profile mode has been set to **animated**.")

		elif "still" in mode or "jpg" in mode or "png" in mode :
			with open('./users/{}/userdata.json'.format(m_author.id),'w', encoding="UTF-8") as f:
				data["profile_mode"] = "still"
				json.dump(data,f, indent=2)
			await self.client.say("\U00002611 Your profile mode has been set to **still**.")


	@commands.group(description="Stay updated about the progress of your spark !", pass_context=True)
	async def spark(self, ctx):
		m_author = ctx.message.author
		m_author_id = m_author.id
		with open('./users/{}/userdata.json'.format(m_author_id)) as fp:
			spark_datas = json.load(fp)
			spark_datas = spark_datas["spark"]
		if ctx.invoked_subcommand is None :
			total_crystals = spark_datas["crystals"]
			total_tickets = spark_datas["tickets"]
			total_10tickets = spark_datas["10tickets"]
			total_draws = int((total_crystals/300) + total_tickets + (total_10tickets*10))
			await self.client.say("You have {} crystals, {} draw ticket(s) and {} 10-part draw ticket(s) for a total of {} draws.".format(total_crystals, total_tickets, total_10tickets, total_draws))


	@spark.command(pass_context=True, name="add", brief="- Add a certain amount of a given element.", help="Add a certain amount of a given element. \nAvailable elements :\n - Crystals : crystal, crystals \n - Draw tickets : ticket, tickets, tix \n - 10-part draw tickets : 10ticket, 10tickets, 10tix")
	async def spark_add(self, ctx, element : str, amount : int):
		m_author = ctx.message.author
		m_author_id = m_author.id
		element = element.lower()
		with open('./users/{}/userdata.json'.format(m_author_id)) as fp:
			spark_datas = json.load(fp)

		if element == "crystals" or element == "crystal" :
			with open('./users/{}/userdata.json'.format(m_author_id), mode="w", encoding='utf-8') as fp :
				spark_datas["spark"]["crystals"] += amount
				json.dump(spark_datas, fp, indent=2)

		elif element == "ticket" or element == "tickets" or element == "tix" :
			with open('./users/{}/userdata.json'.format(m_author_id), mode="w", encoding='utf-8') as fp :
				spark_datas["spark"]["tickets"] += amount
				json.dump(spark_datas, fp, indent=2)

		elif element == "10ticket" or element == "10tickets" or element == "10tix" :
			with open('./users/{}/userdata.json'.format(m_author_id), mode="w", encoding='utf-8') as fp :
				spark_datas["spark"]["10tickets"] += amount
				json.dump(spark_datas, fp, indent=2)

		else :
			await self.client.say("I don't know what you're trying to do.")

		total_crystals = spark_datas["spark"]["crystals"]
		total_tickets = spark_datas["spark"]["tickets"]
		total_10tickets = spark_datas["spark"]["10tickets"]
		total_draws = int((total_crystals/300) + total_tickets + (total_10tickets*10))
		await self.client.say("You now have {} crystals, {} draw ticket(s) and {} 10-part draw ticket(s) for a total of {} draws.".format(total_crystals, total_tickets, total_10tickets, total_draws))


	@spark.command(pass_context=True, name="set", brief="- Set a certain amount of a given element.", help="Set a certain amount of a given element. \nAvailable elements :\n - Crystals : crystal, crystals \n - Draw tickets : ticket, tickets, tix \n - 10-part draw tickets : 10ticket, 10tickets, 10tix")
	async def spark_set(self, ctx, element : str, amount : int):
		m_author = ctx.message.author
		m_author_id = m_author.id
		element = element.lower()
		with open('./users/{}/userdata.json'.format(m_author_id)) as fp:
			spark_datas = json.load(fp)

		if element == "crystals" or element == "crystal" :
			with open('./users/{}/userdata.json'.format(m_author_id), mode="w", encoding='utf-8') as fp :
				spark_datas["spark"]["crystals"] = amount
				json.dump(spark_datas, fp, indent=2)

		elif element == "ticket" or element == "tickets" or element == "tix" :
			with open('./users/{}/userdata.json'.format(m_author_id), mode="w", encoding='utf-8') as fp :
				spark_datas["spark"]["tickets"] = amount
				json.dump(spark_datas, fp, indent=2)

		elif element == "10ticket" or element == "10tickets" or element == "10tix" :
			with open('./users/{}/userdata.json'.format(m_author_id), mode="w", encoding='utf-8') as fp :
				spark_datas["spark"]["10tickets"] = amount
				json.dump(spark_datas, fp, indent=2)

		else :
			await self.client.say("I don't know what you're trying to do.")

		total_crystals = spark_datas["spark"]["crystals"]
		total_tickets = spark_datas["spark"]["tickets"]
		total_10tickets = spark_datas["spark"]["10tickets"]
		total_draws = int((total_crystals/300) + total_tickets + (total_10tickets*10))
		await self.client.say("You now have {} crystals, {} draw ticket(s) and {} 10-part draw ticket(s) for a total of {} draws.".format(total_crystals, total_tickets, total_10tickets, total_draws))


	@spark.command(pass_context=True, name="reset", help="- Resets your spark completely.")
	async def spark_reset(self,ctx):
		m_author = ctx.message.author
		m_author_id = m_author.id
		with open('./users/{}/userdata.json'.format(m_author_id)) as fp:
			spark_datas = json.load(fp)

		with open('./users/{}/userdata.json'.format(m_author_id), mode="w", encoding='utf-8') as fp :
			spark_datas["spark"]["crystals"] = 0
			spark_datas["spark"]["tickets"] = 0
			spark_datas["spark"]["10tickets"] = 0
			json.dump(spark_datas, fp, indent=2)
		await self.client.say("Spark succesfully reset.")


	@commands.group(description="Currency related commands.", aliases=["$"])
	async def money(self):
		pass


	@money.command(description="! Admin Only ! Add flowers to someone's account.", name="add", pass_context=True)
	async def _add(self, ctx, mention, amount : int ):
		
		m_author = ctx.message.author
		mention = ctx.message.mentions[0]
		author_permissions = m_author.permissions_in(ctx.message.channel)

		if mention is None or amount is None:
			await self.client.say("\U0000274E | Correct format is `$$ add <mention> <amount>`")

		elif author_permissions.administrator:
			with open("./users/{}/userdata.json".format(mention.id)) as fp:
				data = json.load(fp)
			with open("./users/{}/userdata.json".format(mention.id), "w", encoding="UTF-8") as f:
				data["money"] += amount
				json.dump(data,f, indent=2)
			await self.client.say("\U0001F4B5 | Successfully gave {}\U0001F4AE to **{}**".format(amount,mention.mention))
		
		else :
			await self.client.say("\U0000274E | You don't have the right to do that.")


	@money.command(description="Transfer flowers to someone.", name="give", pass_context=True)
	async def _give(self, ctx, mention, amount : int ):
		
		m_author = ctx.message.author
		mention = ctx.message.mentions[0]
		author_permissions = m_author.permissions_in(ctx.message.channel)
		with open("./users/{}/userdata.json".format(m_author.id)) as x:
			authordata = json.load(x)
		author_money = authordata["money"]
		if author_money < amount :
			await self.client.say("\U0000274E | You don't have enough {}\U0001F4AE to do that.")

		else :
			with open("./users/{}/userdata.json".format(mention.id)) as fp:
				targetdata = json.load(fp)
			with open("./users/{}/userdata.json".format(mention.id), "w", encoding="UTF-8") as f:
				targetdata["money"] += amount
				json.dump(targetdata,f, indent=2)

			with open("./users/{}/userdata.json".format(m_author.id), 'w', encoding="UTF-8") as y:
				authordata["money"] -= amount
				json.dump(authordata,y, indent=2)
			await self.client.say("\U0001F4B5 | Successfully transferred {}\U0001F4AE to **{}**".format(amount,mention.mention))


	@commands.command(pass_context=True, description="Set or change your registered GBF nickname.", aliases=["pn"])
	async def playername(self, ctx, *, nickname=None) :
		nickname = str(nickname)
		m_author = ctx.message.author
		with open(usrdata(m_author.id)) as fp :
			UserDatas = json.load(fp)

		if nickname is None :
			pass

		else :

			UserDatas["nickname"] = nickname

			with open(usrdata(m_author.id), 'w') as x :
				json.dump(UserDatas, x, indent=2)

			await self.client.say("Your registered player name was set to **{}**".format(nickname))


	@commands.command(pass_context=True, description="Check someone's GBF nickname.", aliases=["cn"])
	async def checkname(self, ctx):
		mention_user = ctx.message.mentions[0]
		with open(usrdata(mention_user.id)) as fp :
			UserDatas = json.load(fp)

		if "nickname" not in UserDatas or UserDatas["nickname"] == "" :
			await self.client.say("{} hasn't registered a GBF nickname.".format(mention_user.display_name))
		else :
			await self.client.say("{}'s GBF nickname is **{}**.".format(mention_user.display_name, UserDatas["nickname"]))

	@commands.command(pass_context = True, description = "Put the server in GW mode", aliases = ["gw"])
	async def guildwar(self, ctx, mode : str) :
		m_author = ctx.message.author
		m_server = ctx.message.server
		serv_path = Path("./servers/{}.json".format(ctx.message.server.id))
		if (mode != "on" and mode != "off") or not m_author.permissions_in(ctx.message.channel).administrator :
			pass
		else :
			create_server_file(m_server.id, ctx.message)
			with open("./servers/{}.json".format(m_server.id), 'r') as sfr :
				server_infos = json.load(sfr)
			if mode == "on" and server_infos["gw"] == False:
				for i in m_server.members :
					with open(usrdata(i.id), 'r') as fr :
						infos = json.load(fr)
					if "nickname" not in infos :
						print("{} hasn't registered a GBF nickname.".format(i.display_name))
					elif not i.permissions_in(ctx.message.channel).administrator :
						with open(usrdata(i.id), 'w') as fw :
							infos["tmp_nickname"] = i.display_name
							json.dump(infos, fw, indent = 4)
						await self.client.change_nickname(i, infos["nickname"])
				await self.client.say("GW mode enabled successfully")
				with open("./servers/{}.json".format(m_server.id), 'w') as sfw :
					server_infos["gw"] = True
					json.dump(server_infos, sfw, indent = 4)

			elif mode == "off" and server_infos["gw"] == True:
				for i in m_server.members :
					with open(usrdata(i.id), 'r') as fr :
						infos = json.load(fr)
					if "tmp_nickname" not in infos :
						pass
					elif not i.permissions_in(ctx.message.channel).administrator :
						await self.client.change_nickname(i, infos["tmp_nickname"])
				await self.client.say("GW mode disabled successfully")
				with open("./servers/{}.json".format(m_server.id), 'w') as sfw :
					server_infos["gw"] = False
					json.dump(server_infos, sfw, indent = 4)


	@commands.command(pass_context=True, description="Send your contribution for checking.", aliases=["cc"])
	async def contribcheck(self, ctx, amount : int) :
		m_author = ctx.message.author
		now = datetime.now()
		month = now.month
		year = now.year
		server_id = ctx.message.server.id
		global gw_server_id

		if server_id not in gw_server_id :
			await self.client.say("\U0000274E | You cannot do that here.")
		else :

			with open(usrdata(m_author.id), encoding="UTF-8") as fp :
				userdata = json.load(fp)

			if userdata.get("totalcontrib-{}{}".format(month,year)) is None :
				with open(usrdata(m_author.id), 'w', encoding="UTF-8") as x :
					userdata["totalcontrib-{}{}".format(month,year)] = 0
					json.dump(userdata,x, indent=2)

			if amount < userdata["totalcontrib-{}{}".format(month,year)] :
				await self.client.say("\U0000274E | The contribution you submitted is lower than your current amount of total contribution, please make sure you submitted the total contribution instead of the daily.")

			else :
				await self.client.add_reaction(ctx.message, "\U00002705")
				await self.client.add_reaction(ctx.message, "\U0000274E")

				res = await self.client.wait_for_reaction(['\U00002705', '\U0000274E'], message=ctx.message)
				res_perm = res.user.permissions_in(ctx.message.channel)

				while res_perm.administrator is False and res.user.id != "90878360053366784":
					res = await self.client.wait_for_reaction(['\U00002705', '\U0000274E'], message=ctx.message)
					res_perm = res.user.permissions_in(ctx.message.channel)

				if res.reaction.emoji in '\U0000274E' :
					await self.client.say('\U0000274E | Your contribution check was denied.')

				elif res.reaction.emoji in '\U00002705' :

					with open(usrdata(m_author.id), 'w', encoding="UTF-8") as f :
						money_amount = amount - userdata["totalcontrib-{}{}".format(month,year)]
						userdata["money"] += (int(round(money_amount/10000)))
						userdata["totalcontrib-{}{}".format(month,year)] = amount
						json.dump(userdata,f, indent=2)

					await self.client.say("\U00002705 | Your contribution check was validated and {}\U0001F4AE were added to your account.".format(int(round(money_amount/10000))))


	# ----------------------------------- Text Command ------------------------------------- #

	"""
	TODO : Instead of going through every users in the users directory, instead check every users presents in the server
	"""
	@commands.command(pass_context=True, description="Shows the scoreboard for the current GW", aliases=["sb"])
	async def scoreboard(self, ctx, crewname = None):
		directory = os.walk('users/')
		userlist = []
		now = datetime.now()
		month = now.month
		year = now.year
		server = ctx.message.server
		embedcolor = discord.Colour.teal()
		if crewname is not None :
			crewname = crewname.lower()
			for i in ctx.message.server.roles :
				if i.name.lower() in crewname :
					embedcolor = i.colour


		for x in directory :
			uid = x[0].replace("users/","")
			userlist.append(uid)


		del userlist[0]

		scoreboard = {}

		for i in userlist :
			with open("./users/{}/userdata.json".format(i)) as fp :
				userdata = json.load(fp)

			if userdata.get("totalcontrib-{}{}".format(month,year)) is None :
				pass

			else :
				try :
					member = server.get_member(i)
					m_roles = member.roles
				except Exception as e :
					print(e)
					pass
				position = 0
				m_rolesname = []
				for i in m_roles :
					m_rolesname.append(i.name.lower())
					position+=1


				if member is None :
					pass
				
				elif crewname is None :
					scoreboard[member.name.title] = userdata["totalcontrib-{}{}".format(month,year)]

				elif crewname in m_rolesname :
					scoreboard[member.name.title()] = userdata["totalcontrib-{}{}".format(month,year)]

				elif crewname not in m_roles :
					pass


		res = list(sorted(scoreboard, key=scoreboard.__getitem__, reverse=True))
		nicknames = ""
		scores = ""
		counter = 1
		totalscore = 0
		for i in res :
			nicknames += "{} - {}       \n\n".format(counter,i)
			totalscore += scoreboard[i]
			scores += "{:,}\n\n".format(scoreboard[i])
			#print("{} {}".format(i, scoreboard[i]))
			counter += 1

		if crewname is None:
			crewname = ""
		else :
			crewname = crewname.title()
		embedobj = discord.Embed(title="{} Ranking for this month's GW".format(crewname), colour=embedcolor)
		embedobj.add_field(name="Nickname", value=nicknames, inline=True)
		embedobj.add_field(name="Score", value=scores, inline=True)
		embedobj.add_field(name="Total score", value="\n{:,}".format(totalscore), inline=False)
		await self.client.send_message(ctx.message.channel,embed=embedobj)

def setup(bot):
	bot.add_cog(Hanapara(bot))

