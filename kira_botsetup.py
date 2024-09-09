# Discord Bot Project 
# Section - BotSetup
# General commands based on changing stuff for the bot.
# Includes command(s) based on editing bot-related aspects.
# Note: In the future, this will likely be the sight of json databases and custom command haven, as that's something out there still for me.
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
try:
    import simplejson as json
except ImportError:
    import json
    
class BotSetup(commands.Cog):
    @commands.command(pass_context=True)
    @has_permissions(administrator=True) #ensure that only administrators can use this command
    async def setprefix(self,ctx, prefix):
        """change prefix"""
        json_file_path = "/database.json"
        with open(json_file_path, 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open(json_file_path, 'w') as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f'Prefix changed to: {prefix}')
        
    @commands.command(pass_context=True)
    # this also will need that "automatic continuation post setup so that its properly working"
    async def auditSetup(self,ctx):
        """audit log setup"""
        s = ""
        async for entry in ctx.guild.audit_logs(limit=10, oldest_first=True):
            s += ('{0.user} did {0.action} to {0.target}\n'.format(entry))
        await ctx.send(s);

