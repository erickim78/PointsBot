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
        global numUsers
        sheet = tempsheet
        numUsers = int(sheet.cell(1,6).value)

    
    #OnMessage 
    @commands.Cog.listener()
    async def on_message( self, message ):
        if( message.author == self.client.user or message.channel.id != 639181046390325269):
            return

        if( message.attachments ):
            global numUsers
            username = message.author
            userid = username.id

            sheet.update_cell( 1, 9, str(userid)+'\"' )
            sheet.update_cell( 1, 9, sheet.cell(1,9).value.strip("\"") )

            if( sheet.cell( 1, 11).value == "#N/A"):
                sheet.update_cell( 1,6, numUsers + 1)
                numUsers = int(sheet.cell(1,6).value)
                sheet.update_cell( numUsers + 1, 1, str(username) )
                sheet.update_cell( numUsers + 1, 2, str(userid)+'\"' )
                sheet.update_cell( numUsers + 1, 2, sheet.cell(numUsers + 1, 2).value.strip("\"") )  #Have to add as string b/c sheets api doesnt like such a long number
                sheet.update_cell( numUsers + 1, 3, 1)
                print(f'Added {username} to leaderboard')
            else:
                i = int( sheet.cell( 1,11).value )
                sheet.update_cell( i , 3, int( sheet.cell( i, 3).value ) + 1 )
                print(f'Updated {username}\'s points on leaderboard')
                

        #await self.client.process_commands(message)  *Dont need anymore?

    
    @commands.command( pass_context = True )
    async def balance( self, ctx):
        username = ctx.message.author
        userid = username.id
        i = numUsers

        sheet.update_cell( 1, 9, str(userid)+'\"' )
        sheet.update_cell( 1, 9, sheet.cell(1,9).value.strip("\"") )

        if( sheet.cell( 1, 11).value == "#N/A"):
            temp = f'{username.mention} has **no** submissions'
        else:
            i = int( sheet.cell( 1,11).value )
            points = int( sheet.cell(i,3).value )
            temp = f'{username.mention} has **{points}** points'

        embed=discord.Embed(title="Your Points:", description=temp, color=0x87b4f8)
        embed.set_author(name="Leaderboard Bot", icon_url="https://cdn.discordapp.com/attachments/444636835109404682/639258380296519703/leaderboard-icon-9.png")
        await ctx.send(embed=embed)


    @commands.command( pass_context = True )
    async def leaderboard( self, ctx):
        username = ctx.message.author

        points = 0
        leaderboard = ""
        arr = []

        i = 0
        while( i < 5 and i < numUsers):
            j = 1
            mostid = 0
            mostpoints = 0
            while( j <= numUsers ):
                current = int( sheet.cell(j + 1, 2).value )
                currentpoints = int( sheet.cell(j + 1, 3).value )
                if( current not in arr and currentpoints >= mostpoints ):
                    mostid = current
                    mostpoints = currentpoints
                j += 1

            leaderboard += f'\n\n*{i+1}) <@{mostid}>* | **Points: {mostpoints}**'
            arr.append(mostid)

            i += 1

        embed=discord.Embed(title="Current Leaderboard", description=leaderboard, color=0x87b4f8)
        embed.set_author(name="Leaderboard Bot", icon_url="https://cdn.discordapp.com/attachments/444636835109404682/639258380296519703/leaderboard-icon-9.png")
        #embed.add_field(name="\u200b", value=f'{username.mention}, you are rank **1** of {numUsers} with {points} points', inline=True)
        await ctx.send(embed=embed)


    @commands.command( pass_context = True )
    async def test( self, ctx):
        userid = ctx.author.id
        print( sheet.cell( 1, 11).value )
        sheet.update_cell( 1, 9, str(userid)+'\"' )
        sheet.update_cell( 1, 9, sheet.cell(1,9).value.strip("\"") )
        print( sheet.cell( 1, 11).value )

