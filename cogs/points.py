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
        numUsers = int(sheet.cell(1,8).value)

    
    #OnMessage 
    @commands.Cog.listener()
    async def on_message( self, message ):
        if( message.author == self.client.user or message.channel.id != 637115299883122708):
            return

        if( message.attachments ):
            global numUsers
            username = message.author
            userid = username.id
            i = numUsers
            dexists = True
            while( i > 0 ):
                dexists = True
                if( str( sheet.cell( i + 1, 2).value ) != userid ):
                    sheet.update_cell( i + 1, 3, int(sheet.cell( i + 1, 3).value ) + 1 )
                    dexists = False
                    print(f'Updated {username}\'s points on leaderboard')
                    break
                i -= 1
            
            if( dexists ):
                sheet.update_cell( 1,8, numUsers + 1)
                numUsers = int(sheet.cell(1,8).value)
                sheet.update_cell( numUsers + 1, 1, str(username) )
                sheet.update_cell( numUsers + 1, 2, str(userid)+'\"' )
                sheet.update_cell( numUsers + 1, 2, sheet.cell(numUsers + 1, 2).value.strip("\"") )  #Have to add as string b/c sheets api doesnt like such a long number
                sheet.update_cell( numUsers + 1, 3, 1)
                print(f'Added {username} to leaderboard')

        #await self.client.process_commands(message)  *Dont need anymore?

    
    @commands.command( pass_context = True )
    async def points( self, ctx):
        username = ctx.message.author
        userid = username.id
        i = numUsers
        temp = f'{username.mention} has **no** submissions'
        while( i > 0 ):
            if( int( sheet.cell(i + 1,2).value ) == userid ):
                points = int( sheet.cell(i + 1,3).value )
                if( points == 1 ):
                    temp = f'{username.mention} has **{points}** point'
                else:
                    temp = f'{username.mention} has **{points}** points'

                break
            i -= 1

        embed=discord.Embed(title="Your Points:", description=temp, color=0x87b4f8)
        embed.set_author(name="Leaderboard Bot", icon_url="https://i.imgur.com/YSZg8kU.png")
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

        embed=discord.Embed(title="TOP 5", description=leaderboard, color=0x87b4f8)
        embed.set_author(name="Leaderboard Bot", icon_url="https://i.imgur.com/YSZg8kU.png")
        await ctx.send(embed=embed)







        