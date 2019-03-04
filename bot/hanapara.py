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
from database.database import check_user, updateuser, curs, db

async def addspark(userid, crystals = 0, tix = 0, ten_tix = 0):
	if not await check_user(userid, "spark") :
		curs.execute('INSERT INTO spark VALUES (?,?,?,?)', (userid, crystals, tix, ten_tix))
		db.commit()

async def updatespark(userid, crystals = 0, tix = 0, ten_tix = 0):
	if await check_user(userid, "spark") :
		curs.execute("UPDATE spark SET crystal = (?), ticket = (?), ten_ticket = (?) WHERE uid = (?)", (crystals, tix, ten_tix, userid))
		db.commit()
	else :
		await addspark(userid, crystals, tix, ten_tix)

async def getspark(userid) :
	await addspark(userid, 0, 0, 0)
	curs.execute("SELECT crystal, ticket, ten_ticket FROM spark WHERE uid = (?)", (userid,))
	spark = curs.fetchall()
	return spark

async def search_userdata(pk, col_name, table = "main"):
	infos = [col_name, table, int(pk)]
	curs.execute("SELECT (?) FROM main WHERE uid = (?)", infos)
	res = curs.fetchone()
	return res


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
async def processImage(m_author, im):
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
	curs.execute("SELECT title, about, money FROM main WHERE uid = (?)", (m_author.id,))
	userdata = curs.fetchone()
	title = userdata[0]
	if title is "" :
		title = " "
	sparkdata = await getspark(m_author.id)
	crystals = sparkdata[0][0]
	tix = sparkdata[0][1]
	tentix = sparkdata[0][2]
	total_progress = (crystals + (tix*300) + (tentix*3000))/900
	money = userdata[2]
	aboutme_txt = userdata[1]
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


	@commands.command(description="Show your profile", aliases=["p"])
	async def profile(self, ctx, mention = None):
		"Shows your profile !"
		if mention is None :
			m_author = ctx.message.author
		else :
			m_author = ctx.message.mentions[0]

		m_channel = ctx.message.channel
		await ctx.channel.trigger_typing()

		nickname = m_author.display_name

		curs.execute("SELECT title, about, money, profile_mode FROM main WHERE uid = (?)", (m_author.id,))
		userdata = curs.fetchone()
		title = userdata[0]
		if title is "" :
			title = " "
		sparkdata = await getspark(m_author.id)
		crystals = sparkdata[0][0]
		tix = sparkdata[0][1]
		tentix = sparkdata[0][2]
		total_progress = (crystals + (tix*300) + (tentix*3000))/900
		money = userdata[2]
		aboutme_txt = userdata[1]
		response = requests.get(m_author.avatar_url)

		if "still" in userdata[3] :

			canvas = Image.new("RGBA",(600,600),color=(255, 255, 255, 255))

			#Check if the user already has a background picture, if not use the default one.
			curs.execute("SELECT bg FROM main WHERE uid = (?)", (m_author.id,))
			bg_data = curs.fetchone()[0]
			if bg_data:
				background = Image.open(BytesIO(bg_data))
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
			await ctx.send(file = discord.File("{}.png".format(m_author.id)))
			await asyncio.sleep(10)
			os.remove("{}.png".format(m_author.id))

		elif "animated" in userdata[3]:
			#Check if bg exists
			await ctx.channel.trigger_typing()
			curs.execute("SELECT anim_bg FROM main WHERE uid = (?)", (m_author.id,))
			bg_data = curs.fetchone()[0]
			if bg_data:
				background = Image.open(BytesIO(bg_data))
			else :
				background = Image.open("./assets/bg.gif")

			gif = await processImage(m_author, background)
			gif_duration = gif["duration"]
			gif = gif["gif"]
			gifcanvas = gif[0]
			del gif[0]
			gifcanvas.save("{}.gif".format(m_author.id), save_all=True, append_images=gif, loop=99, duration=gif_duration)
			await ctx.send(file = discord.File("{}.gif".format(m_author.id)))
			await asyncio.sleep(15)
			os.remove("{}.gif".format(m_author.id))

	@commands.group(description="Set of command to customize one's profile.",name="set")
	async def _set(self, ctx):
		pass

	@_set.command(description="Set a background (Will be resized to a height of 600px )\nAdd reset or default to reset your background", name="background", aliases=["bg"])
	async def _background(self, ctx, link = None):
		m_author = ctx.message.author
		m_channel = ctx.message.channel
		try :
			attachment = ctx.message.attachments
			bg_url = attachment[0].url
			#print(attachment[0]['url'])
			response = requests.get(bg_url)
			bg = Image.open(BytesIO(response.content))
			if bg_url.endswith(".gif") :
				dl = requests.get(bg_url)
				bgBytes = sqlite3.Binary(dl.content)
				await updateuser(m_author.id, "anim_bg", bgBytes)

			else :
				baseheight = 600
				hpercent = (baseheight/float(bg.size[1]))
				wsize = int((float(bg.size[0])*float(hpercent)))
				bg = bg.resize((wsize,baseheight), Image.BICUBIC)

				bgBytes = BytesIO()
				bg.convert('RGB').save(bgBytes, format = 'JPEG')
				await updateuser(m_author.id, "bg", bgBytes.getvalue())

			msg = "\U00002611 Your background has been successfully changed." 
			await ctx.send(msg)
		except IndexError :
			if link is None :
				await ctx.send("\U0000274E Please attach a picture to your message or send a link.")

			elif link.endswith(".jpg") or link.endswith(".png") and link.startswith("http") :
				bg_url = link
				response = requests.get(bg_url)
				bg = Image.open(BytesIO(response.content))

				baseheight = 600
				hpercent = (baseheight/float(bg.size[1]))
				wsize = int((float(bg.size[0])*float(hpercent)))
				bg = bg.resize((wsize,baseheight), Image.BICUBIC)

				bgBytes = BytesIO()
				bg.convert('RGB').save(bgBytes, format = 'JPEG')
				await updateuser(m_author.id, "bg", bgBytes.getvalue())
				await ctx.send("\U00002611 Your background has been successfully changed.")

			elif link.endswith(".gif"):
				dl = requests.get(link)
				bgBytes = sqlite3.Binary(dl.content)
				await updateuser(m_author.id, "anim_bg", bgBytes)
				await ctx.send("\U00002611 Your background has been successfully changed.")


			elif link.startswith("default") or link.startswith("reset") :
				await updateuser(m_author.id, "bg", None)
				await ctx.send("\U00002611 Your background has been successfully reset.")

			

	@_set.command(description="Change your profile message", aliases=["am","about"])
	async def _aboutme(self, ctx, *, msg):
		m_author = ctx.message.author
		m_channel = ctx.message.channel
		linewidth = 30
		aboutme_txt = msg
		aboutme_wrap = textwrap.wrap(aboutme_txt, width=linewidth)

		for i in range(len(aboutme_wrap)) :
			while font("lt",1).getsize(aboutme_wrap[i])[0] >= 200 :
				linewidth -= 1
				aboutme_wrap = textwrap.wrap(aboutme_txt, width=linewidth)

		if len(aboutme_wrap) > 6 :
			await ctx.send("\U0000274E Your message is too long")

		else :
			await updateuser(m_author.id, "about", msg)
			res = "\U00002611 Your profile has been successfully changed." 
			await ctx.send(res)

		
	@_set.command(description="Change someone's title (Admin only)", name="title")
	async def _title(self, ctx, mention, *, msg):
		m_author = ctx.message.author
		mention = ctx.message.mentions[0]
		author_permissions = m_author.permissions_in(ctx.message.channel)
		if author_permissions.administrator :
			await updateuser(m_author.id, "title", msg)
			await ctx.send("{}'s title successfully set to **{}**".format(mention.mention, msg))
		else :
			await ctx.send("\U0000274E You don't have the right to do that.")


	@_set.command(description="Change your profile's background to be still or animated", name="mode")
	async def _mode(self, ctx, mode):
		m_author = ctx.message.author

		if "animated" in mode or "gif" in mode or "GIF" in mode :
			await updateuser(m_author.id, "profile_mode", "animated")
			await ctx.send("\U00002611 Your profile mode has been set to **animated**.")

		elif "still" in mode or "jpg" in mode or "png" in mode :
			await updateuser(m_author.id, "profile_mode", "still")
			await ctx.send("\U00002611 Your profile mode has been set to **still**.")


	@commands.group(description="Stay updated about the progress of your spark !")
	async def spark(self, ctx):
		m_author = ctx.message.author
		m_author_id = m_author.id
		if ctx.invoked_subcommand is None :
			spark = await getspark(ctx.author.id)
			crystals = spark[0][0]
			tickets = spark[0][1]
			tentickets = spark[0][2]
			total_draws = int((crystals/300) + tickets + (tentickets*10))
			await ctx.send("You have {} crystals, {} draw ticket(s) and {} 10-part draw ticket(s) for a total of {} draws.".format(crystals, tickets, tentickets, total_draws))


	@spark.command(name="add", brief="- Add a certain amount of a given element.", help="Add a certain amount of a given element. \nAvailable elements :\n - Crystals : crystal, crystals \n - Draw tickets : ticket, tickets, tix \n - 10-part draw tickets : 10ticket, tentickets, 10tix")
	async def spark_add(self, ctx, element : str, amount : int):
		m_author = ctx.message.author
		m_author_id = m_author.id
		element = element.lower()
		spark = await getspark(m_author_id)
		crystals = spark[0][0]
		tickets = spark[0][1]
		tentickets = spark[0][2]

		if element == "crystals" or element == "crystal" :
			crystals += amount

		elif element == "ticket" or element == "tickets" or element == "tix" :
			tickets += amount

		elif element == "10ticket" or element == "tentickets" or element == "10tix" :
			tentickets += amount

		else :
			await ctx.send("I don't know what you're trying to do.")

		await updatespark(m_author_id, crystals, tickets, tentickets)
		total_draws = int((crystals/300) + tickets + (tentickets*10))
		await ctx.send("You now have {} crystals, {} draw ticket(s) and {} 10-part draw ticket(s) for a total of {} draws.".format(crystals, tickets, tentickets, total_draws))


	@spark.command(name="set", brief="- Set a certain amount of a given element.", help="Set a certain amount of a given element. \nAvailable elements :\n - Crystals : crystal, crystals \n - Draw tickets : ticket, tickets, tix \n - 10-part draw tickets : 10ticket, tentickets, 10tix")
	async def spark_set(self, ctx, element : str, amount = None):
		m_author = ctx.message.author
		m_author_id = m_author.id
		element = element.lower()
		spark = await getspark(m_author_id)
		crystals = spark[0][0]
		tickets = spark[0][1]
		tentickets = spark[0][2]

		if amount is None :
			nb_list = element.split(";")
			if len(nb_list) > 3 :
				await ctx.send("There are too much elements.")
				return
			items = [crystals, tickets, tentickets]
			for i in range(len(nb_list)) :
				if i is 0 :
					crystals = int(nb_list[i])
				elif i is 1 :
					tickets = int(nb_list[i])
				elif i is 2 :
					tentickets = int(nb_list[i])
		else :

			if element == "crystals" or element == "crystal" :
				crystals = amount

			elif element == "ticket" or element == "tickets" or element == "tix" :
				tickets = amount

			elif element == "10ticket" or element == "tentickets" or element == "10tix" :
				tentickets = amount

			else :
				await ctx.send("I don't know what you're trying to do.")

		await updatespark(m_author_id, crystals, tickets, tentickets)
		total_draws = int((crystals/300) + tickets + (tentickets*10))
		await ctx.send("You now have {} crystals, {} draw ticket(s) and {} 10-part draw ticket(s) for a total of {} draws.".format(crystals, tickets, tentickets, total_draws))


	@spark.command(name="reset", help="- Resets your spark completely.")
	async def spark_reset(self,ctx):
		m_author = ctx.message.author
		m_author_id = m_author.id
		await updatespark(m_author.id)
		await ctx.send("Spark succesfully reset.")


	@commands.group(description="Currency related commands.", name="money", aliases=["$"])
	async def _money(self, ctx):
		pass


	@_money.command(description="! OWNER ONLY ! Add flowers to someone's account.", name="add")
	async def _add(self, ctx, mention, amount : int ):
		
		m_author = ctx.message.author
		mention_user = ctx.message.mentions[0]

		if mention is None or amount is None:
			await ctx.send("\U0000274E | Correct format is `$$ add <mention> <amount>`")

		elif m_author.id == 90878360053366784:
			money = curs.execute("SELECT money from main WHERE uid = (?)", [mention_user.id]).fetchone()[0]
			await updateuser(mention_user.id, "money", money + amount)
			await ctx.send("\U0001F4B5 | Successfully added {} \U0001F4AE to **{}**'s account".format(amount, mention_user.display_name))
		
		else :
			await ctx.send("\U0000274E | You don't have the right to do that.")


	@_money.command(description="Transfer flowers to someone.", name="give")
	async def _give(self, ctx, mention, amount : int ):
		m_author = ctx.message.author
		mention = ctx.message.mentions[0]
		author_money = curs.execute("SELECT money from main WHERE uid = (?)", [m_author.id]).fetchone()[0]
		if author_money < amount :
			await ctx.send("\U0000274E | You don't have enough {}\U0001F4AE to do that.")

		else :
			mention_money = curs.execute("SELECT money from main WHERE uid = (?)", [mention.id]).fetchone()[0]
			await updateuser(m_author.id, "money", author_money - amount)
			await updateuser(mention.id, "money", mention_money + amount)
			await ctx.send("\U0001F4B5 | Successfully transferred {}\U0001F4AE to **{}**".format(amount,mention.mention))


	@_set.command(description="Set or change your registered GBF nickname.", aliases=["sn"])
	async def setname(self, ctx, *, nickname=None) :
		nickname = str(nickname)
		m_author = ctx.message.author

		if nickname is None :
			pass

		else :
			await updateuser(m_author.id, "gbf_name", nickname)
			await ctx.send("Your registered player name was set to **{}**".format(nickname))


	@commands.command(description="Check someone's GBF nickname.", aliases=["cn"])
	async def checkname(self, ctx):
		try :
			mention_user = ctx.message.mentions[0]
		except IndexError :
			mention_user = ctx.author
		user_nickname = curs.execute("SELECT gbf_name FROM main WHERE uid = (?)", [mention_user.id]).fetchone()[0]

		if user_nickname == "" :
			await ctx.send("{} hasn't registered a GBF nickname. Register one with `$setname`.".format(mention_user.display_name))
		else :
			await ctx.send("{}'s GBF nickname is **{}**.".format(mention_user.display_name, user_nickname))

def setup(bot):
	bot.add_cog(Hanapara(bot))

