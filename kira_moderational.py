# Discord Bot Project 
# Section - Moderational
# General commands based on Moderational Tasks.
# Includes all commands known for it, such as kick/ban and mute/serverinfo
# Note: Be 1000% certain that permissions are correctly set before deploying outside of test server.
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio

class Moderational(commands.Cog):

    @commands.command()
    async def userinfo(self,ctx,user:discord.User):
        """Note relevant user info into an embed, similar to serverinfo"""
        embed = discord.Embed()
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.add_field(name="Info:",value="ID: " + str(user.id) + "\nCreated: " + str(user.created_at))
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self,ctx, msg: str=None):
        """Fetch Server Info - comprehensive"""
        # this works, for now --- future me: make it actually look nice --- me from the future: no
        # display all custom emojis of server
        if msg:
            server, found = ctx.find_server(msg)
            if not found:
                return await ctx.send(server)
        else:
            server = ctx.guild
            emojis = [str(x) for x in server.emojis]
        
        embed = discord.Embed(
        title="Server Info of " + ctx.guild.name,
        description="A short, yet fullfilling summary."
        )
        embed.add_field(name="IDs",value="Owner ID: "+str(ctx.guild.owner_id)+"\nServer ID: "+str(ctx.guild.id))
        embed.add_field(name="Server Specialities:", value="Region: "+str(ctx.guild.region)+"\nDefault Notifications: "+str(ctx.guild.default_notifications)+"\nMax Members: "+str(ctx.guild.max_members)+"\nMax Stream Users: "+str(ctx.guild.max_video_channel_users)+"\nEmotes: "+str(emojis))
        embed.add_field(name="Server Security:", value="Verification Level: "+str(ctx.guild.verification_level)+"\nContent Filter: "+str(ctx.guild.explicit_content_filter)+"\n2FA: "+str(bool(ctx.guild.mfa_level)), inline=False)
        embed.add_field(name="Server Nitro Stats:", value="Server Nitro Tier: "+str(ctx.guild.premium_tier)+"\nNitro Boosters: "+str(ctx.guild.premium_subscription_count))
        embed.add_field(name="Server Channels:", value="Text Channel Amount: "+str(len(ctx.guild.text_channels))+"\nVoice Channel Amount: "+str(len(ctx.guild.voice_channels))+"\nCategories Amount: "+str(len(ctx.guild.categories)))
        # send the embed out into infinity
        await ctx.send(embed=embed)

    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """The ability to permanently remove a player from your server."""
        if member.dm_channel == None:
            await member.create_dm()
        await member.dm_channel.send(content=f"You have been banned from {ctx.guild} by {ctx.message.author}\nReason: {reason} ")
        try:
            await member.ban(reason=reason)
        except:
            await ctx.send(f'Unable to ban {member}, sorry!')
        await ctx.send(f'{member} has been **banned** from this establishment')
     
    #as showcased in comment later down below, current discord does not allow this - unless *weird* methods are used
    @commands.command()
    @has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        """The ability to undo the permanent removal of a player."""
        banned_users = await ctx.guild.bans()
        # also, add possibility to use @ tag directly instead of spelled out user#0456
        member_name, member_discriminator = member.split('#')
        
        for ban_entry in banned_users:
            user = ban_entry.user
            tuser = user
            if((user.name, user.discriminator) == (member_name, member_discriminator)):
                try:
                    await ctx.guild.unban(user)
                    await ctx.send(f'**Unbanned** {user.name}#{user.discriminator}')
                    #await tuser.dm_channel.send(content=f"You have been unbanned from {ctx.guild} by {ctx.message.author}")
                    #await Moderational.invite(self,ctx,tuser)
                    #this is likely not possible due to discord limitations, but if in the future working, this will dm the user with an invite when unbanned
                except:
                    await ctx.send(f'Unable to unban {user}, sorry!')
    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self,ctx, member: discord.Member, *, reason=None):
        """The ability to remove a player from your server, once per usage."""
        if member.dm_channel == None:
            await member.create_dm()
        await member.dm_channel.send(content=f"You have been kicked from {ctx.guild} by {ctx.message.author}\nReason: {reason} ")
        await Moderational.invite(self,ctx,member)
        try:
            await member.kick(reason=reason)
            await ctx.send(f'{member} has been **kicked** from this establishment')
        except:
            await ctx.send(f'Unable to kick {member}, sorry!')
    @commands.command()
    @has_permissions(manage_messages=True)
    async def purge(self,ctx, x:int):
        """Deletes X messages in a channel."""
        await ctx.channel.purge(limit=x)
        await ctx.send('Cleared by <@{.author.id}>'.format(ctx))
        await asyncio.sleep(2)
        await ctx.channel.purge(limit=1)
        
    @commands.command()
    @has_permissions(create_instant_invite=True)
    async def invite(self, ctx, member: discord.Member):
        """Send an Invite to a User's DMs to simplify invite creation."""
        if member.dm_channel == None:
            channel = await member.create_dm()
        channel = member.dm_channel
        link = await ctx.channel.create_invite(max_age = 300)
        await channel.send(link)
