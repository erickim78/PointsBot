import discord
from discord.ext import commands

def setup( client ):
    client.add_cog(initial(client) )

class initial( commands.Cog ):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('PointsBOT is RUNNING.\n')