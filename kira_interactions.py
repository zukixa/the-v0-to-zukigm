# Discord Bot Project 
# Section - Interactions
# Commands based on the 'some-random-api'-API.
# Includes all non-image based commands from the API.
# Note: Keeping up the API is out of my hands and I cannot guarantee this working at any time.
import discord
from discord.ext import commands
# below required for API usage
import aiohttp
import sr_api 

client = sr_api.Client()

class interactapi(commands.Cog):
    @commands.command()
    async def fact(self,ctx,str:str):
        """random fact: Available options: cat, dog, koala, fox, bird, elephant, panda, racoon, kangaroo, giraffe, whale"""
        try:
            result = await client.get_fact(str)
            await ctx.send(result)
        except discord.Exception:
            await ctx.send('Pick a valid option: cat, dog, koala, fox, bird, elephant, panda, racoon, kangaroo, giraffe, whale')
    
    @commands.command()
    async def gif(self,ctx,str:str):
        """random gif: Available options: wink, pat, hug, face-palm"""
        try:
            result = await client.get_gif(str)
            await ctx.send(result)
        except:
            await ctx.send('Not a valid gif.')
    @commands.command()
    async def talk(self,ctx,*,str:str):
        """talk to chatbot [[[very likely its cleverbot]]]"""
        try:
            result = await client.chatbot(str)
            await ctx.send(result)
        except:
            await ctx.send('What?')

    @commands.command()
    async def joke(self,ctx):
        """get a haha funny"""
        try:
            result = await client.get_joke()
            await ctx.send(result)
        except:
            await ctx.send('¿a?')
    @commands.command()
    async def mcuser(self,ctx,stri:str):
        """get minecraft user data"""
        result = await client.mc_user(stri)
        embed = discord.Embed(
            title = "%s/%s\n" % (result.name, result.uuid),
            color = ctx.author.color
        )
        embed.add_field(name="Name History:",value=str(result.formatted_history),inline=True)
        await ctx.send(embed=embed)
