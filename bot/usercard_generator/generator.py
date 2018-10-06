from PIL import Image, ImageFont, ImageDraw
import textwrap

nickname = "Akeyro"
title = "Banned"
crystals = 60000
tix = 50
tentix = 5
total_progress = (crystals + (tix*300) + (tentix*3000))/900
money = 26421
aboutme_txt = "Help Help Help Help Help Help Help Help Help Help Help Help "

def font(name = "rg" ,font_size = 24):
	if name is "lt" :
		return ImageFont.truetype(font="./fonts/Aller_Lt.ttf", size=font_size, encoding="unic")
	elif name is "rg" :
		return ImageFont.truetype(font="./fonts/Aller_Rg.ttf", size=font_size, encoding="unic")
	elif name is "bd" :
		return ImageFont.truetype(font="./fonts/Aller_Bd.ttf", size=font_size, encoding="unic")

canvas = Image.new("RGBA",(600,600),color=(255, 255, 255, 255))


background = Image.open("bg.jpg")
canvas.paste(background,(0,0))

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
icon = Image.open("icon.png")
icon.convert("RGBA")
icon.thumbnail((150,150),Image.ANTIALIAS)
bigsize = (icon.size[0] * 3, icon.size[1] * 3)
mask = Image.new('L', bigsize, 0)
draw = ImageDraw.Draw(mask) 
draw.ellipse((0, 0) + bigsize, fill=255)
mask = mask.resize(icon.size, Image.ANTIALIAS)
icon.putalpha(mask)

#Iconborder
iconmask = Image.open("mask.png").convert('L')
border = Image.new("RGBA",(1500,1500),(255,255,255,255))
border.putalpha(iconmask)
border.thumbnail((150,150), Image.ANTIALIAS)
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
	progressbar.rectangle([30,564,300*(total_progress/100),590], fill=(66,134,244,255))
elif total_progress > 100 :
	progressbar.rectangle([30,564,300,590], fill=(66,134,244,255))


#CurrencyIcons
crystal_icon = Image.open("crystal.jpg")
tix_icon = Image.open("ticket.png")
tentix_icon = Image.open("10ticket.jpg")

crystal_icon.thumbnail((25,25), Image.ANTIALIAS)
tix_icon.thumbnail((25,25), Image.ANTIALIAS)
tentix_icon.thumbnail((25,25), Image.ANTIALIAS)

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
flower = Image.open("flower.png").convert("RGBA")
flower.thumbnail((23,23),Image.ANTIALIAS)
canvas.paste(flower,(270,394),flower)

#Spark progression text
drawtext.text((307,565), "{}%".format(int(total_progress)), fill="black",font=font("lt",23))
drawtext.text((403,565), "{}".format(crystals), fill="black",font=font("lt",21))
drawtext.text((498,565), "{}".format(tix), fill="black",font=font("lt",21))
drawtext.text((569,565), "{}".format(tentix), fill="black",font=font("lt",22))

#About Me text
offset = 0
linewidth = 50
aboutme_wrap = textwrap.wrap(aboutme_txt, width=linewidth)

for i in range(len(aboutme_wrap)) :
	while font("lt",15).getsize(aboutme_wrap[i])[0] >= 155 :
		linewidth -= 1
		aboutme_wrap = textwrap.wrap(aboutme_txt, width=linewidth)

for line in aboutme_wrap:
	drawtext.text((365, 391+offset), line, font=font("lt",20), fill="black")
	offset += font("lt",15).getsize(line)[1]
	offset += 4

if len(aboutme_wrap) > 6 :
	print("There are too much lines !")

canvas.thumbnail((300,300), Image.ANTIALIAS)
canvas.save("test.png")