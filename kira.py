# Discord Bot Project 
# Section - Main File
# The General runner of this artpiece.
# Includes anything not being able to be put in a seperate file.
# 'Documentation' can be found in: kira_documentation.py
import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import has_permissions
import asyncio
import datetime
import traceback
try:
    import simplejson as json
except ImportError:
    import json
import kira_music
import kira_tmw
import kira_moderational
import kira_botsetup
import kira_imagesapi
import kira_interactions
import kira_other
import kira_token
import kira_polls
import kira_encryption
import kira_economy
description = '''
Bot usage is intended to simplify and/or automate certain actions.
'''

intents = discord.Intents.default()
intents.members = True

json_file_path = "/database.json"
json_file_path_2 = "/presence.json"

def get_prefix(client, message):
    try:
        with open(json_file_path, 'r') as f:
            prefixes = json.load(f)
        return prefixes[str(message.guild.id)]
    except:
        return "?"
def get_presence(client, message):
    with open(json_file_path_2, 'r') as f:
        presences = json.load(f)
    return presences[str(message.guild.id)]
    
snipe_message_content = None
snipe_message_author = None
snipe_message_id = None

bot = commands.Bot(command_prefix=get_prefix, description=description, intents=intents)
client = discord.Client()

#this neeeds to bee here, duee to the 'bot.change_presence' command, which just does not work in other files
@bot.command()
@has_permissions(administrator=True)
async def changepresence(ctx, *, presence):
    """change presence"""
    json_file_path_2 = "/presence.json"
    with open(json_file_path_2, 'r') as f:
        presences = json.load(f)

    presences[str(ctx.guild.id)] = presence

    with open(json_file_path_2, 'w') as f:
        json.dump(presences, f, indent=4)##
        
    game = discord.Game(presence)
    await bot.change_presence(status=discord.Status.idle, activity=game)#
    await ctx.send(f'Presence changed to: {presence}')
    
@bot.event
async def on_guild_join(guild):
    #prefixes
    with open(json_file_path, 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = '?'
    with open(json_file_path, 'w') as f:
        json.dump(prefixes, f, indent=4)
    #presences
    with open(json_file_path_2, 'r') as f:
        presences = json.load(f)
    presences[str(guild.id)] = 'pfft pfft'
    with open(json_file_path_2, 'w') as f:
        json.dump(presences, f, indent=4)

@bot.event
async def on_guild_remove(guild):
    #prefixes
    with open(json_file_path, 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open(json_file_path, 'w') as f:
        json.dump(prefixes, f, indent=4)
    #presences
    with open(json_file_path_2, 'r') as f:
        presences = json.load(f)
    presences.pop(str(guild.id))
    with open(json_file_path_2, 'w') as f:
        json.dump(presences, f, indent=4)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    game = discord.Game("h")
    await bot.change_presence(status=discord.Status.idle, activity=game)
    
#@bot.event
#async def on_message(message):
   # if message.author == bot.user:
   #     return
    # this is an extremely ugly implementation, will likely hinder performance if scaled, but given my scenario of this bot being used at most in 3 servers, thats fine.
    # to explain, it updates the presence every time a new message is sent.
    # DO NOT UNCOMMEENT BELOW
    # THIS F~CKER WILL BREAK THE ENTIRE BOT
    # I DO NOT KNOW HOW, I DO NOT KNOW WHY, BUT THIS IS THE SOURCE OF THE ISSUE
    # ON_MESSAGE CANNOT BE TRUSTED
    
    # i have attempted to fix this
    # it did not work
    # i hate on_message
    # :(
    
   # game = discord.Game("h")
   # if str(get_prefix) in message.content:
   #     return
  #  else:
   #     game = discord.Game(get_presence(client,message))
  #      await bot.change_presence(status=discord.Status.idle, activity=game)
   # if bot.user.mentioned_in(message):
   #     await message.channel.send(f'My prefix is: {bot.command_prefix}')



@bot.event
async def on_message_delete(message):

    global snipe_message_content
    global snipe_message_author
    global snipe_message_id

    snipe_message_content = message.content
    snipe_message_author = message.author.id
    snipe_message_id = message.id
    await asyncio.sleep(60)

    if message.id == snipe_message_id:
        snipe_message_author = None
        snipe_message_content = None
        snipe_message_id = None

#while this would be better to have in a different category, due to the cooperation with above condition, it requires it being here at this time
@bot.command()
async def snipe(message):
    if snipe_message_content==None:
        await message.channel.send("Theres nothing to snipe.")
    else:
        embed = discord.Embed(description=f"{snipe_message_content}")
        embed.set_footer(text=f"Said by {message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
        embed.set_author(name= f"poof poof sniped it:")
        await message.channel.send(embed=embed)
        return
# it is to note, that welcome/goodbye works with the server-side assigned welcome channel
@bot.event
async def on_member_join(member):
    """Welcoming code to welcome upon joining."""
    guild = member.guild
    if guild.system_channel is not None:
        to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
        try:
            await guild.system_channel.send(to_send)
        except:
            await guild.system_channel.send("Couldn't send message, sorry!")
@bot.event
async def on_member_remove(member):
    """Opposite to above, cya'ing a leaving member."""
    guild = member.guild
    if guild.system_channel is not None:
        to_send = 'cya {0.mention}!'.format(member, guild)
        try:
            await guild.system_channel.send(to_send)
        except:
            await guild.system_channel.send("Couldn't send message, sorry!")
        
@bot.event
async def on_invite_create(invite):
    """Note down the creation of each invite, by whom they were done, and when"""
    guild = bot.get_guild(408477219611213836)
    to_send = '{0} created {1} at {2}'.format(invite.inviter,invite,invite.created_at)
    try:
        await guild.system_channel.send(to_send)
    except:
        await guild.system_channel.send("Couldn't send message, sorry!")

@bot.event
async def on_reaction_add(reaction, user):
    """Audit log to check reactions on messages"""
    guild = bot.get_guild(408477219611213836)
    to_send = '{0} reacted to {1} with {2}'.format(user,reaction.message.id,reaction)
    try:
        await guild.system_channel.send(to_send)
    except:
        await guild.system_channel.send("Couldn't send message, sorry!")

@bot.event
async def on_reaction_remove(reaction, user):
    """Audit log to check removed reactions on messages"""
    guild = bot.get_guild(408477219611213836)
    to_send = '{0} unreacted to {1} with {2}'.format(user,reaction.message.id,reaction)
    try:
        await guild.system_channel.send(to_send)
    except:
        await guild.system_channel.send("Couldn't send message, sorry!")

@bot.event
async def on_error(event, *args, **kwargs):
    embed = discord.Embed(title=':x: Event Error', colour=0xe74c3c)
    embed.add_field(name='Event', value=event)
    embed.description = '```py\n%s\n```' % traceback.format_exc()
    embed.timestamp = datetime.datetime.utcnow()
    await bot.AppInfo.owner.send(embed=embed)


#Categories used below to organize the Help Command and implement other-files.
bot.add_cog(kira_moderational.Moderational(bot))
bot.add_cog(kira_botsetup.BotSetup(bot))
bot.add_cog(kira_tmw.TMW(bot))
bot.add_cog(kira_music.Music(bot))
bot.add_cog(kira_other.Other(bot))
bot.add_cog(kira_imagesapi.imagesapi(bot))
bot.add_cog(kira_interactions.interactapi(bot))
bot.add_cog(kira_polls.Polls(bot))
bot.add_cog(kira_encryption.encryption(bot))
#bot.add_cog(kira_errorhandler.CommandErrorHandler(bot)) this never worked, so the file was deleted
bot.add_cog(kira_economy.Economy(bot))
#If I ever decide to use a public version control, it is ***very*** essential to hide the token.
bot.run(kira_token.token)
