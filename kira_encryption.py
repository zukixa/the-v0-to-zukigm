# Discord Bot Project 
# Section - Encryption
# Encrypt and decrypt messages at one's own convenience.
# Note: Hopefully expanded to more ciphers, and something similar to
# https://www.boxentriq.com/code-breaking/cipher-identifier
import discord
from discord.ext import commands
import sr_api
import aiohttp
client = sr_api.Client()
#overall possibility to expand to secret/unsecret methods, where one would show both messages[current], and a future version would only post the encrypted version, and keep out everything else.
class encryption(commands.Cog):
    # tried to do unicode fun, opted instead for this monstrosity
    # previous iterations of a similar idea resulted in the value of h to baloon extremely in size
    # good example: Base10: V Funny: w5NddcOTXXQ=   -- this is the case already with the CURRENT system.
    @commands.command()
    async def to_fun(self,ctx,text:str):
        """encode text to funny"""
        h = await client.encode_binary(text)
        h = await client.decode_base64(h)
        h = await client.encode_base64(h)
        embed = discord.Embed(title="To Funny Encryption")
        embed.add_field(name="Base10:",value=text)
        embed.add_field(name="Funny:",value=h)
        await ctx.send(embed=embed)
        # currently the part below is unable to actually decipher a message that has been launched from above
        # that is quite surprising but i have no idea how to fix such
    @commands.command()
    async def from_fun(self,ctx,text:str):
        """encode text to funny"""
        h = await client.decode_base64(text)
        print(h)
        h = await client.encode_base64(h)
        print(h)
        h = await client.encode_binary(h)
        print(h)
        h = await client.decode_binary(h)
        embed = discord.Embed(title="From Funny Encryption")
        embed.add_field(name="Funny:",value=text)
        embed.add_field(name="Base 10:",value=h)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def to_binary(self,ctx,text):
        """Encode text to Binary."""
        result = await client.encode_binary(text)
        embed = discord.Embed(
            title="To Binary Encryption"
            )
        embed.add_field(name="Base10:",value=text)
        embed.add_field(name="Binary:",value=result)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def from_binary(self,ctx,text):
        """Decode text from Binary."""
        result = await client.decode_binary(text)
        embed = discord.Embed(
            title="From Binary Encryption"
            )
        embed.add_field(name="Binary:",value=text)
        embed.add_field(name="Base10:",value=result)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def to_base64(self,ctx,text):
        """Encode text to Base64."""
        result = await client.encode_base64(text)
        embed = discord.Embed(
            title="To Base64 Encryption"
            )
        embed.add_field(name="Base10:",value=text)
        embed.add_field(name="Base64:",value=result)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def from_base64(self,ctx,text):
        """Decode text from Base64."""
        result = await client.decode_base64(text)
        embed = discord.Embed(
            title="From Base64 Encryption"
            )
        embed.add_field(name="Base64:",value=text)
        embed.add_field(name="Base10:",value=result)
        await ctx.send(embed=embed)


