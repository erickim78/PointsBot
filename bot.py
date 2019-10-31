#Importing Discord 
import discord
from discord.ext import commands

#Oath2
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Misc Imports
import json
import os

#Config File
with open('config.json') as config_file:
    config = json.load( config_file )

#Sheets Oath
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('sheetscredentials.json', scope)
client = gspread.authorize(creds)
tempsheet = client.open('points').sheet1

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
