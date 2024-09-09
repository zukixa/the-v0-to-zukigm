# Discord Bot Project 
# Section - ImagesAPI
# Commands based on the 'some-random-api'-API.
# Includes all image based commands from the API.
# Note: It will be likely easier to rewrite this entire thing into one command with a massive switch statement
# Or at least it would require less repeating, hopefully?

# ^
# |
# no
#
#

# Note: Keeping up the API is out of my hands and I cannot guarantee this working at any time.
import discord
from discord.ext import commands
import random
import asyncio
# below required for API usage
import aiohttp 
import sr_api
from PIL import Image
import io
client = sr_api.Client()
#below the mess that is all of this, is the holy grail of 'client.filter(option, url)'
class imagesapi(commands.Cog):
    
    @commands.command(name='i')
    async def getimage(self,ctx,str):
        """Get an image of a: birb,cat,dog,fox,kangaroo,koala,panda,pika,racoon,redpanda,whale"""
        data = await client.get_image(str)
        embed = discord.Embed(
            title="Here's your "+str,
            color=ctx.author.color
        )
        embed.set_image(url=data.url)
        await ctx.send(embed=embed)

    @commands.command(name='filter')
    async def filter(self,ctx,option=None,url=None):
        """Give an image a nice touch. Options: gay, wasted, greyscale, invert, triggered, blur, blurple, glass, pixelate, sepia, invertgreyscale, brightness, threshold, red, green, blue, spin"""
        #there's supposedely some problems with the command below [said by the creator], yet I do not think there is an issue.
        if option == None:
            await ctx.send('Options are: gay, wasted, greyscale, invert, triggered, blur, blurple, glass, pixelate, sepia, invertgreyscale, brightness, threshold, red, green, blue, spin')
            return
        elif url == None:
            await ctx.send('An image is required.')
            return
        image = client.filter(option,url)
        embed = discord.Embed(
            title="Here's your "+option,
            color = ctx.author.color
        )
        embed.set_image(url=image.url)
        await ctx.send(embed=embed)
    
    @commands.command(name='color')
    #note, this is hex code
    async def viewcolor(self,ctx,color):
        """View a color from words!"""
        image = client.view_color(color)
        embed = discord.Embed(
            title="Here's your "+color,
            color = ctx.author.color
        )
        embed.set_image(url=image.url)
        await ctx.send(embed=embed)
