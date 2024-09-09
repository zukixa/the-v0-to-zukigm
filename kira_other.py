# Discord Bot Project 
# Section - Other
# Commands that not necessarily can be grouped anywhere
# Can include anything not appropriate elsewhere.
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import random
import asyncio
try:
    import simplejson as json
except ImportError:
    import json
# below required for outside-api usage
import aiohttp
import sr_api
import wikipedia
import string
client = sr_api.Client()

class Other(commands.Cog):

    @commands.command()
    async def randomname(self,ctx,length:int):
        """Generate a random string of characters"""
        await ctx.send(''.join(random.choice(string.ascii_lowercase) for i in range(length)))

    @commands.command()
    #wikipedias
    async def wiki(self,ctx,term:str):
        """IT WORKS."""
        t = wikipedia.search(term,results=1,suggestion=True)
        h = wikipedia.page(t[0], None, False, True, False);
        await ctx.send(h.url)
    @commands.command()
    async def randwiki(self,ctx):
        """random wikipedia page"""
        t = wikipedia.random(pages=1)
        h = wikipedia.page(t, None, False, True, False);
        await ctx.send(h.url)
        
    # It is finally fixed, and will be used once I learn how to have the bot
    # automaticcally check for things on its own, since it cant do that right now.
    @commands.command()
    async def reactcheck(self,ctx, msg: discord.Message):
        """List all reactions posted to a given message"""
        s = ""
        for v in msg.reactions:
            s += f"{v.emoji} {v.count} times\n"
        await ctx.send(s)
        
    @commands.command()
    async def dm(self,ctx,member:discord.Member,*,text):
        """DM a user Publically."""
        if member.dm_channel == None:
            channel = await member.create_dm()
        channel = member.dm_channel
        json_file_path = "/chatlog.json"
        with open(json_file_path, 'r') as f:
            fulltext = json.load(f)
        with open(json_file_path, 'w') as f:
            fulltext[str(ctx.message.id)] = str(member) + " " + text
            json.dump(fulltext, f, indent=4)
        embed = discord.Embed(
        title="Message from: "+str(ctx.author),
        color=ctx.author.color,
        description=text
        )
        await channel.send(embed=embed)
        
    @commands.command()
    #considering the abuse possibilities of this if ever deployed, consider implementing a permission management
    # -> above should be done in database construction <<<<- why old me, why did you think this, thats not a good idea
    @has_permissions(manage_messages=True) #obligatory decision for what is considered 'an admin'
    async def anondm(self,ctx,member:discord.Member,*,text):
        """DM a user Anonymously."""
        if member.dm_channel == None:
            channel = await member.create_dm()
        channel = member.dm_channel
        json_file_path = "/chatlog.json"
        with open(json_file_path, 'r') as f:
            fulltext = json.load(f)
        with open(json_file_path, 'w') as f:
            fulltext[str(ctx.message.id)] = "Anon Message by: " + str(member) + " " + text
            json.dump(fulltext, f, indent=4)
        embed = discord.Embed(
        title="Anonymous Message",
        color=ctx.author.color,
        description=text
        )
        await channel.send(embed=embed)
            
            
    @commands.command()
    async def add(self,ctx, left: int, right: int):
        """Adds two numbers together."""
        await ctx.send(left + right)
        
    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self,ctx, *choices: str):
        """Chooses between multiple choices."""
        if '@everyone' in choices or '@here' in choices:
            return
        await ctx.send(random.choice(choices))
        
    @commands.command()
    async def repeat(self,ctx, times: int, content='repeating...', interval = 1):
        """Repeats a message multiple times in a given interval."""
        if '@everyone' in content or '@here' in content or '@&' in content: #fixed 'mass role ping' issue
            return
        for i in range(times):
            print(str(content))
            await ctx.send(content)
            await asyncio.sleep(interval)
        await ctx.send("Repeat Done")
        await asyncio.sleep(1)
        await ctx.channel.purge(limit=1)
        
    @commands.command(name='8ball')
    async def ball8(self,ctx, *, question):
        """Ask a question and receive an ambigious answer."""
        responses = [
                "It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]
        embed = discord.Embed(
        title="You asked: "+question,
        description="The ball says: "+str(random.choice(responses))
        )
        await ctx.send(embed=embed)
        

