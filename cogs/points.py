import discord
from discord.ext import commands

from datetime import date

#Global Variables
sheet = None
numUsers = None
sheetc = None

def setup( client ):
    client.add_cog( points(client) )

class points( commands.Cog ):

    def __init__(self, client):
        self.client = client

        from bot import tempsheet, sheetclient
        global sheet, numUsers, sheetc
        sheet = tempsheet
        numUsers = int(sheet.cell(1,6).value)
        sheetc = sheetclient

    #OnMessage 
    @commands.Cog.listener()
    async def on_message( self, message ):
        allowed = [642483689137111080, 642483696271884309]
        if( message.author == self.client.user or message.channel.id not in allowed) :
            print("Message Detected in other Channel, Returning **(Ignore this message)**")
            return

        if( message.attachments ):
            sheetc.login()

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

            # ***SENDS MESSAGE WHEN A POINT IS EARNED, COMMENTED OUT FOR NOW***
            #embed=discord.Embed(title="Success!", description=f'{username.mention}, you earned 1 point!', color=0x87b4f8)
            #embed.set_author(name="Leaderboard Bot", icon_url="https://cdn.discordapp.com/attachments/444636835109404682/639258380296519703/leaderboard-icon-9.png")
            #await message.channel.get("").send(embed=embed)

        #await self.client.process_commands(message)  *Dont need anymore?

    
    @commands.command( pass_context = True )
    async def balance( self, ctx):
        allowed = [642483690575757347, 642483696271884309]
        if( ctx.message.channel.id not in allowed ):
            return

        sheetc.login()

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
        allowed = [642483680132071450, 642483696271884309]
        if( ctx.message.channel.id not in allowed ):
            return
        
        sheetc.login()
        leaderboard = ""
        i = 2
        while( i < 7 ):
            userid = sheet.cell( i, 13).value
            points = sheet.cell( i, 14).value
            leaderboard += f'\n\n*{i-1}) <@{userid}>* | **Points: {points}**'
            i = i + 1

        embed=discord.Embed(title="Current Leaderboard", description=leaderboard, color=0x87b4f8)
        embed.set_author(name="Leaderboard Bot", icon_url="https://cdn.discordapp.com/attachments/444636835109404682/639258380296519703/leaderboard-icon-9.png")
        await ctx.send(embed=embed)


    @commands.command( pass_context = True )
    @commands.has_permissions( administrator = True )
    async def addpoints( self, ctx ):
        allowed = [642483696271884309, 642483694287847477]
        if( ctx.message.channel.id not in allowed ):
            return

        sheetc.login()

        if len(ctx.message.mentions) == 0:
            username = ctx.message.author
        else:
            username = ctx.message.mentions[0]
        userid = username.id

        sheet.update_cell( 1, 9, str(userid)+'\"' )
        sheet.update_cell( 1, 9, sheet.cell(1,9).value.strip("\"") )

        if( sheet.cell( 1, 11).value == "#N/A"):
            temp = f'{username.mention} has **no** submissions (0 points)'
            embed=discord.Embed(title="Add Points", description=temp, color=0x87b4f8)
            embed.set_author(name="Leaderboard Bot", icon_url="https://cdn.discordapp.com/attachments/444636835109404682/639258380296519703/leaderboard-icon-9.png")
            await ctx.send( embed=embed)
            return
        else:
            i = int( sheet.cell( 1,11).value )
            points = int( sheet.cell(i,3).value )
            temp = f'{username.mention} has **{points}** points'

        embed=discord.Embed(title="Add Points", description=temp, color=0x87b4f8)
        embed.set_author(name="Leaderboard Bot", icon_url="https://cdn.discordapp.com/attachments/444636835109404682/639258380296519703/leaderboard-icon-9.png")
        embed.add_field(name="\u200b", value="How many points would you like to add?", inline=True)
        await ctx.send(embed=embed)
    
        while True:
            temp = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
            if temp.content.lower() == "quit" or temp.content.lower() == "q":
                embed=discord.Embed(title="Add Points", description="Command has been canceled", color=0x87b4f8)
                embed.set_author(name="Leaderboard Bot", icon_url="https://cdn.discordapp.com/attachments/444636835109404682/639258380296519703/leaderboard-icon-9.png")
                await ctx.send(embed=embed)
                return
            elif temp.content.isdigit() is False:
                embed=discord.Embed(title="Add Points", description="Please enter a valid positive integer", color=0x87b4f8)
                embed.set_author(name="Leaderboard Bot", icon_url="https://cdn.discordapp.com/attachments/444636835109404682/639258380296519703/leaderboard-icon-9.png")
                await ctx.send(embed=embed)
            else:
                sheet.update_cell( i , 3, int( sheet.cell( i, 3).value ) + int(temp.content) )
                points = int( sheet.cell(i,3).value )
                description = f'{username.mention} has **{points}** points'
                embed=discord.Embed(title=f'Added {temp.content} Points', description=description, color=0x87b4f8)
                embed.set_author(name="Leaderboard Bot", icon_url="https://cdn.discordapp.com/attachments/444636835109404682/639258380296519703/leaderboard-icon-9.png")
                await ctx.send(embed=embed)
                print(f'Updated {username}\'s points on leaderboard')
                return


    @commands.command( pass_context = True )
    @commands.has_permissions( administrator = True )
    async def removepoints( self, ctx ):
        allowed = [642483696271884309, 642483694287847477]
        if( ctx.message.channel.id not in allowed ):
            return
            
        sheetc.login()

        if len(ctx.message.mentions) == 0:
            username = ctx.message.author
        else:
            username = ctx.message.mentions[0]
        userid = username.id

        sheet.update_cell( 1, 9, str(userid)+'\"' )
        sheet.update_cell( 1, 9, sheet.cell(1,9).value.strip("\"") )
        
        if( sheet.cell( 1, 11).value == "#N/A"):
            temp = f'{username.mention} has **no** submissions (0 points)'
            embed=discord.Embed(title="Remove Points", description=temp, color=0x87b4f8)
            embed.set_author(name="Leaderboard Bot", icon_url="https://cdn.discordapp.com/attachments/444636835109404682/639258380296519703/leaderboard-icon-9.png")
            await ctx.send( embed=embed)
            return
        else:
            i = int( sheet.cell( 1,11).value )
            points = int( sheet.cell(i,3).value )
            temp = f'{username.mention} has **{points}** points'

        embed=discord.Embed(title="Remove Points", description=temp, color=0x87b4f8)
        embed.set_author(name="Leaderboard Bot", icon_url="https://cdn.discordapp.com/attachments/444636835109404682/639258380296519703/leaderboard-icon-9.png")
        embed.add_field(name="\u200b", value="How many points would you like to remove?", inline=True)
        await ctx.send(embed=embed)

        while True:
            temp = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
            if temp.content.lower() == "quit" or temp.content.lower() == "q":
                embed=discord.Embed(title="Remove Points", description="Command has been canceled", color=0x87b4f8)
                embed.set_author(name="Leaderboard Bot", icon_url="https://cdn.discordapp.com/attachments/444636835109404682/639258380296519703/leaderboard-icon-9.png")
                await ctx.send(embed=embed)
                return
            elif temp.content.isdigit() is False:
                embed=discord.Embed(title="Remove Points", description="Please enter a valid positive integer", color=0x87b4f8)
                embed.set_author(name="Leaderboard Bot", icon_url="https://cdn.discordapp.com/attachments/444636835109404682/639258380296519703/leaderboard-icon-9.png")
                await ctx.send(embed=embed)
            else:
                sheet.update_cell( i , 3, int( sheet.cell( i, 3).value ) - int(temp.content) )
                points = int( sheet.cell(i,3).value )
                description = f'{username.mention} has **{points}** points'
                embed=discord.Embed(title=f'Removed {temp.content} Points', description=description, color=0x87b4f8)
                embed.set_author(name="Leaderboard Bot", icon_url="https://cdn.discordapp.com/attachments/444636835109404682/639258380296519703/leaderboard-icon-9.png")
                await ctx.send(embed=embed)
                print(f'Updated {username}\'s points on leaderboard')
                return


    @commands.command( pass_context = True )
    async def test( self, ctx):
        today = date.today()
        print("Today's date:", today)

