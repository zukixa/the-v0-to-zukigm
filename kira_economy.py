# this stuff's gonna get ambitious
# the current implementation is for testing purposes.

import collections
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import random
#dicts thatll be moved to json once the project is more existing than currently
who_plays_what = {}
list_of_gdps = {}
list_of_gdp_growths = {}
# note, these 3 below can be just universally agreed to be simply for any non-nation entity
list_of_companies = {}
list_of_companies_operational_cost = {}
list_of_companies_operational_revenue = {}

class Economy(commands.Cog):

    # another fairly ambitious command, but it ended up working unlike leaderboard grr
    @commands.command(pass_context=True)
    async def pay(self,ctx,destination: discord.User,money):
        """The method that allows you to pay others money (not nations, due to lack of budget)"""
        global list_of_companies
        global who_plays_what
        list_of_companies[who_plays_what.get(destination.id)] = int(list_of_companies[who_plays_what.get(destination.id)]) + int(money)
        list_of_companies[who_plays_what.get(ctx.author.id)] = int(list_of_companies[who_plays_what.get(ctx.author.id)]) - int(money)
        await ctx.send(f"{money}$ paid to {destination} successfully!")
    
    @commands.command(pass_context=True)
    async def setGDP(self,ctx, country, gdp):
        """Setter for GDP values in global"""
        global list_of_gdps
        list_of_gdps[country] = gdp;
        await ctx.send(f"{country}'s GDP has been set to {gdp}$")
        
    @commands.command(pass_context=True)
    async def getGDP(self,ctx, country):
        """Acccessor for GDP values in global"""
        global list_of_gdps
        await ctx.send(list_of_gdps[country] + "$");
        
    @commands.command(pass_context=True)
    async def listGDP(self,ctx):
        """List all GDP's listed in the storage at this time."""
        global list_of_gdps
        answer = ""
        x = list_of_gdps.keys()
        for x in list_of_gdps:
            answer += x + f" = {list_of_gdps[x]}$" + "\n"
        await ctx.send(answer)
        
    @commands.command(pass_context=True)
    async def setGrowth(self,ctx, country, growth):
        """Setter for GDP growth values in global"""
        global list_of_gdp_growths
        list_of_gdp_growths[country] = growth;
        await ctx.send(f"{country}'s GDP Growth has been set to {growth}%")
        
    @commands.command(pass_context=True)
    async def getGrowth(self,ctx, country):
        """Acccessor for GDP growth values in global"""
        global list_of_gdp_growths
        await ctx.send(list_of_gdp_growths[country] + "%");
        
    @commands.command(pass_context=True)
    async def listGrowth(self,ctx):
        """List all GDP Growth's listed in the storage at this time."""
        global list_of_gdp_growths
        answer = ""
        x = list_of_gdp_growths.keys()
        for x in list_of_gdp_growths:
            answer += x + f" = {list_of_gdp_growths[x]}%" + "\n"
        await ctx.send(answer)
 
    @commands.command(pass_context=True)
    @has_permissions(administrator=True)
    async def setCountry(self, ctx, user: discord.User, name, gdp, growth):
        """Combines the 2 setters above into a full one, may have good use."""
        global list_of_gdps
        global list_of_gdp_growths
        global who_plays_what
        who_plays_what[user.id] = name
        list_of_gdps[name] = gdp
        list_of_gdp_growths[name] = growth
        await ctx.send(f"{name} has been set to {gdp}$ GDP with {growth}% growth.")
        
    @commands.command(pass_context=True)
    @has_permissions(administrator=True)
    # may need additional setters to  edit last 3 arguments specifically
    # may honestly even become just a single get/set command with "the specific thing to edit" as a parameter
    # additional consideration to generalize this, as this system honestly applies to anything non-nation
    async def setCompany(self, ctx, user: discord.User, name, budget, operational_cost, operational_revenue):
        """Unique set for companies, combining all necessary things."""
        global list_of_companies
        global list_of_companies_operational_cost
        global list_of_companies_operational_revenue
        global who_plays_what
        who_plays_what[user.id] = name
        list_of_companies[name] = budget
        # this one will be slightly special, as its a % value of the original budget how much is operational cost
        # but the actual  value stored is as an actual value of money
        list_of_companies_operational_cost[name] = int(budget) * int(operational_cost) / 100
        list_of_companies_operational_revenue[name] = operational_revenue
        await ctx.send(f"{user.name}'s {name} has been set to {operational_revenue}$ yearly revenue with {operational_cost}% operational cost on a {budget}$ current budget.")
 
    @commands.command(pass_context=True)
    async def listCompany(self,ctx):
        """List all Company's listed in the storage at this time."""
        global list_of_companies
        global list_of_companies_operational_cost
        global list_of_companies_operational_revenue
        answer = ""
        x = list_of_companies.keys()
        for x in list_of_companies:
            answer += x + f" = {list_of_companies[x]}$ budget with {list_of_companies_operational_cost.get(x)}% operational cost and {list_of_companies_operational_revenue.get(x)}$" + "\n"
        await ctx.send(answer)
 
 
    @commands.command(pass_context=True)
    async def leaderboard(self,ctx):
        """Leaderboard for GDP/Growth - sorts dicts then calls each list"""
        global list_of_gdps
        global list_of_gdp_growths
        global who_plays_what
        a = sorted(list_of_gdps.items(), key=lambda kv: kv[1], reverse = True)
        b = sorted(list_of_gdp_growths.items(), key=lambda x: x[1], reverse=True )
        a = {k: v for k, v in a}
        b = {k: v for k, v in b}
        a_answer = ""
        b_answer = ""
        x = a.keys()
        for x in a:
            a_answer += x + f" = {list_of_gdps[x]}$" + "\n"
        x = b.keys()
        for x in b:
            b_answer += x + f" = {list_of_gdp_growths[x]}%" + "\n"
        await ctx.send("Top Countries by GDP:\n" + a_answer + "\nTop Countries by GDP Growth:\n" + b_answer)
 
    @commands.command(pass_context=True)
    async def sponsor(self,ctx):
        """Proof of concept in regards to randomized money generation, mostly for companies"""
        global who_plays_what
        global list_of_companies_operational_revenue
        global list_of_companies
        max_money = int(list_of_companies_operational_revenue[who_plays_what.get(ctx.author.id)]) / 2
        y = int(max_money / random.randrange(1,100))
        list_of_companies[who_plays_what.get(ctx.author.id)] = int(list_of_companies[who_plays_what.get(ctx.author.id)]) + y
        await ctx.send(f'You have received a sponsorship of {y}$ value!')
 
    @commands.command(pass_context=True)
    async def update(self,ctx):
        """Update the economy of all entities (Nations and Companies so far)"""
        global list_of_gdp_growths
        global list_of_gdps
        global list_of_companies
        global list_of_companies_operational_cost
        global list_of_companies_operational_revenue
        # try-except chain to allow for peaceful testing
        # KeyErrors will be passed as i wont fill all dicts with values
        try:
            x = list_of_gdps.keys()
            for x in list_of_gdps:
                # this seperation is dumb
                # but it doesnt work if i dont do so
                # python moment
                y = int(list_of_gdps[x]) * int(list_of_gdp_growths[x]) / 100
                list_of_gdps[x] = int(list_of_gdps[x]) + y
        except:
            pass
        try:
            x = list_of_companies.keys()
            for x in list_of_companies:
                list_of_companies[x] = int(list_of_companies[x]) - int(list_of_companies_operational_cost.get(x)) + int(list_of_companies_operational_revenue.get(x))
        except:
            pass
        await ctx.send("Economy has been updated.")




