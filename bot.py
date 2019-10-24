#Importing Discord 
import discord
from discord.ext import commands

#Misc Imports
import json
import os

#Config File
with open('config.json') as config_file:
    config = json.load( config_file )

#REPLACE '!' WITH ANY CHAR TO CHANGE COMMAND PREFIX
client = commands.Bot( command_prefix = '!')
serverid = config['serverid']

#Loading All Cogs/Commands in cogs folder
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#Run Bot
token = config['token']
client.run(token)
