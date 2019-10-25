import discord
from discord.ext import commands

#Global Variables
sheet = None
numUsers = None

def setup( client ):
    client.add_cog( points(client) )

class points( commands.Cog ):

    def __init__(self, client):
        self.client = client

        from bot import tempsheet
        global sheet
        sheet = tempsheet
        numUsers = int(sheet.cell(1,5).value)

    
    @commands.command( pass_context = True )
    async def points( self, ctx):
        username = ctx.message.author
        embed=discord.Embed(color=0xff1515)
        embed.add_field(name="Points", value=f'{username.mention}, You have 0 points', inline=False)
        await ctx.send(embed=embed)


    @commands.command( pass_context = True )
    async def leaderboard( self, ctx ):
        points = 0
        username = ctx.message.author
        count = 1

        leaderboard = f'\n\n*{count}) {username}*\n **Points: {points}**'
        leaderboard += f'\n\n*{count}) {username}*\n **Points: {points}**'
        leaderboard += f'\n\n*{count}) {username}*\n **Points: {points}**'
        leaderboard += f'\n\n*{count}) {username}*\n **Points: {points}**'
        leaderboard += f'\n\n*{count}) {username}*\n **Points: {points}**'

        embed=discord.Embed(color=0xff1515)
        embed.add_field(name=f'Leaderboard', value=f'{username.mention}, You are #1 out of 1\n\n', inline=False)
        embed.add_field(name="Top 5:", value=leaderboard, inline=False)
        await ctx.send(embed=embed)


    @commands.command( pass_context = True )
    async def test( self, ctx):
        global numUsers
        await ctx.send(f'{sheet.cell(1,1).value}')
        await ctx.send(numUsers)
        numUsers += 1
        sheet.update_cell(1,5, numUsers)
        await ctx.send(sheet.cell(1,5).value)






        