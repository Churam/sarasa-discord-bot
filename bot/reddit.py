import discord
from discord.ext import commands
import random

#------------------------- Reddit pic grabber ---------------------- #
from urllib.request import urlopen
import re
import praw
from bs4 import BeautifulSoup #Parser module
import lxml

reddit = praw.Reddit(client_id='CLIENT_ID',
                     client_secret='CLIENT_SECRET',
                     password='REDDIT_PASSWORD',
                     user_agent='BOT_DESCRIPTION',
                     username='REDDIT_USERNAME')


#----------------------------------------------------


def redditpic(subreddit,limit=100, tfilter="day"):
    posts = reddit.subreddit(str(subreddit)).hot()#top(time_filter=tfilter, limit=limit)
    post_obj = []

    for i in posts :
        post_obj.append(i)

    post = random.choice(post_obj)
    while "i.imgur.com" not in post.url and "i.redd.it" not in post.url :
        post = random.choice(post_obj)

    return post


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
    


class Reddit():
    def __init__(self, bot):
        self.client = bot

    @commands.command(pass_context=True, aliases=["ameme", "am"])
    async def animeme(self, ctx):
        m_author_name = ctx.message.author.name
        await self.client.send_typing(ctx.message.channel)
        post = redditpic(subreddit="animemes")
        post_title = post.title
        post_url = post.url
        post_shortlink = post.shortlink
        post_score = post.score

        await self.client.say(embed=embedpic(title=post_title, url=post_shortlink, pic_url=post_url, author=m_author_name, description="{} points".format(post_score), color=0x609371))


    @commands.command(pass_context=True, aliases=["anirl"])
    async def animeirl(self, ctx):
        m_author_name = ctx.message.author.name
        await self.client.send_typing(ctx.message.channel)
        post = redditpic(subreddit="anime_irl")
        post_title = post.title
        post_url = post.url
        post_shortlink = post.shortlink
        post_score = post.score

        await self.client.say(embed=embedpic(title=post_title, url=post_shortlink, pic_url=post_url, author=m_author_name, description="{} points".format(post_score), color=0x609371))

    @commands.command(pass_context=True, aliases=["mi"])
    async def meirl(self, ctx):
        m_author_name = ctx.message.author.name
        await self.client.send_typing(ctx.message.channel)
        post = redditpic(subreddit="me_irl", tfilter="day", limit=50)
        post_title = post.title
        post_url = post.url
        post_shortlink = post.shortlink
        post_score = post.score

        await self.client.say(embed=embedpic(title=post_title, url=post_shortlink, pic_url=post_url, author=m_author_name, description="{} points".format(post_score), color=0x609371))


def setup(bot):
    bot.add_cog(Reddit(bot))