import discord
from discord.ext import commands
import json
import asyncio
from datetime import datetime

#To avoid having to write the same path all the time
def usrdata(userid):
	return "./users/{}/userdata.json".format(userid)

class goal():
	def __init__(self, bot):
		self.client = bot

	"""
	Goals list : Set objectives to keep track of things you want to achieve.
	"""
	@commands.group(pass_context=True, description="Set objectives to keep track of things you want to achieve.", aliases=["ol"])
	async def goalslist(self,ctx):
		if ctx.invoked_subcommand is None:
			command_summoner = ctx.message.author
			if len(ctx.message.mentions) != 0 :
				m_author = ctx.message.mentions[0]
			
			else :
				m_author = ctx.message.author

			with open(usrdata(m_author.id)) as f :
				UserDatas = json.load(f)

			if "goals" not in UserDatas or bool(UserDatas["goals"]) is False :
				ErrorMessage = await self.client.say("You don't have any objectives yet, try adding some !")
				await asyncio.sleep(10)
				await self.client.delete_message(ErrorMessage)

			else :
				#Load the user's current objectives
				goal = UserDatas["goals"]

				#List to store the embeds and make the page system easier
				embeds = []

				#Embed for the In-Progress Objectives
				IP_embed = discord.Embed(title="In progress", colour=0x80ffff )
				embeds.append(IP_embed)

				#Embed for the On-Hold objectives
				OH_embed = discord.Embed(title="On-hold", colour=0xff8040)
				embeds.append(OH_embed)

				#Embed for the Completed objectives
				C_embed = discord.Embed(title="Completed", colour=0x80ff80)
				embeds.append(C_embed)

				#Assign each goals to a category
				for i in goal :
					if goal[i]["status"] == "In Progress" :
						embeds[0].add_field(name="{}. {}".format(i, goal[i]["description"]), inline=False, value="Added : {}".format(goal[i]["StartDate"]))
						embeds[0].set_author(name=m_author.display_name)

					elif goal[i]["status"] == "On Hold" :
						embeds[1].add_field(name="{}. {}".format(i, goal[i]["description"]), inline=False, value="Added : {}".format(goal[i]["StartDate"]))
						embeds[1].set_author(name=m_author.display_name)

					elif goal[i]["status"] == "Completed" :
						embeds[2].add_field(name="{}. {}".format(i, goal[i]["description"]), inline=False, value="Added : {} | Completed : {}".format(goal[i]["StartDate"],goal[i]["EndDate"]))
						embeds[2].set_author(name=m_author.display_name)

				#Pages
				count = 0
				msg = await self.client.say(embed=embeds[0])
				await self.client.add_reaction(msg, "\u2B05")
				await self.client.add_reaction(msg, "\u27A1")
				while True :
					try :
						res = await self.client.wait_for_reaction(['\u2B05', '\u27A1'],user=command_summoner, message=msg, timeout=10)

						#await self.client.say('{0.user} reacted with {0.reaction.emoji}!'.format(res))
						if res.reaction.emoji == "\u2B05" :
							if count > 0 :
								count -= 1
								await self.client.edit_message(msg, embed=embeds[count])
							else :
								count = len(embeds) - 1
								await self.client.edit_message(msg, embed=embeds[count])
							await self.client.remove_reaction(msg, '\u2B05', res.user)

						elif res.reaction.emoji == "\u27A1":
							if count < (len(embeds)-1) :
								count += 1
								await self.client.edit_message(msg, embed=embeds[count])
							else :
								count = 0
								await self.client.edit_message(msg, embed=embeds[count])

							await self.client.remove_reaction(msg, "\u27A1", res.user)
					except Exception as e:
						print(e)
						break
				await self.client.clear_reactions(msg)


	@goalslist.command(pass_context=True, name="add")
	async def addgoal(self, ctx, *, goal : str):
		m_author = ctx.message.author
		IDList = []
		NowTime = datetime.now()
		month = NowTime.month
		day = NowTime.day
		year = NowTime.year
		GoalID = 0

		with open(usrdata(m_author.id)) as f :
			UserDatas = json.load(f)

		if "goals" not in UserDatas or bool(UserDatas) is False :
			UserDatas["goals"] = {}


		#Assign the ID of the objective
		for i in UserDatas["goals"] :
			IDList.append(int(i))

		if bool(IDList) is False : #If IDList is empty
			GoalID = 1

		else :
			GoalID = sorted(IDList)[-1] + 1


		#If goal contains ;, add several objectives

		if ";" in goal :
			goalList = goal.split(";")
			formatedGoalList = []

			for i in goalList :
				if i.startswith(" ") :
					i[1:]
				if i.endswith(" ") :
					i[:-1]

				for x in UserDatas["goals"] :
					IDList.append(int(x))

				if bool(IDList) is False : #If IDList is empty
					GoalID = 1

				else :
					GoalID = sorted(IDList)[-1] + 1

				UserDatas["goals"][GoalID] = {"description" : i, "status" : "In Progress", "StartDate" : "{}/{}/{}".format(month, day, year), "EndDate" : ""}

		else :
			#Date is in MM/DD/YY Format
			UserDatas["goals"][GoalID] = {"description" : goal, "status" : "In Progress", "StartDate" : "{}/{}/{}".format(month, day, year), "EndDate" : ""}

		with open(usrdata(m_author.id), "w") as o :
			json.dump(UserDatas, o, indent=2)

		await self.client.say("Objective(s) successfully added !")


	@goalslist.command(pass_context=True, name="remove")
	async def removegoal(self,ctx, goalid : str):
		m_author = ctx.message.author
		with open(usrdata(m_author.id)) as f :
			UserDatas = json.load(f)

		try :
			del UserDatas["goals"][goalid]

		except :
			await self.client.say("There isn't any objective with that ID.")
		else :

			with open(usrdata(m_author.id), "w") as x :
				json.dump(UserDatas, x, indent=2)

			await self.client.say("Successfully removed that objective from your list !")

	@goalslist.command(pass_context=True, name="update")
	async def updategoal(self,ctx, goalid : str):
		m_author = ctx.message.author

		NowTime = datetime.now()
		month = NowTime.month
		day = NowTime.day
		year = NowTime.year

		with open(usrdata(m_author.id)) as f :
			UserDatas = json.load(f)

		goals = UserDatas["goals"]

		if goalid not in goals :
			await self.client.say("There is no objective with that ID.")

		else :

			GoalEmbed=discord.Embed(title="{}. {}".format(goalid, goals[goalid]["description"]), description="Status: {}".format(goals[goalid]["status"]))

			#Define the color of the embed depending on the status of the objective
			if goals[goalid]["status"] == "In Progress" :
				GoalEmbed.color=0x80ffff

			elif goals[goalid]["status"] == "On Hold" :
				GoalEmbed.color=0xff8040

			elif goals[goalid]["status"] == "Completed" :
				GoalEmbed.color=0x80ff80

			GoalMessage = await self.client.say(embed=GoalEmbed)

			emojis = ["\U0001F1E8","\U0001F1ED", "\U0001F1F5", "\U0000274E"]
			for i in emojis :
				await self.client.add_reaction(GoalMessage, i)

			while True :
				try :
					GoalReaction = await self.client.wait_for_reaction(emojis, message=GoalMessage, user=m_author, timeout=10)

					if GoalReaction.reaction.emoji == "\U0001F1E8" : #C
						goals[goalid]["status"] = "Completed"
						goals[goalid]["EndDate"] = "{}/{}/{}".format(month, day, year)
						GoalEmbed.color=0x80ff80
						await self.client.remove_reaction(GoalMessage, "\U0001F1E8", m_author)

					elif GoalReaction.reaction.emoji == "\U0001F1ED" : #H
						goals[goalid]["status"] = "On Hold"
						GoalEmbed.color=0xff8040
						await self.client.remove_reaction(GoalMessage, "\U0001F1ED", m_author)

					elif GoalReaction.reaction.emoji == "\U0001F1F5" : #P
						goals[goalid]["status"] = "In Progress"
						GoalEmbed.color=0x80ffff
						await self.client.remove_reaction(GoalMessage, "\U0001F1F5", m_author)

					elif GoalReaction.reaction.emoji == "\U0000274E" : #Cross mark
						break

					GoalEmbed.description = "Status: {}".format(goals[goalid]["status"])

					if goals[goalid]["status"] != "Completed" and goals[goalid]["EndDate"] != "" :
						goals[goalid]["EndDate"] = ""

					await self.client.edit_message(GoalMessage, embed=GoalEmbed)

				except Exception as e :
					print(e)
					break

			await self.client.clear_reactions(GoalMessage)
			UserDatas["goals"] = goals
			with open(usrdata(m_author.id), "w") as x:
				json.dump(UserDatas, x, indent=2)

	@goalslist.command(pass_context=True, name="info")
	async def infogoal(self,ctx, goalid : str):
		m_author = ctx.message.author
		with open(usrdata(m_author.id)) as f:
			UserDatas = json.load(f)

		goal = UserDatas["goals"][goalid]

		if goalid not in UserDatas["goals"] :
			await self.client.say("There is no objective with that ID.")
		else :

			embed=discord.Embed(color=0x80ffff)

			#Set color depending on status
			if goal["status"] == "Completed" :
				embed.color=0x80ff80

			elif goal["status"] == "On Hold" :
				embed.color=0xff8040

			elif goal["status"] == "In Progress" :
				embed.color=0x80ffff

			embed.add_field(name="{}. {}".format(goalid, goal["description"]), value="Started : {}".format(goal["StartDate"]), inline=True)
			embed.add_field(name="{}".format(goal["status"]), value="Finished : {}".format(goal["EndDate"]), inline=True)
			await self.client.say(embed=embed)

def setup(bot):
	bot.add_cog(goal(bot))