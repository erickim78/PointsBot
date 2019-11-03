import discord
from discord.ext import commands

def setup( client ):
    client.add_cog(initial(client) )

class initial( commands.Cog ):

    def __init__(self, client):
        self.client = client
        client.remove_command('help')


    @commands.Cog.listener()
    async def on_ready(self):
        print('PointsBOT is RUNNING.')

    @commands.command( pass_context = True)
    async def help(self, ctx):
        embed=discord.Embed(color=0x87b4f8)
        embed.set_author(name="Leaderboard Bot", icon_url="https://cdn.discordapp.com/attachments/444636835109404682/639258380296519703/leaderboard-icon-9.png")
        embed.add_field(name="?balance", value="Check your current point balance\n\u200b", inline = True)
        embed.add_field(name="?leaderboard", value="Check the current point leaderboard\n\u200b", inline = False)
        embed.add_field(name="?addpoints @user", value="**ADMIN ONLY**: Add points to a user\n\u200b", inline = False)
        embed.add_field(name="?removepoints @user", value="**ADMIN ONLY**: Remove points from a user", inline = False)
        await ctx.send(embed=embed)
        return
