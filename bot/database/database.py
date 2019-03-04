import sqlite3
import json

#db connection
db = sqlite3.connect("./database/zooey_db.sqlite3")
curs = db.cursor()

async def check_user(uid, table = "main"):
	if table == "main" :
		curs.execute("SELECT uid FROM main WHERE uid = (?)", (uid,))
	elif table == "spark" :
		curs.execute("SELECT uid FROM spark WHERE uid = (?)", (uid,))
	exists = curs.fetchone()
	if exists :
		return True
	else :
		return False

async def adduser(userid) :
	if not await check_user(userid) :
		title = ""
		about_me = ""
		money = 0
		gbf_name = ""
		profile_mode = "still"
		waifu = []
		husbando = []
		datas = [userid, title, about_me, money, gbf_name, profile_mode, json.dumps(waifu), json.dumps(waifu), None, None]
		curs.execute('INSERT INTO main VALUES (?,?,?,?,?,?,?,?,?,?)', datas)
		db.commit()
	else :
		pass

async def updateuser(userid, column, content):
	if await check_user(userid) :
		if column == "about" :
			curs.execute("UPDATE main set about = (?) WHERE uid = (?)", (content, userid))
		elif column == "title" :
			curs.execute("UPDATE main set title = (?) WHERE uid = (?)", (content, userid))
		elif column == "profile_mode" :
			curs.execute("UPDATE main set profile_mode = (?) WHERE uid = (?)", (content, userid))
		elif column == "bg" :
			curs.execute("UPDATE main set bg = (?) WHERE uid = (?)", (content, userid))
		elif column == "anim_bg" :
			curs.execute("UPDATE main set anim_bg = (?) WHERE uid = (?)", (content, userid))
		elif column == "money" :
			curs.execute("UPDATE main set money = (?) WHERE uid = (?)", (content, userid))
		elif column == "gbf_name" :
			curs.execute("UPDATE main set gbf_name = (?) WHERE uid = (?)", (content, userid))
		elif column == "waifu" :
			curs.execute("UPDATE main set waifu = (?) WHERE uid = (?)", (content, userid))
		elif column == "husbando" :
			curs.execute("UPDATE main set husbando = (?) WHERE uid = (?)", (content, userid))
		db.commit()
	else :
		pass