# Discord Bot Project 
# Section - TMW
# Commands based on functionality with TMW.
# Includes all commands specified for usage on TMW and other RP Servers.
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import emoji
import random
import asyncio
import time
import datetime
from datetime import date, timedelta
# wikipedia was moved to kira_other
#ooc base matcher
match = ['[']
class TMW(commands.Cog):
    rptime = None
    @commands.command()
    async def roll(self,ctx, dice: str,Add1=0,Add2=0,Add3=0,Add4=0):
        """Rolls a dice in NdN format. Compatible with up to 4 modifiers."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return
        modifiers = Add1+Add2+Add3+Add4;
        result = ', '.join(str(random.randint(1, limit+modifiers)) for r in range(rolls))
        embed = discord.Embed(
            title="Your roll out of "+str(limit),
            description="Sum of Modifiers: "+str(modifiers)
        )
        embed.add_field(name="Your Result:",value=str(result),inline=True)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def splitroll(self,ctx, percent: int, parts: int):
        """Split any number into any number of parts, randomly."""
        result = [0] * parts
        remainder = percent
        for i in range(0,parts):
            if (i == 0 and parts == 1) or i == parts-1:
                result[i] = remainder
                break
            elif (i == 0):
                result[i] = random.randrange(0,remainder)
                remainder = remainder - result[i]
            else:
                result[i] = random.randrange(0,remainder)
                remainder = remainder - result[i]
        embed = discord.Embed(
            title=f'Your result from {percent}% in {parts} Parts.'
        )
        for i in range(0,len(result)):
            embed.add_field(name=f'Object {str(i)} - {result[i]}%',value='\u200b')
        
        await ctx.send(embed=embed)
    @commands.command()
    async def rolecheck(self,ctx, str: str):
        """List all roles which are either taken, or free"""
        result = ""
        if str == "taken" or str == "free":
            for r in ctx.guild.roles:
                if str == "taken":
                    if r.members:
                        if r.name != "@everyone":
                            result += (r.name + ', ')
                if str == "free":
                    if not r.members:
                        if r.name != "@everyone":
                            result += (r.name + ', ')
            
            await ctx.send(result)
        else:
            await ctx.send("taken or free roles?")
    @commands.command()
    async def randomrole(self,ctx):
        """post random free role"""
        freeroles = []
        for r in ctx.guild.roles:
            if not r.members:
                freeroles.append(r)
        try:
            result = freeroles[random.randint(0, len(freeroles))]
            await ctx.send(result)
        except:
            await ctx.send('All roles are taken.')
        
        
    @commands.command(name='say')
    async def cpost(self,ctx, newname:str, *, msg:str):
    # an old system included changing the bots nickname for this
    # but now the nickname bug (old nicknames stay with old messages after changing name)
    # was fixed, so the system had to be redesigned
        """Make the bot say something for you!"""
        try:
            await ctx.message.delete()
            await ctx.send(f'__**{newname}** said:__\n{msg}')
        #oldname = ctx.bot.user.name
        #try:
        #    await ctx.message.delete()
        #    await ctx.guild.me.edit(nick=newname)
         #   await ctx.send(msg)
         #   await asyncio.sleep(2)
         #   await ctx.guild.me.edit(nick=oldname)
        except:
            await ctx.send('Say failed to work. Format: nickname, message')
            
    @commands.command()
    @has_permissions(manage_messages=True)
    async def setOOC(self,ctx,string):
        """Adds more stuff to the ooc filter"""
        global match
        match.append(string)
        await ctx.send(f'{string} has been added to the OOC filter')
        
    @commands.command()
    @has_permissions(manage_messages=True)
    async def ooc(self,ctx):
        """Purges OOC by TMW convention."""
        async for message in ctx.channel.history():
            global match
            counter = 0
            # expand this to include more 'conventional characters', possibly customizable in the future
            list =['🇦🇫','🇦🇽','🇦🇱','🇩🇿','🇦🇸','🇦🇩','🇦🇴','🇦🇮','🇦🇶','🇦🇬','🇦🇷','🇦🇲','🇦🇼','🇦🇨','🇦🇺','🇦🇹','🇦🇿','🇧🇸','🇧🇭','🇧🇩','🇧🇧','🇧🇾','🇧🇪','🇧🇿','🇧🇯','🇧🇲','🇧🇹','🇧🇴','🇧🇦','🇧🇼','🇧🇻','🇧🇷','🇮🇴','🇻🇬','🇧🇳','🇧🇬','🇧🇫','🇧🇮','🇰🇭','🇨🇲','🇨🇦','🇮🇨','🇨🇻','🇧🇶','🇰🇾','🇨🇫','🇪🇦','🇹🇩','🇨🇱','🇨🇳','🇨🇽','🇨🇵','🇨🇨','🇨🇴','🇰🇲','🇨🇬','🇨🇩','🇨🇰','🇨🇷','🇨🇮','🇭🇷','🇨🇺','🇨🇼','🇨🇾','🇨🇿','🇩🇰','🇩🇬','🇩🇯','🇩🇲','🇩🇴','🇪🇨','🇪🇬','🇸🇻','🇬🇶','🇪🇷','🇪🇪','🇪🇹','🇪🇺','🇫🇰','🇫🇴','🇫🇯','🇫🇮','🇫🇷','🇬🇫','🇵🇫','🇹🇫','🇬🇦','🇬🇲','🇬🇪','🇩🇪','🇬🇭','🇬🇮','🇬🇷','🇬🇱','🇬🇩','🇬🇵','🇬🇺','🇬🇹','🇬🇬','🇬🇳','🇬🇼','🇬🇾','🇭🇹','🇭🇲','🇭🇳','🇭🇰','🇭🇺','🇮🇸','🇮🇳','🇮🇩','🇮🇷','🇮🇶','🇮🇪','🇮🇲','🇮🇱','🇮🇹','🇯🇲','🇯🇵','🇯🇪','🇯🇴','🇰🇿','🇰🇪','🇰🇮','🇽🇰','🇰🇼','🇰🇬','🇱🇦','🇱🇻','🇱🇧','🇱🇸','🇱🇷','🇱🇾','🇱🇮','🇱🇹','🇱🇺','🇲🇴','🇲🇰','🇲🇬','🇲🇼','🇲🇾','🇲🇻','🇲🇱','🇲🇹','🇲🇭','🇲🇶','🇲🇷','🇲🇺','🇾🇹','🇲🇽','🇫🇲','🇲🇩','🇲🇨','🇲🇳','🇲🇪','🇲🇸','🇲🇦','🇲🇿','🇲🇲','🇳🇦','🇳🇷','🇳🇵','🇳🇱','🇳🇨','🇳🇿','🇳🇮','🇳🇪','🇳🇬','🇳🇺','🇳🇫','🇲🇵','🇰🇵','🇳🇴','🇴🇲','🇵🇰','🇵🇼','🇵🇸','🇵🇦','🇵🇬','🇵🇾','🇵🇪','🇵🇭','🇵🇳','🇵🇱','🇵🇹','🇵🇷','🇶🇦','🇷🇪','🇷🇴','🇷🇺','🇷🇼','🇼🇸','🇸🇲','🇸🇹','🇸🇦','🇸🇳','🇷🇸','🇸🇨','🇸🇱','🇸🇬','🇸🇽','🇸🇰','🇸🇮','🇸🇧','🇸🇴','🇿🇦','🇬🇸','🇰🇷','🇸🇸','🇪🇸','🇱🇰','🇧🇱','🇸🇭','🇰🇳','🇱🇨','🇲🇫','🇵🇲','🇻🇨','🇸🇩','🇸🇷','🇸🇯','🇸🇿','🇸🇪','🇨🇭','🇸🇾','🇹🇼','🇹🇯','🇹🇿','🇹🇭','🇹🇱','🇹🇬','🇹🇰','🇹🇴','🇹🇹','🇹🇦','🇹🇳','🇹🇷','🇹🇲','🇹🇨','🇹🇻','🇺🇬','🇺🇦','🇦🇪','🇬🇧','🏴󠁧󠁢󠁥󠁮󠁧󠁿','🏴󠁧󠁢󠁳󠁣󠁴󠁿','🏴󠁧󠁢󠁷󠁬󠁳󠁿','🇺🇸','🇺🇾','🇺🇲','🇻🇮','🇺🇿','🇻🇺','🇻🇦','🇻🇪','🇻🇳','🇼🇫','🇪🇭','🇾🇪','🇿🇲','🇿🇼']
            custom_emojis = ctx.guild.emojis
            # while it may be a good idea to replace this with some form of file, given that I had to differentiate between two types of ' , it may not be a good idea.
            try:
                for m in match:
                    if m not in message.content:
                        counter += 1
                for e in custom_emojis:
                    if str(e) not in message.content:
                        counter += 1
                for f in list:
                    if f not in message.content:
                       counter += 1
                if counter == len(match) + len(list) + len(custom_emojis):
                    await message.delete()
                    counter = 0
            except Exception:
                continue #this is extremely ugly but required for messages that have been deleted already
        await ctx.send(f'Cleared by <@{ctx.author.id}>')
        await asyncio.sleep(2)
        await ctx.channel.purge(limit=1)
    
    #possible use is 're-adding' roles pre-jailing, besides that - works as intended.
    @commands.command(pass_context=True)
    @has_permissions(manage_messages=True) #theres no 'mod' permission, which doesnt include 'administrator' which is too much, so this is likely the best middle ground
    async def jail(self,ctx, usr: discord.Member):
        """Similar to a mute, but it removes all roles of a user and adds a role."""
        role = discord.utils.get(ctx.guild.roles, name="jail")
        if role in usr.roles:
            await usr.remove_roles(role)
            await ctx.send(f'User has been **unjailed.**')
        else:
            await usr.add_roles(role)
            for role in ctx.guild.roles:
                if role.name != "jail":
                    try:
                        await usr.remove_roles(role)
                    except:
                        continue
            await ctx.send(f'User has been **jailed.**')
    
    # bp specific, but tmw could use this too
    @commands.command()
    @has_permissions(manage_messages=True) # consider above explanation similar to why it's here again
    async def pending(self,ctx, usr: discord.Member):
        """Remove all roles and give a role called Pending"""
        for role in usr.roles:
            try:
                await usr.remove_roles(role)
            except:
                pass #oh well
        pending = discord.utils.get(ctx.guild.roles, name="pending")
        await usr.add_roles(pending)
        await ctx.send(f'User has been sent to **pending.**')
    
            
    @commands.command()
    async def reminder(self, ctx, time, *, reminder):
        """tell the bot to remind you off something!"""
        user = ctx.message.author
        embed = discord.Embed(color=0x55a7f7, timestamp=datetime.datetime.now())
        seconds = 0
        if reminder is None:
            embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.') # Error message
        if time.lower().endswith("d"):
            seconds += int(time[:-1]) * 60 * 60 * 24
            counter = f"{seconds // 60 // 60 // 24} days"
        if time.lower().endswith("h"):
            seconds += int(time[:-1]) * 60 * 60
            counter = f"{seconds // 60 // 60} hours"
        elif time.lower().endswith("m"):
            seconds += int(time[:-1]) * 60
            counter = f"{seconds // 60} minutes"
        elif time.lower().endswith("s"):
            seconds += int(time[:-1])
            counter = f"{seconds} seconds"
        if seconds == 0:
            embed.add_field(name='Warning',
                            value='Please specify a proper duration, send `reminder_help` for more information.')
        elif seconds < 60:
            embed.add_field(name='Warning',
                            value='You have specified a too short duration!\nMinimum duration is 1 minute.')
        elif seconds > 7776000:
            embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
        else:
            await ctx.send(f"Alright, I will remind you about {reminder} in {counter}.")
            await asyncio.sleep(seconds)
            await ctx.send(f"Hi, you asked me to remind you about {reminder} {counter} ago.")
            return
        await ctx.send(embed=embed)
    #time calculation
    #in future, expand to use datetime
    @commands.command()
    @has_permissions(administrator=True)
    async def settime(self, ctx, month:int, year:int, interval:int, frequency:int):
        """Set a RP time counter, with a (M)M/YYYY input, includes time passing interval in seconds and frequency of update option"""
        global rptime
        rptime = datetime.datetime(year, month, 1, 0, 0, 0, 0)
        #aribitrary time of 10 years in seconds
        for i in range(0,31536000):
            await ctx.send(rptime)
            for i in range(0,frequency):
                rptime += timedelta(seconds=interval/frequency)
                await asyncio.sleep(1)
    @commands.command()
    async def gettime(self,ctx):
        """Get current IRP time, uses settime's method."""
        await ctx.send("Current Time is: " + str(rptime))
        
    @commands.command()
    async def getidea(self,ctx):
        """Get random idea of entity to play"""
        list =['🇦🇫','🇦🇽','🇦🇱','🇩🇿','🇦🇸','🇦🇩','🇦🇴','🇦🇮','🇦🇶','🇦🇬','🇦🇷','🇦🇲','🇦🇼','🇦🇨','🇦🇺','🇦🇹','🇦🇿','🇧🇸','🇧🇭','🇧🇩','🇧🇧','🇧🇾','🇧🇪','🇧🇿','🇧🇯','🇧🇲','🇧🇹','🇧🇴','🇧🇦','🇧🇼','🇧🇻','🇧🇷','🇮🇴','🇻🇬','🇧🇳','🇧🇬','🇧🇫','🇧🇮','🇰🇭','🇨🇲','🇨🇦','🇮🇨','🇨🇻','🇧🇶','🇰🇾','🇨🇫','🇪🇦','🇹🇩','🇨🇱','🇨🇳','🇨🇽','🇨🇵','🇨🇨','🇨🇴','🇰🇲','🇨🇬','🇨🇩','🇨🇰','🇨🇷','🇨🇮','🇭🇷','🇨🇺','🇨🇼','🇨🇾','🇨🇿','🇩🇰','🇩🇬','🇩🇯','🇩🇲','🇩🇴','🇪🇨','🇪🇬','🇸🇻','🇬🇶','🇪🇷','🇪🇪','🇪🇹','🇪🇺','🇫🇰','🇫🇴','🇫🇯','🇫🇮','🇫🇷','🇬🇫','🇵🇫','🇹🇫','🇬🇦','🇬🇲','🇬🇪','🇩🇪','🇬🇭','🇬🇮','🇬🇷','🇬🇱','🇬🇩','🇬🇵','🇬🇺','🇬🇹','🇬🇬','🇬🇳','🇬🇼','🇬🇾','🇭🇹','🇭🇲','🇭🇳','🇭🇰','🇭🇺','🇮🇸','🇮🇳','🇮🇩','🇮🇷','🇮🇶','🇮🇪','🇮🇲','🇮🇱','🇮🇹','🇯🇲','🇯🇵','🇯🇪','🇯🇴','🇰🇿','🇰🇪','🇰🇮','🇽🇰','🇰🇼','🇰🇬','🇱🇦','🇱🇻','🇱🇧','🇱🇸','🇱🇷','🇱🇾','🇱🇮','🇱🇹','🇱🇺','🇲🇴','🇲🇰','🇲🇬','🇲🇼','🇲🇾','🇲🇻','🇲🇱','🇲🇹','🇲🇭','🇲🇶','🇲🇷','🇲🇺','🇾🇹','🇲🇽','🇫🇲','🇲🇩','🇲🇨','🇲🇳','🇲🇪','🇲🇸','🇲🇦','🇲🇿','🇲🇲','🇳🇦','🇳🇷','🇳🇵','🇳🇱','🇳🇨','🇳🇿','🇳🇮','🇳🇪','🇳🇬','🇳🇺','🇳🇫','🇲🇵','🇰🇵','🇳🇴','🇴🇲','🇵🇰','🇵🇼','🇵🇸','🇵🇦','🇵🇬','🇵🇾','🇵🇪','🇵🇭','🇵🇳','🇵🇱','🇵🇹','🇵🇷','🇶🇦','🇷🇪','🇷🇴','🇷🇺','🇷🇼','🇼🇸','🇸🇲','🇸🇹','🇸🇦','🇸🇳','🇷🇸','🇸🇨','🇸🇱','🇸🇬','🇸🇽','🇸🇰','🇸🇮','🇸🇧','🇸🇴','🇿🇦','🇬🇸','🇰🇷','🇸🇸','🇪🇸','🇱🇰','🇧🇱','🇸🇭','🇰🇳','🇱🇨','🇲🇫','🇵🇲','🇻🇨','🇸🇩','🇸🇷','🇸🇯','🇸🇿','🇸🇪','🇨🇭','🇸🇾','🇹🇼','🇹🇯','🇹🇿','🇹🇭','🇹🇱','🇹🇬','🇹🇰','🇹🇴','🇹🇹','🇹🇦','🇹🇳','🇹🇷','🇹🇲','🇹🇨','🇹🇻','🇺🇬','🇺🇦','🇦🇪','🇬🇧','🏴󠁧󠁢󠁥󠁮󠁧󠁿','🏴󠁧󠁢󠁳󠁣󠁴󠁿','🏴󠁧󠁢󠁷󠁬󠁳󠁿','🇺🇸','🇺🇾','🇺🇲','🇻🇮','🇺🇿','🇻🇺','🇻🇦','🇻🇪','🇻🇳','🇼🇫','🇪🇭','🇾🇪','🇿🇲','🇿🇼']
        await ctx.send(list[random.randint(0,len(list))])
        
    @commands.command()
    async def whois(self, ctx, *, name:str):
        """Check who holds what role."""
        response = ""
        try:
            role = discord.utils.get(ctx.guild.roles, name=name)
            for member in role.members:
                response += member.mention + ", "
        
            if response is not None:
                await ctx.send(response)
            else:
                await ctx.send(f"No one is {role}")
        except Exception:
            await ctx.send("Either the role doesn't exist, or you misspelled it.")
